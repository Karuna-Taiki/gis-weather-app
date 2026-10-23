import os
import re
import sys
import tempfile
import traceback
import datetime
import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.feature as cfeature
import cartopy.io.shapereader as shapereader
import cv2
from PIL import Image

import streamlit as st

# ==========================================
# 1. デザイン設定（CSS）
# ==========================================
st.set_page_config(page_title="地球科学GIS総合アナライザー", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
    }
    body {
        translate: no !important;
    }
    [data-testid="stForm"] {
        border: 1px solid #707070 !important;
        border-radius: 24px !important;
        padding: 40px !important;
        background-color: #FFFFFF !important;
        max-width: 500px;
        margin: 0 auto;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
    }
    [data-testid="stForm"] label {
        color: #555555 !important;
        font-weight: bold;
        font-size: 16px;
    }
    div[data-baseweb="input"] {
        background-color: #EFEFEF !important;
        border-radius: 4px !important;
        border: none !important;
    }
    input {
        background-color: #EFEFEF !important;
        color: #333333 !important;
    }
    [data-testid="stFormSubmitButton"] button {
        background-color: #4A80E6 !important;
        color: white !important;
        border: none !important;
        padding: 10px 30px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 4px !important;
        width: auto !important;
        display: block !important;
        margin: 20px auto 0 auto !important;
    }
    .login-title {
        text-align: center;
        color: #555555;
        font-size: 30px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* --- サイドバーメニューボタンのデザイン --- */
    [data-testid="stSidebar"] button[kind="secondary"] {
        background-color: #F8F9FA !important;
        color: #333333 !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 8px !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 8px 14px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        margin-bottom: 4px !important;
        transition: all 0.2s ease-in-out !important;
        min-height: unset !important;
    }
    [data-testid="stSidebar"] button[kind="secondary"]:hover {
        background-color: #E8F0FE !important;
        border-color: #D2E3FC !important;
        color: #1A73E8 !important;
    }

    /* 選択中（アクティブ）ボタンのデザイン */
    [data-testid="stSidebar"] button[kind="primary"] {
        background-color: #D2E3FC !important;
        color: #041E49 !important;
        border: 1px solid #A8C7FA !important;
        border-radius: 8px !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 8px 14px !important;
        font-size: 14px !important;
        font-weight: bold !important;
        margin-bottom: 4px !important;
        box-shadow: none !important;
        min-height: unset !important;
    }

    /* Logoutボタンをサイドバー最下部に固定 */
    div.element-container:has(button#logout_btn) {
        position: fixed !important;
        bottom: 20px !important;
        left: 20px !important;
        width: 200px !important;
        z-index: 999999 !important;
    }
    button#logout_btn {
        background-color: #FFFFFF !important;
        color: #555555 !important;
        border: 1px solid #CCCCCC !important;
        border-radius: 8px !important;
        padding: 6px 16px !important;
        font-size: 14px !important;
    }
    button#logout_btn:hover {
        background-color: #F5F5F5 !important;
        color: #000000 !important;
    }

    /* 撮影履歴カードの枠組みスタイル */
    .history-card {
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 12px;
        background-color: #FAFAFA;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 地図作成・可視化エンジン
# ==========================================
def generate_weather_map(file_paths, element_type, custom_column=""):
    reader = None
    try:
        if not file_paths:
            raise ValueError("処理対象のファイルが選択されていません。")

        valid_paths = []
        for path in file_paths:
            if not os.path.exists(path):
                continue
            base, ext = os.path.splitext(path)
            if ext.lower() == '.dbf':
                shp_path = base + '.shp'
                if os.path.exists(shp_path):
                    valid_paths.append(shp_path)
                else:
                    valid_paths.append(path)
            else:
                valid_paths.append(path)

        valid_paths = sorted(list(set(valid_paths)))

        if not valid_paths:
            raise FileNotFoundError("有効なGISデータファイル（.shp または .dbf）が見つかりませんでした。")

        lons_list, lats_list, values_list = [], [], []

        def clean_attributes(attrs):
            cleaned = {}
            for k, v in attrs.items():
                clean_key = k.split('\x00')[0].strip()
                cleaned[clean_key] = v
            return cleaned

        target_key = None
        scale_factor = 1.0
        unit = ""

        try:
            reader = shapereader.Reader(valid_paths[0], encoding='cp932')
            records = list(reader.records())
        except Exception as read_err:
            raise RuntimeError(f"ファイル読み込みエラー: {str(read_err)}")
        finally:
            if reader:
                reader.close()
                reader = None

        if not records:
            raise ValueError("ファイルの中身が空です。")

        sample_attrs = clean_attributes(records[0].attributes)

        if element_type == '気温':
            candidates = ['G02_053', 'G02_002', 'G02_011']
            for cand in candidates:
                if cand in sample_attrs:
                    target_key = cand
                    break
            scale_factor = 0.1
            unit = "年平均気温 (°C)"
        elif element_type == '降水量':
            candidates = ['G02_014', 'G02_003', 'G02_012']
            for cand in candidates:
                if cand in sample_attrs:
                    target_key = cand
                    break
            scale_factor = 0.1
            unit = "年降水量 (mm)"
        elif element_type == 'カスタム列':
            target_key = custom_column
            scale_factor = 1.0
            unit = f"カスタム値 ({target_key})"

        if not target_key or target_key not in sample_attrs:
            available_keys = [k for k in sample_attrs.keys() if k.startswith('G02_')]
            if len(available_keys) > 1:
                target_key = available_keys[1]
            else:
                raise KeyError(f"指定された列「{target_key}」が存在しません。利用可能: {list(sample_attrs.keys())}")

        for file_path in valid_paths:
            try:
                reader = shapereader.Reader(file_path, encoding='cp932')
                records = list(reader.records())
            except Exception:
                continue
            finally:
                if reader:
                    reader.close()
                    reader = None

            for record in records:
                attrs = clean_attributes(record.attributes)
                val_raw = attrs.get(target_key)
                if val_raw is None:
                    continue

                mesh_code = None
                for k in ['G02_001', 'KEY_CODE', 'MESH_CODE']:
                    if k in attrs and attrs[k] is not None:
                        mesh_code = str(attrs[k]).strip().split('.')[0]
                        break

                if mesh_code and len(mesh_code) == 8 and mesh_code.isdigit():
                    p1, p2, p3, p4, p5, p6, p7, p8 = map(int, mesh_code)
                    lat = (p1 * 10 + p2) / 1.5 + p5 * (5 / 60) + p7 * (30 / 3600) + (15 / 3600)
                    lon = (p3 * 10 + p4) + 100 + p6 * (7.5 / 60) + p8 * (45 / 3600) + (22.5 / 3600)
                else:
                    if record.geometry is None:
                        continue
                    bounds = record.geometry.bounds
                    lon = (bounds[0] + bounds[2]) / 2
                    lat = (bounds[1] + bounds[3]) / 2

                lons_list.append(lon)
                lats_list.append(lat)
                try:
                    values_list.append(float(val_raw) * scale_factor)
                except ValueError:
                    continue

        lons_arr = np.array(lons_list)
        lats_arr = np.array(lats_list)
        values_arr = np.array(values_list)

        if len(values_arr) == 0:
            raise ValueError("有効な数値データが見つかりませんでした。")

        lonmin, lonmax = lons_arr.min() - 0.5, lons_arr.max() + 0.5
        latmin, latmax = lats_arr.min() - 0.5, lats_arr.max() + 0.5

        area_size = (lonmax - lonmin) * (latmax - latmin)
        marker_size = 3.0 if area_size > 100 else (12.0 if area_size > 20 else 35.0)

        if element_type == '気温':
            levels = [-5, 0, 5, 10, 15, 20, 25, 30]
            colors = ['blue', 'deepskyblue', 'greenyellow', 'yellow', 'orange', 'red', 'darkred']
        elif element_type == '降水量':
            levels = [0, 500, 1000, 1500, 2000, 2500, 3000, 4000]
            colors = ['#ffffff', '#b3d9ff', '#3399ff', '#0066cc', '#003399', '#9900cc', '#660066']
        else:
            levels = np.linspace(values_arr.min(), values_arr.max(), 8)
            colors = ['blue', 'cyan', 'green', 'yellow', 'orange', 'red', 'purple']

        cmap = mcolors.ListedColormap(colors[:len(levels)-1])
        norm = mcolors.BoundaryNorm(levels, cmap.N)

        plt.rcParams['font.family'] = 'MS Gothic'
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax.set_extent([lonmin, lonmax, latmin, latmax], ccrs.PlateCarree())

        try:
            ax.coastlines(resolution='10m')
            province = cfeature.NaturalEarthFeature(
                category='cultural', name='admin_1_states_provinces',
                scale='10m', facecolor='none', edgecolor='gray', lw=0.5
            )
            ax.add_feature(province)
        except Exception:
            pass

        axc = ax.scatter(lons_arr, lats_arr, c=values_arr, cmap=cmap, norm=norm, 
                         s=marker_size, marker='s', edgecolors='none', transform=ccrs.PlateCarree())

        cb = fig.colorbar(axc, orientation="vertical", pad=0.03, shrink=0.8, ticks=levels)
        cb.set_label(unit, fontsize=12)

        dlon = dlat = 1.0 if area_size < 30 else 2.0
        xticks = np.arange(np.floor(lonmin), np.ceil(lonmax)+0.1, dlon)
        yticks = np.arange(np.floor(latmin), np.ceil(latmax)+0.1, dlat)
        ax.set_xticks(xticks, crs=ccrs.PlateCarree())
        ax.set_yticks(yticks, crs=ccrs.PlateCarree())
        ax.xaxis.set_major_formatter(LongitudeFormatter())
        ax.yaxis.set_major_formatter(LatitudeFormatter())

        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
        gl.xlocator = mticker.FixedLocator(xticks)
        gl.ylocator = mticker.FixedLocator(yticks)
        ax.set_title(f"選択データ可視化：{unit}", fontsize=14)

        return fig

    except Exception as e:
        plt.clf()
        plt.close('all')
        raise e

# ==========================================
# 3. サーモグラフィ画像処理エンジン
# ==========================================
def process_thermal_frame(img_pil, cmap_name='inferno'):
    """入力画像を輝度に応じてサーモグラフィ風の熱可視化画像へ変換"""
    img_np = np.array(img_pil)
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    
    # コントラスト強調
    equalized = cv2.equalizeHist(gray)
    
    # Matplotlibのカラーマップを適用
    cmap = plt.get_cmap(cmap_name)
    thermal_np = (cmap(equalized / 255.0)[:, :, :3] * 255).astype(np.uint8)
    
    return Image.fromarray(thermal_np)

def pil_to_bytes(img_pil):
    """PIL画像をダウンロード用のバイトデータ（PNG）へ変換"""
    buf = io.BytesIO()
    img_pil.save(buf, format="PNG")
    return buf.getvalue()

# ==========================================
# 4. 簡易認証処理
# ==========================================
if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = False

if not st.session_state["authentication_status"]:
    # ログイン画面のシステムタイトル変更
    st.markdown('<div class="login-title">地球科学GIS総合アナライザー</div>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if username == "admin" and password == "cdctype":
                st.session_state["authentication_status"] = True
                st.session_state["name"] = "テスト"
                st.rerun()
            else:
                st.error("ユーザー名またはパスワードが間違っています")

authentication_status = st.session_state.get("authentication_status")
name = st.session_state.get("name", "管理者")

# ==========================================
# 5. 画面制御メインルーチン
# ==========================================
if authentication_status:
    if "selected_menu" not in st.session_state:
        st.session_state.selected_menu = "気象データ可視化マップ"

    if "thermal_history" not in st.session_state:
        st.session_state.thermal_history = []

    # カメラON/OFF状態の初期化（初期値はOFF）
    if "camera_active" not in st.session_state:
        st.session_state.camera_active = False

    # --- 1. サイドバー領域 ---
    with st.sidebar:
        st.write(f"👤 ログイン中: **{name}** さん")
        
        # サイドメニューの名称整理
        menu_items = [
            ("🗺️  気象データ可視化マップ", "気象データ可視化マップ"),
            ("🗾  地形図", "地形図"),
            ("📹  Liveカメラ映像", "Liveカメラ映像"),
            ("💧  ため池・ダム・湖データ", "ため池・ダム・湖データ")
        ]

        for label, key_name in menu_items:
            is_active = (st.session_state.selected_menu == key_name)
            if st.button(
                label,
                key=f"nav_btn_{key_name}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.selected_menu = key_name
                st.rerun()

        if st.button("Logout", key="logout_btn"):
            st.session_state["authentication_status"] = False
            st.session_state.camera_active = False
            st.rerun()

    # --- 2. メインコンテンツ領域 ---
    current_page = st.session_state.selected_menu

    if current_page == "気象データ可視化マップ":
        st.header("🗺️ 気象データ可視化マップ")
        st.markdown("---")

        st.subheader("1. 対象データの指定")
        uploaded_files = st.file_uploader(
            "GISデータ（.shp / .dbf）を選択してください（複数選択可能）",
            type=["shp", "dbf"],
            accept_multiple_files=True
        )

        st.subheader("2. 可視化する気象要素の選択")
        col1, col2 = st.columns(2)
        with col1:
            use_temp = st.checkbox("年平均気温", value=True)
            use_rain = st.checkbox("年降水量", value=False)
        with col2:
            use_custom = st.checkbox("カスタム列指定", value=False)
            custom_col = st.text_input("カスタム列名", value="", disabled=not use_custom)

        st.markdown("---")

        if st.button("地図レポートを生成・表示", type="primary"):
            if not uploaded_files:
                st.error("ファイルをアップロードしてください。")
            else:
                with tempfile.TemporaryDirectory() as tmpdir:
                    saved_paths = []
                    for file in uploaded_files:
                        path = os.path.join(tmpdir, file.name)
                        with open(path, "wb") as f:
                            f.write(file.getbuffer())
                        saved_paths.append(path)

                    elements_to_run = []
                    if use_temp: elements_to_run.append("気温")
                    if use_rain: elements_to_run.append("降水量")
                    if use_custom and custom_col: elements_to_run.append("カスタム列")

                    if not elements_to_run:
                        st.warning("出力対象の要素を少なくとも1つ選択してください。")
                    else:
                        for elem in elements_to_run:
                            st.subheader(f"📊 結果: {elem}")
                            with st.spinner(f"{elem} の地図を生成中..."):
                                try:
                                    fig = generate_weather_map(saved_paths, elem, custom_col)
                                    st.pyplot(fig)
                                except Exception as e:
                                    st.error(f"エラーが発生しました: {str(e)}")
                                    st.code(traceback.format_exc())

    elif current_page == "地形図":
        st.header("🗾 地形図")
        st.markdown("---")
        st.info("地形図の閲覧機能は現在準備中です。")

    elif current_page == "Liveカメラ映像":
        st.header("📹 Liveカメラ映像（サーモグラフィモード）")
        st.markdown("---")
        st.markdown("カメラ画像から背景（人・地形・建物等）の温度分布をリアルタイムで解析・保存します。")

        col_ctrl1, col_ctrl2 = st.columns([1, 2])
        with col_ctrl1:
            cmap_choice = st.selectbox(
                "サーモグラフィの配色タイプを選んでください",
                options=["inferno", "jet", "plasma", "rainbow"],
                format_func=lambda x: {
                    "inferno": "Inferno (標準熱画像: 黒→紫→赤→黄)",
                    "jet": "Jet (レインボー: 青→緑→赤)",
                    "plasma": "Plasma (高コントラスト: 紫→オレンジ)",
                    "rainbow": "Rainbow (虹色)"
                }[x]
            )

        st.write("")
        st.subheader("📷 リアルタイム・カメラ入力")

        # --- カメラ ON / OFF コントロールボタン ---
        col_cam_btn1, col_cam_btn2 = st.columns([1, 3])
        with col_cam_btn1:
            if not st.session_state.camera_active:
                if st.button("📷 カメラを起動する (ON)", type="primary"):
                    st.session_state.camera_active = True
                    st.rerun()
            else:
                if st.button("🛑 カメラを停止する (OFF)", type="secondary"):
                    st.session_state.camera_active = False
                    st.rerun()

        # カメラ起動（ON）時のみカメラUIを表示
        if st.session_state.camera_active:
            camera_photo = st.camera_input("写真を撮影して履歴に保存", key=f"cam_input_{len(st.session_state.thermal_history)}")

            if camera_photo:
                img_input = Image.open(camera_photo)
                thermal_img = process_thermal_frame(img_input, cmap_name=cmap_choice)
                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                
                st.session_state.thermal_history.insert(0, {
                    "time": now_str,
                    "timestamp": file_timestamp,
                    "original": img_input,
                    "thermal": thermal_img,
                    "type": cmap_choice
                })
                st.rerun()
        else:
            st.info("💡 カメラ機能は現在オフになっています。「📷 カメラを起動する (ON)」を押すと撮影が開始できます。")

        st.markdown("""
        <div style="background: linear-gradient(to right, blue, cyan, green, yellow, red); height: 18px; border-radius: 4px; margin-top: 15px;"></div>
        <div style="display: flex; justify-content: space-between; font-weight: bold; font-size: 12px; margin-top: 4px; color: #555;">
            <span>低温 / 背景 (約15°C〜)</span>
            <span>中温 (約25°C〜)</span>
            <span>高温 / 人体・光源 (約36°C〜)</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        
        # --- 撮影履歴一覧表示 ---
        st.subheader("📋 撮影解析履歴一覧")
        
        if not st.session_state.thermal_history:
            st.info("まだ撮影された画像はありません。カメラを起動して撮影を行ってください。")
        else:
            for idx, item in enumerate(st.session_state.thermal_history):
                with st.container():
                    st.markdown(f'<div class="history-card">', unsafe_allow_html=True)
                    
                    header_col1, header_col2 = st.columns([4, 1])
                    with header_col1:
                        st.markdown(f"**🕒 撮影日時: {item['time']}** （タイプ: {item['type']}）")
                    with header_col2:
                        if st.button("🗑️ 行削除", key=f"del_btn_{idx}_{item['timestamp']}", type="secondary"):
                            st.session_state.thermal_history.pop(idx)
                            st.rerun()

                    col_img1, col_img2 = st.columns(2)
                    with col_img1:
                        st.image(item["original"], caption="元画像 (可視光)", use_container_width=True)
                        st.download_button(
                            label="📥 元画像をダウンロード",
                            data=pil_to_bytes(item["original"]),
                            file_name=f"original_{item['timestamp']}.png",
                            mime="image/png",
                            key=f"dl_orig_{idx}_{item['timestamp']}"
                        )

                    with col_img2:
                        st.image(item["thermal"], caption="サーモグラフィ解析画像", use_container_width=True)
                        st.download_button(
                            label="📥 サーモ画像をダウンロード",
                            data=pil_to_bytes(item["thermal"]),
                            file_name=f"thermal_{item['timestamp']}.png",
                            mime="image/png",
                            key=f"dl_therm_{idx}_{item['timestamp']}"
                        )

                    st.markdown('</div>', unsafe_allow_html=True)

    elif current_page == "ため池・ダム・湖データ":
        st.header("💧 ため池・ダム・湖データ")
        st.markdown("---")
        st.info("ため池・ダム・湖のデータ解析機能は現在準備中です。")
