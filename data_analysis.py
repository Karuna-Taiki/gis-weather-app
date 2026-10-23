<!DOCTYPE html>
<html>
<head>
  <base target="_top">
  <meta name="robots" content="noindex, nofollow">

  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap" rel="stylesheet">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <style>
    /* --- 基本スタイル（PC・タブレット共通） --- */
    body { font-family: 'Noto Sans JP', sans-serif; background-color: #f5f7fa; color: #333; margin: 0; padding: 0; }

    /* --- レイアウト構造 --- */
    #app { display: flex; flex-direction: column; min-height: 100vh; }
    .main-content { flex: 1; padding: 20px; width: 100%; max-width: 960px; margin: 0 auto; box-sizing: border-box; }

    /* --- ヘッダー（背景：#17184B / 文字：白色 / ボタン：黄色） --- */
    .site-header {
      background-color: #17184B; 
      padding: 30px 0;
      position: relative;
      box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    }
    .header-inner { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
    .header-logo { position: absolute; top: 15px; left: 20px; z-index: 10; }
    .header-logo img { height: 30px; width: auto; display: block; }
    .header-text { text-align: left; padding-left: 180px; }
    .header-title { font-size: 1.5rem; font-weight: bold; color: #fff; margin-top: 0; } 
    .header-desc { font-size: 0.9rem; line-height: 1.6; color: #fff; margin: 0; } 
    .header-desc span { font-weight: bold; color: #fff; } 

    /* ヘッダー内の問い合わせボタン */
    .header-cta-btn {
      display: inline-block;
      margin-top: 20px;
      background-color: #fbdc00; 
      color: #0E3A8A;            
      text-decoration: none;
      font-weight: bold;
      font-size: 1rem;
      padding: 12px 40px;
      border-radius: 50px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.15);
      transition: all 0.3s ease;
    }
    .header-cta-btn:hover {
      background-color: #e5c900;
      transform: translateY(-2px);
      box-shadow: 0 6px 15px rgba(0,0,0,0.25);
    }
    .header-cta-btn::before {
      content: "✉";
      margin-right: 8px;
    }

    /* --- フッター（背景：#17184B / 文字：白色） --- */
    .site-footer { 
      background-color: #17184B; 
      color: #fff;               
      padding: 40px 20px 20px; 
      margin-top: 50px; 
      box-shadow: 0 -4px 10px rgba(0,0,0,0.05);
    }
    .footer-inner { max-width: 1000px; margin: 0 auto; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 40px; }
    .footer-section { flex: 1; min-width: 280px; }
    .footer-title { font-size: 1.1rem; font-weight: bold; margin-bottom: 20px; border-left: 4px solid #fbdc00; padding-left: 10px; color: #fff; }
    .footer-info p { margin: 8px 0; font-size: 0.9rem; line-height: 1.6; color: #fff; }
    .copyright { text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.2); font-size: 0.8rem; color: #fff; }

    /* --- 上に戻るボタン --- */
    .scroll-top-btn {
      position: fixed; bottom: 30px; right: 20px; width: 50px; height: 50px;
      background-color: #fbdc00; color: #0E3A8A; border: 2px solid #0E3A8A; border-radius: 50%;
      font-size: 1.5rem; font-weight: bold; cursor: pointer;
      box-shadow: 0 4px 10px rgba(0,0,0,0.15); z-index: 1000;
      display: flex; align-items: center; justify-content: center;
      transition: all 0.3s ease; opacity: 0; pointer-events: none;
    }
    .scroll-top-btn.visible { opacity: 0.95; pointer-events: auto; }
    .scroll-top-btn:hover { background-color: #e5c900; transform: translateY(-3px); opacity: 1; }
    @media (min-width: 940px) { .scroll-top-btn { right: auto; left: 50%; margin-left: 450px; } }

    /* 検索ボックス */
    .search-section { text-align: center; margin-bottom: 20px; }
    .search-box { 
      width: 100%; 
      max-width: 600px; 
      padding: 15px 20px; 
      font-size: 1rem; 
      border: 2px solid #17184B; 
      border-radius: 50px; 
      outline: none; 
      transition: box-shadow 0.3s; 
      box-sizing: border-box; 
      color: #17184B;
    }
    .search-box:focus { box-shadow: 0 0 10px rgba(23, 24, 75, 0.4); }
    
    .search-box::placeholder {
      color: #17184B;
      opacity: 0.7;
    }

    /* カテゴリタブ スタイル調整 */
    .tab-container { display: flex; flex-direction: row; justify-content: center; align-items: center; margin-bottom: 20px; gap: 10px; flex-wrap: wrap; }
    .tab-all-wrapper { display: flex; justify-content: center; }
    .tab-sub-wrapper { display: flex; justify-content: center; flex-wrap: nowrap; gap: 10px; }

    /* メインタブボタン */
    .tab-btn { 
      padding: 8px 16px; 
      border: 2px solid #17184B; 
      background: #fff; 
      color: #17184B; 
      border-radius: 4px; 
      cursor: pointer; 
      font-weight: bold; 
      transition: all 0.3s; 
      font-size: 0.9rem; 
      white-space: nowrap; 
      min-width: 100px; 
      text-align: center; 
      box-sizing: border-box; 
    }
    .tab-btn:hover { background-color: #eef4ff; }
    .tab-btn.active { background: #17184B; color: #fff; border-color: #17184B; }

    /* サブフィルター（職種タブ） */
    .filter-container { text-align: center; margin-bottom: 20px; display: flex; justify-content: center; flex-wrap: wrap; gap: 15px; }
    .filter-link { cursor: pointer; color: #17184B; border-bottom: 2px solid transparent; padding-bottom: 2px; font-size: 0.9rem; }
    .filter-link:hover, .filter-link.active { color: #17184B; border-bottom: 2px solid #17184B; font-weight: bold; }

    /* 操作ガイド・注意書きボックス */
    .usage-guide-box {
      background-color: #eef4ff;
      border-left: 4px solid #17184B;
      padding: 10px 15px;
      margin-bottom: 15px;
      border-radius: 4px;
      font-size: 0.85rem;
      color: #17184B;
      line-height: 1.5;
    }
    .usage-guide-box strong {
      font-weight: bold;
      color: #17184B;
    }

    /* 視覚的中央揃え */
    .status-bar {
      display: flex;
      justify-content: space-between;
      align-items: center; 
      background-color: #f0f5ff;
      border: 1px solid #b2ccff;
      border-radius: 8px;
      padding: 10px 20px;
      margin-bottom: 25px;
      font-size: 0.9rem;
      color: #17184B;
      box-shadow: 0 2px 4px rgba(23, 24, 75, 0.08);
      box-sizing: border-box;
      line-height: 1; 
    }
    .status-condition {
      font-weight: 500;
      word-break: break-all;
      display: flex;
      align-items: center;
      color: #17184B;
    }
    .status-right-group {
      display: flex;
      align-items: center;
      gap: 15px;
    }
    .status-count {
      white-space: nowrap;
      font-weight: 500;
      display: flex;
      align-items: center; 
      color: #17184B;
    }
    .status-count-num {
      font-size: 1.2rem;
      font-weight: bold;
      color: #17184B;
      margin: 0 4px;
      line-height: 1;
      position: relative;
      top: -1px; 
    }

    /* 全選択ボタン */
    .select-all-btn {
      background-color: #fff;
      border: 1px solid #17184B;
      color: #17184B;
      padding: 5px 12px;
      border-radius: 4px;
      font-size: 0.8rem;
      font-weight: bold;
      cursor: pointer;
      transition: all 0.2s;
      white-space: nowrap;
    }
    .select-all-btn:hover {
      background-color: #17184B;
      color: #fff;
    }

    .card-list { display: flex; flex-direction: column; gap: 30px; }

    .local-loading {
      text-align: center; padding: 60px 20px; color: #888; background: #fff;
      border-radius: 8px; border: 1px dashed #ccc; margin-top: 20px;
    }

    /* カードスタイル */
    .p-job-card { background: #fff; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    .p-job-header { display: flex; align-items: center; padding: 20px; border-bottom: 1px solid #eee; background-color: #fff; gap: 15px; }
    .p-job-info { flex-grow: 1; display: flex; align-items: center; flex-wrap: wrap; gap: 15px; }
    .p-job-title { font-size: 1.4rem; font-weight: bold; color: #333; margin: 0; line-height: 1.2; }
    .p-job-meta { font-size: 0.9rem; color: #666; background: #eee; padding: 4px 12px; border-radius: 20px; white-space: nowrap; }

    /* カード左上選択チェックボックス＆「選択」ラベル */
    .p-job-card-select {
      display: flex;
      align-items: center;
      gap: 6px;
      background-color: #f0f5ff;
      padding: 6px 12px;
      border-radius: 20px;
      border: 1px solid #c2d7ff;
      cursor: pointer;
      user-select: none;
      transition: background-color 0.2s;
    }
    .p-job-card-select:hover {
      background-color: #e0ecff;
    }
    .p-job-card-select span {
      font-size: 0.85rem;
      font-weight: bold;
      color: #17184B;
      white-space: nowrap;
    }
    .card-checkbox { width: 18px; height: 18px; cursor: pointer; accent-color: #17184B; margin: 0; }

    /* ボタンエリア設定 */
    .p-job-btn-group { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }

    .p-job-btn a { 
      display: inline-block; 
      background-color: #fbdc00; 
      color: #17184B; 
      text-decoration: none; 
      padding: 10px 25px; 
      border-radius: 4px; 
      font-weight: bold; 
      font-size: 0.9rem; 
      transition: background 0.3s; 
      box-shadow: 0 2px 5px rgba(251, 220, 0, 0.4); 
    }
    .p-job-btn a:hover { background-color: #e5c900; }
    .p-job-btn a.disabled { background-color: #ccc; color: #888; box-shadow: none; pointer-events: none; }
    
    .p-job-block-wrap { display: flex; padding: 25px; gap: 30px; }
    .p-job-block { flex: 1; }
    .p-job-block:first-child { flex: 0 0 42%; }
    .p-job-block:last-child { flex: 1; }
    .p-job-label { font-weight: bold; color: #17184B; border-left: 4px solid #17184B; padding-left: 10px; margin-bottom: 12px; font-size: 1.1rem; }
    .p-job-list { margin: 0; padding: 0; }
    
    /* リスト項目の配置調整 */
    .p-job-list-item { display: flex; border-bottom: 1px solid #f0f0f0; padding: 10px 0; font-size: 0.95rem; line-height: 1.5; align-items: flex-start; }
    .p-job-list-item dt { width: 110px; font-weight: bold; color: #666; flex-shrink: 0; white-space: nowrap; padding-top: 2px; }
    .p-job-list-item dd { margin: 0; flex: 1; font-weight: bold; }

    /* ポートフォリオリンク */
    .p-job-portfolio-links a {
      margin-left: 8px;
    }

    /* 経験領域のタグ表示スタイル */
    .p-job-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      align-items: center;
    }
    .p-job-tag {
      display: inline-block;
      background-color: #e8f0fe; 
      color: #17184B;           
      border: 1px solid #c2d7ff; 
      border-radius: 6px;        
      padding: 3px 8px;
      font-size: 0.85rem;
      font-weight: bold;
      line-height: 1.3;
    }

    /* 「経験・スキル」テキストボックス */
    .p-job-text { 
      font-size: 0.95rem; 
      line-height: 1.8; 
      color: #444; 
      white-space: pre-wrap; 
      margin: 0; 
      background-color: #fafbfc; 
      border: 1px solid #e2e8f0; 
      border-radius: 6px; 
      padding: 12px 15px; 
      box-sizing: border-box;
      height: 350px;           
      max-height: 350px; 
      overflow-y: auto;        
    }

    /* モーダルポップアップ用CSS */
    .modal-overlay {
      position: fixed; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0,0,0,0.6); z-index: 2000;
      display: flex; align-items: center; justify-content: center;
      opacity: 0; pointer-events: none; transition: opacity 0.3s ease;
    }
    .modal-overlay.active { opacity: 1; pointer-events: auto; }
    .modal-content {
      background: #f5f7fa; width: 92%; max-width: 680px; max-height: 90vh;
      overflow-y: auto; border-radius: 8px; box-shadow: 0 5px 20px rgba(0,0,0,0.3);
      padding: 0; position: relative; border: 1px solid #ddd;
    }
    .modal-header {
      background-color: #fbdc00;
      color: #17184B;
      padding: 15px 20px;
      font-size: 1.2rem;
      font-weight: bold;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .modal-close {
      background: none;
      border: none;
      color: #17184B;
      font-size: 1.8rem;
      cursor: pointer;
    }
    
    .modal-body { padding: 25px; font-size: 0.9rem; line-height: 1.5; background: #f5f7fa; }
    
    .modal-section-title {
      font-weight: bold; color: #17184B; border-left: 4px solid #17184B;
      padding-left: 10px; margin: 25px 0 15px 0; font-size: 1.1rem;
    }
    .modal-section-title:first-child { margin-top: 0; }
    
    .form-grid { display: grid; grid-template-columns: 85px 1fr 85px 1fr; gap: 10px 10px; align-items: center; margin-bottom: 15px; }
    .form-label { font-weight: bold; color: #555; font-size: 0.85rem; }
    
    .required-mark { color: #e53e3e; font-weight: bold; margin-left: 2px; }

    /* 複数エンジニア表示コンテナ */
    .modal-multi-engineer-container {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-bottom: 15px;
    }

    .form-input,
    .form-select,
    .form-textarea {
      width: 100%;
      padding: 8px 10px;
      background-color: #ffffff !important;
      border: 1px solid #ddd;
      border-radius: 8px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.03);
      box-sizing: border-box;
      font-size: 0.9rem;
      transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .form-textarea {
      min-height: 38px;
      height: 38px;
      resize: none;
      line-height: 1.4;
      overflow-y: hidden;
    }

    .form-input:focus,
    .form-select:focus,
    .form-textarea:focus {
      outline: none;
      border-color: #17184B;
      box-shadow: 0 0 8px rgba(23, 24, 75, 0.4);
    }

    .form-full-field { margin-bottom: 15px; }
    .form-full-field .form-label { margin-bottom: 6px; display: block; }

    .schedule-row { display: flex; gap: 6px; align-items: center; margin-bottom: 8px; flex-wrap: wrap; }
    .schedule-top-group { display: flex; align-items: center; gap: 6px; justify-content: flex-start; }
    .time-range-wrap { display: flex; align-items: center; gap: 4px; flex-wrap: nowrap; }
    .time-group { display: inline-flex; align-items: center; gap: 2px; white-space: nowrap; font-size: 0.85rem; }

    input[type="date"].form-input {
      position: relative;
      cursor: pointer;
    }
    input[type="date"]::-webkit-calendar-picker-indicator {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      opacity: 0;
      cursor: pointer;
      z-index: 2;
    }

    .btn-add-schedule {
      background: #ffffff;
      border: 1px dashed #17184B;
      color: #17184B;
      padding: 8px 14px;
      border-radius: 6px;
      font-size: 0.85rem;
      font-weight: bold;
      cursor: pointer;
      transition: all 0.2s ease;
      margin-top: 4px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
    .btn-add-schedule:hover {
      background-color: #eef4ff;
      border-color: #17184B;
      color: #17184B;
    }

    .btn-remove-schedule {
      background: #ccc;
      color: #fff;
      border: none;
      border-radius: 50%;
      width: 24px;
      height: 24px;
      font-size: 0.9rem;
      font-weight: bold;
      line-height: 1;
      cursor: pointer;
      margin-left: 4px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s ease;
      flex-shrink: 0;
    }
    .btn-remove-schedule:hover {
      background: #e53e3e;
      color: #fff;
      transform: scale(1.1);
    }

    .radio-label {
      cursor: pointer;
      user-select: none;
      margin-right: 15px;
    }

    .notice-box { background: #fff3cd; border: 1px solid #ffeeba; color: #856404; padding: 12px; border-radius: 6px; margin-top: 20px; font-size: 0.82rem; line-height: 1.5; }
    
    .submit-btn {
      width: 100%; background-color: #17184B; color: white; padding: 14px; border: none;
      border-radius: 6px; font-size: 1.05rem; font-weight: bold; margin-top: 20px; cursor: pointer;
      transition: all 0.3s; box-shadow: 0 2px 5px rgba(23, 24, 75, 0.3);
    }
    .submit-btn:hover:not(:disabled) { background-color: #0d0e2e; }
    .submit-btn:disabled {
      background-color: #ccc;
      box-shadow: none;
      cursor: not-allowed;
      opacity: 0.7;
    }

    /* 画面右下の固定商談依頼フローティングボタン */
    .floating-cta-btn {
      position: fixed;
      bottom: 90px;
      right: 20px;
      background-color: #17184B;
      color: #fff;
      border: none;
      border-radius: 50px;
      padding: 14px 28px;
      font-size: 1rem;
      font-weight: bold;
      cursor: pointer;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
      z-index: 999;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.3s ease;
      opacity: 0;
      pointer-events: none;
      transform: translateY(20px);
    }
    .floating-cta-btn.visible {
      opacity: 1;
      pointer-events: auto;
      transform: translateY(0);
    }
    .floating-cta-btn:hover {
      background-color: #0d0e2e;
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    }

    /* ==========================================================================
       スマホ閲覧時の専用レイアウト切り替え
       ========================================================================== */
    @media (max-width: 768px) {
      * { -webkit-tap-highlight-color: transparent; }
      #app { overflow-x: hidden; }
      .main-content { padding: 15px 10px; }
      
      .site-header { padding: 20px 0; }
      .header-logo { position: static; text-align: center; margin-bottom: 10px; }
      .header-logo img { margin: 0 auto; }
      .header-text { padding-left: 0; text-align: center; }
      .header-title { font-size: 1.25rem; }
      .header-desc { font-size: 0.8rem; text-align: left; }
      .header-cta-btn { width: 100%; box-sizing: border-box; text-align: center; -webkit-appearance: none; }
      
      .footer-inner { flex-direction: column; gap: 20px; }
      
      .p-job-header { 
        flex-direction: column; 
        align-items: flex-start; 
        text-align: left; 
        gap: 12px; 
        padding: 15px; 
      }

      .p-job-card-select {
        align-self: flex-start;
      }

      .p-job-info { 
        justify-content: flex-start; 
        flex-direction: column; 
        align-items: center; 
        width: 100%;
        text-align: center;
        gap: 8px; 
      }
      .p-job-btn-group { width: 100%; flex-direction: column; gap: 8px; }
      .p-job-btn, .p-job-btn a { display: block; width: 100%; text-align: center; box-sizing: border-box; -webkit-appearance: none; }
      
      .p-job-block-wrap { flex-direction: column; gap: 15px; padding: 15px; }
      .p-job-block:first-child { flex: auto; }
      
      .p-job-list-item dt { width: 110px; flex-shrink: 0; }

      .p-job-text { height: 200px; max-height: 200px; }

      .floating-cta-btn { bottom: 85px; right: 15px; padding: 12px 22px; font-size: 0.9rem; }

      .tab-container {
        flex-direction: column;
        gap: 10px;
      }
      .tab-btn {
        padding: 6px 8px;
        font-size: 0.8rem;
        width: 31%;           
        min-width: 80px;
      }
      .tab-all-wrapper {
        width: 100%;
        display: flex;
        justify-content: center;
      }
      .tab-all-wrapper .tab-btn {
        width: auto;          
        min-width: 80px;
      }
      .tab-sub-wrapper {
        width: 100%;
        justify-content: space-between;
        gap: 6px;
      }

      .status-bar {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
        padding: 12px;
        font-size: 0.8rem;
      }
      .status-right-group {
        width: 100%;
        justify-content: space-between;
      }

      .modal-overlay { padding: 10px; }
      .modal-content { width: 100%; max-height: 90vh; -webkit-overflow-scrolling: touch; }
      .modal-header { position: sticky; top: 0; z-index: 10; }
      .modal-body { padding: 15px; background: #f5f7fa; }

      .form-grid { grid-template-columns: 1fr; gap: 6px; margin-bottom: 12px; }
      .form-label { margin-top: 6px; }

      .form-input,
      .form-select,
      .form-textarea {
        font-size: 14px;
        -webkit-appearance: none;
      }
      .form-textarea { height: 38px; }

      .schedule-row {
        background: #ffffff;
        padding: 10px 8px;
        border-radius: 6px;
        border: 1px solid #ddd;
        display: flex;
        flex-direction: column;
        align-items: stretch;
        gap: 8px;
      }
      .schedule-top-group {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 8px;
        width: 100%;
      }
      .schedule-row input[type="date"] {
        flex: 0.3;
        min-width: 130px;
        font-size: 14px;
        padding: 6px 8px;
      }
      .schedule-row .time-range-wrap {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        gap: 2px;
      }
      .schedule-row .time-group {
        display: flex;
        align-items: center;
        gap: 2px;
        font-size: 0.8rem;
      }
      .schedule-row .form-select {
        width: 48px !important;
        padding: 6px 2px !important;
        font-size: 14px !important;
        text-align: center;
      }
      .btn-add-schedule, .btn-remove-schedule, .submit-btn { -webkit-appearance: none; }
      .btn-remove-schedule { width: 24px; height: 24px; font-size: 1rem; margin-left: auto; }
    }
  </style>
</head>
<body>

  <div id="app">

    <header class="site-header">
      <div class="header-inner">
        <div class="header-logo">
          <img src="https://drive.google.com/file/d/1hVfG4LUnAE0woLWQYmKl6ve8hZS7xeXw/view?usp=drive_link">
        </div>
        <div class="header-text">
          <h1 class="header-title">
            株式会社キャリアデザインセンター <br>
            正社員エンジニアのご紹介
          </h1>
          <p class="header-desc">
            弊社の無期雇用（正社員）エンジニアをご紹介させていただきます。<br>
            お顔合わせ可否やその他ご質問などがございましたら、お気軽にお問合せください。<br>
            <span>※契約形態は「派遣」となります。</span>
          </p>

          <a href="https://it-partners.type.jp/business/contact/" target="_blank" class="header-cta-btn">
            お問い合わせはこちら
          </a>
        </div>
      </div>
    </header>

    <main class="main-content">

      <div id="tab-menu" class="tab-container"></div>
      <div id="filter-container" class="filter-container"></div>

      <div class="search-section">
        <input type="text" id="search-box" class="search-box" placeholder="キーワード検索（例：Java 金融 PM 1月）">
      </div>

      <!-- 利用ガイド（注意書き） -->
      <div class="usage-guide-box">
        💡 <strong>ご利用方法：</strong>ご希望のエンジニアの <strong>「選択」</strong> にチェックを入れ、画面右下の <strong>「商談依頼」ボタン</strong> からまとめてお問い合わせいただけます。
      </div>

      <!-- 動的ステータスバー -->
      <div id="status-bar" class="status-bar">
        <div class="status-condition" id="status-condition-text">条件：すべて</div>
        <div class="status-right-group">
          <button type="button" id="select-all-btn" class="select-all-btn" onclick="toggleSelectAll()">すべて選択</button>
          <div class="status-count">該当エンジニア：<span class="status-count-num" id="status-count-num">0</span> 名</div>
        </div>
      </div>

      <div id="card-list" class="card-list">
        <div class="local-loading">
          <p>データを取得しています...<br><span style="font-size:0.8rem;">※数秒お待ちください</span></p>
        </div>
      </div>

    </main>

    <!-- フッター（ヘッダーとデザイン統一） -->
    <footer class="site-footer">
      <div class="footer-inner">
        <div class="footer-section">
          <div class="footer-title">会社情報</div>
          <div class="footer-info">
            <p><strong>株式会社キャリアデザインセンター</strong></p>
            <p>〒107-0052 東京都港区赤坂3-21-20 赤坂ロングビーチビル</p>
            <p>代表取締役社長兼会長: 多田 弘實</p>
            <p>設立: 1993年7月8日</p>
            <p>営業時間：平日 9:00〜17:45</p>
            <p>労働者派遣事業派13-315344</p>
          </div>
        </div>
      </div>
      <div class="copyright">
        &copy; Career Design Center Co., Ltd. All Rights Reserved.
      </div>
    </footer>

    <button id="scroll-top-btn" class="scroll-top-btn">↑</button>

    <!-- 商談依頼 固定フローティングボタン -->
    <button id="floating-cta-btn" class="floating-cta-btn" onclick="openSelectedModal()">
      <span id="floating-btn-text">商談依頼</span>
    </button>
  </div>

  <!-- ★商談依頼モーダル -->
  <div id="request-modal" class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <span>商談依頼</span>
        <button class="modal-close" onclick="closeModal()">&times;</button>
      </div>
      <div class="modal-body">
        <form id="negotiation-form" onsubmit="handleFormSubmit(event)">
          
          <!-- 対象エンジニア情報 -->
          <div class="modal-section-title">対象エンジニア情報</div>
          
          <!-- 単一選択用グリッド表示領域 -->
          <div id="modal-single-engineer-group" class="form-grid">
            <div class="form-label">ID：</div>
            <div><input type="text" id="m-id" name="empId" class="form-input" readonly style="background:#e9ecef !important;"></div>
            <div class="form-label">ポジション：</div>
            <div><input type="text" id="m-role" name="role" class="form-input" readonly style="background:#e9ecef !important;"></div>
            
            <div class="form-label">性別：</div>
            <div><input type="text" id="m-gender" name="gender" class="form-input" readonly style="background:#e9ecef !important;"></div>
            <div class="form-label">年代：</div>
            <div><input type="text" id="m-age" name="age" class="form-input" readonly style="background:#e9ecef !important;"></div>
          </div>

          <!-- 複数選択時：人数分の入力欄（1行ずつ）を自動生成するコンテナ -->
          <div id="modal-multi-engineer-group" class="modal-multi-engineer-container" style="display: none;"></div>

          <!-- 貴社情報 -->
          <div class="modal-section-title">貴社情報</div>
          <div class="form-grid">
            <div class="form-label">貴社名<span class="required-mark">*</span>：</div>
            <div><input type="text" name="companyName" class="form-input" required></div>
            <div class="form-label">担当者名<span class="required-mark">*</span>：</div>
            <div><input type="text" name="contactName" class="form-input" required></div>
            
            <div class="form-label">会社URL<span class="required-mark">*</span>：</div>
            <div><input type="url" name="url" class="form-input" placeholder="https://" required></div>
            <div class="form-label">アドレス<span class="required-mark">*</span>：</div>
            <div><input type="email" name="email" class="form-input" placeholder="example@example.com" required></div>
          </div>

          <!-- 案件詳細 -->
          <div class="modal-section-title">案件詳細</div>
          
          <!-- 案件状況ラジオボタン -->
          <div style="margin-bottom:15px;">
            <div class="form-label" style="margin-bottom:8px;">案件状況<span class="required-mark">*</span></div>
            <div style="padding: 4px 0;">
              <label class="radio-label"><input type="radio" name="projectStatus" value="確定" onchange="handleProjectStatusChange()"> 確定</label>
              <label class="radio-label"><input type="radio" name="projectStatus" value="未定" onchange="handleProjectStatusChange()"> 未定</label>
            </div>
          </div>

          <!-- 「確定」選択時に表示するグループ -->
          <div id="project-detail-group" style="display:none;">
            <div class="form-grid">
              <div class="form-label">案件名<span class="required-mark">*</span>：</div>
              <div><input type="text" name="projectName" class="form-input" placeholder="例：〇〇システム開発"></div>
              
              <div class="form-label">就業時間<span class="required-mark">*</span>：</div>
              <div><input type="text" name="workHours" class="form-input" placeholder="例：09:00 〜 18:00（休憩1h）"></div>
              
              <div class="form-label">残業時間<span class="required-mark">*</span>：</div>
              <div><input type="text" name="overtime" class="form-input" placeholder="例：15時間/月"></div>
              
              <div class="form-label">勤務曜日<span class="required-mark">*</span>：</div>
              <div><input type="text" name="workDays" class="form-input" placeholder="例：月〜金（土日祝休み）"></div>
              
              <div class="form-label">最寄り駅<span class="required-mark">*</span>：</div>
              <div><input type="text" name="station" class="form-input" placeholder="例：新宿駅 徒歩5分"></div>
              
              <div class="form-label">働き方<span class="required-mark">*</span>：</div>
              <div><input type="text" name="workStyle" class="form-input" placeholder="例：週4 リモート"></div>
            </div>

            <div class="form-full-field">
              <div class="form-label">業務内容<span class="required-mark">*</span></div>
              <textarea name="jobDescription" class="form-textarea auto-resize" placeholder="業務の具体的な内容をご記入ください"></textarea>
            </div>

            <div class="form-full-field">
              <div class="form-label">環境・使用ツール<span class="required-mark">*</span></div>
              <textarea name="environment" class="form-textarea auto-resize" placeholder="使用する言語、DB、フレームワーク、ツール等をご記入ください"></textarea>
            </div>
          </div>

          <!-- 「その他」エリア -->
          <div class="form-full-field" id="other-notes-group" style="display:none;">
            <div class="form-label" id="other-notes-label">その他</div>
            <textarea name="otherNotes" id="other-notes-textarea" class="form-textarea auto-resize" placeholder="補足事項やその他のご要望等をご記入ください（任意）"></textarea>
          </div>

          <!-- 商談希望条件 -->
          <div class="modal-section-title">商談希望条件</div>

          <!-- 商談候補日時 -->
          <div style="margin-bottom:20px;">
            <div class="form-label" style="margin-bottom:8px;">商談候補日時</div>
            
            <div id="schedule-container">
              <div class="schedule-row" data-row-index="1">
                <div class="schedule-top-group">
                  <span class="row-num" style="font-weight:bold; min-width:25px;">1<span class="required-mark">*</span></span>
                  <input type="date" name="date1" class="form-input">
                </div>
                <div class="time-range-wrap">
                  <div class="time-group">
                    <select name="time1_start_h" class="form-select time-hour" style="width:52px;"></select>時
                    <select name="time1_start_m" class="form-select time-min" style="width:52px;"></select>分
                  </div>
                  ～
                  <div class="time-group">
                    <select name="time1_end_h" class="form-select time-hour" style="width:52px;"></select>時
                    <select name="time1_end_m" class="form-select time-min" style="width:52px;"></select>分
                  </div>
                </div>
              </div>
              
              <div class="schedule-row" data-row-index="2">
                <div class="schedule-top-group">
                  <span class="row-num" style="font-weight:bold; min-width:25px;">2</span>
                  <input type="date" name="date2" class="form-input">
                </div>
                <div class="time-range-wrap">
                  <div class="time-group">
                    <select name="time2_start_h" class="form-select time-hour" style="width:52px;"></select>時
                    <select name="time2_start_m" class="form-select time-min" style="width:52px;"></select>分
                  </div>
                  ～
                  <div class="time-group">
                    <select name="time2_end_h" class="form-select time-hour" style="width:52px;"></select>時
                    <select name="time2_end_m" class="form-select time-min" style="width:52px;"></select>分
                  </div>
                </div>
              </div>

              <div class="schedule-row" data-row-index="3">
                <div class="schedule-top-group">
                  <span class="row-num" style="font-weight:bold; min-width:25px;">3</span>
                  <input type="date" name="date3" class="form-input">
                </div>
                <div class="time-range-wrap">
                  <div class="time-group">
                    <select name="time3_start_h" class="form-select time-hour" style="width:52px;"></select>時
                    <select name="time3_start_m" class="form-select time-min" style="width:52px;"></select>分
                  </div>
                  ～
                  <div class="time-group">
                    <select name="time3_end_h" class="form-select time-hour" style="width:52px;"></select>時
                    <select name="time3_end_m" class="form-select time-min" style="width:52px;"></select>分
                  </div>
                </div>
              </div>
            </div>

            <button type="button" class="btn-add-schedule" onclick="addScheduleRow()">＋ 候補日時を追加</button>
          </div>

          <!-- 実施方法 -->
          <div style="margin-bottom:20px;">
            <div class="form-label" style="margin-bottom:8px;">実施方法<span class="required-mark">*</span></div>
            <div style="padding: 4px 0;">
              <label class="radio-label"><input type="radio" name="method" value="オンライン" onchange="handleMethodChange()"> オンライン</label>
              <label class="radio-label"><input type="radio" name="method" value="対面" id="method-offline" onchange="handleMethodChange()"> 対面</label>
              <label class="radio-label"><input type="radio" name="method" value="どちらでも可" onchange="handleMethodChange()"> どちらでも可</label>
            </div>
          </div>

          <!-- 対面・どちらでも可選択時の場所入力 -->
          <div id="method-detail-group" style="display:none; margin-bottom:20px;">
            <div class="form-label" id="method-detail-label" style="margin-bottom:8px;">場所<span class="required-mark">*</span></div>
            <input type="text" name="location" id="method-detail-input" class="form-input" placeholder="">
          </div>

          <div class="notice-box">
            派遣法により、個人を特定した商談は行っておりません。商談には参照いただいたサンプルの人材は参加できない可能性がありますことをあらかじめご了承ください。<br>
            <strong>担当者からあらためてご連絡させていただきます。</strong>
          </div>

          <button type="submit" id="submit-btn" class="submit-btn" disabled>依頼する</button>
        </form>
      </div>
    </div>
  </div>

  <script>
    // --- グローバル変数 ---
    let allEmployees = []; 
    let fieldLabels = {};  
    let groupedCategories = []; 
    let currentTab = ''; 
    let currentRole = ''; 
    let searchQuery = ''; 
    let gradesMap = {}; 
    let scheduleCount = 3; 
    let selectedEngineers = []; // 選択中のエンジニア保持用

    // --- 初期化 ---
    document.addEventListener('DOMContentLoaded', () => {
      google.script.run
        .withSuccessHandler(initApp) 
        .withFailureHandler(showError)
        .getAppDataSet();

      document.getElementById('search-box').addEventListener('input', (e) => {
        searchQuery = e.target.value;
        renderCards(); 
      });

      window.addEventListener('scroll', handleScroll);
      document.getElementById('scroll-top-btn').addEventListener('click', scrollToTabs);

      initTimeSelectOptions();
      initAutoResizeTextarea();

      const form = document.getElementById('negotiation-form');
      form.addEventListener('input', checkFormValidity);
      form.addEventListener('change', checkFormValidity);

      handleProjectStatusChange();
    });

    /* テキストエリアの入力内容に応じた自動高さ調整機能 */
    function initAutoResizeTextarea() {
      const textareas = document.querySelectorAll('textarea.auto-resize');
      textareas.forEach(textarea => {
        textarea.addEventListener('input', adjustTextareaHeight);
      });
    }

    function adjustTextareaHeight(e) {
      const el = e.target || e;
      el.style.height = '38px'; 
      if (el.value.trim() !== '') {
        el.style.height = el.scrollHeight + 'px';
      }
    }

    /* 「時（9〜20）」「分（0, 15, 30, 45）」のプルダウン選択肢生成 */
    function initTimeSelectOptions() {
      const rows = document.querySelectorAll('#schedule-container .schedule-row');
      rows.forEach(row => populateRowTimeOptions(row));
    }

    function populateRowTimeOptions(rowElement) {
      const hourSelects = rowElement.querySelectorAll('.time-hour');
      const minSelects = rowElement.querySelectorAll('.time-min');

      hourSelects.forEach(select => {
        if (select.children.length === 0) {
          select.innerHTML = '<option value="">--</option>';
          for (let h = 9; h <= 20; h++) {
            const hStr = String(h).padStart(2, '0');
            const opt = document.createElement('option');
            opt.value = hStr;
            opt.textContent = hStr;
            select.appendChild(opt);
          }
        }
      });

      minSelects.forEach(select => {
        if (select.children.length === 0) {
          select.innerHTML = '<option value="">--</option>';
          [0, 15, 30, 45].forEach(m => {
            const mStr = String(m).padStart(2, '0');
            const opt = document.createElement('option');
            opt.value = mStr;
            opt.textContent = mStr;
            select.appendChild(opt);
          });
        }
      });
    }

    /* 案件状況ラジオボタンの選択切替処理 */
    function handleProjectStatusChange() {
      const statusSelected = document.querySelector('input[name="projectStatus"]:checked');
      const detailGroup = document.getElementById('project-detail-group');
      const otherGroup = document.getElementById('other-notes-group');
      const otherLabel = document.getElementById('other-notes-label');
      const otherTextarea = document.getElementById('other-notes-textarea');

      if (!statusSelected) {
        detailGroup.style.display = 'none';
        otherGroup.style.display = 'none';
      } else if (statusSelected.value === '未定') {
        detailGroup.style.display = 'none';
        otherGroup.style.display = 'block';
        otherLabel.innerHTML = 'その他<span class="required-mark">*</span>';
        otherTextarea.placeholder = 'どんな案件を実施していくのか可能な限りご説明ください';
      } else if (statusSelected.value === '確定') {
        detailGroup.style.display = 'block';
        otherGroup.style.display = 'block';
        otherLabel.innerHTML = 'その他';
        otherTextarea.placeholder = '補足事項やその他のご要望等をご記入ください（任意）';
      }

      checkFormValidity();
    }

    // --- データ取得後の処理 ---
    function initApp(data) {
      allEmployees = data.employees || []; 
      fieldLabels = data.labels || {}; 
      gradesMap = data.grades || {}; 
      
      const groups = {};
      (data.categories || []).forEach(item => {
        const cat = item.category; 
        const role = item.role; 
        if (!groups[cat]) { groups[cat] = { name: cat, roles: [] }; }
        if (role && !groups[cat].roles.includes(role)) { groups[cat].roles.push(role); }
      });
      groupedCategories = Object.values(groups);

      groupedCategories.unshift({ name: 'すべて', roles: [] });

      if (groupedCategories.length > 0) {
        currentTab = groupedCategories[0].name;
      }

      renderTabs(); 
      renderFilters(); 
      renderCards(); 
    }

    // --- タブ描画関数（PC版：横1行 / スマホ版：2段構成） ---
    function renderTabs() {
      const container = document.getElementById('tab-menu');
      container.innerHTML = '';

      const allWrapper = document.createElement('div');
      allWrapper.className = 'tab-all-wrapper';

      const subWrapper = document.createElement('div');
      subWrapper.className = 'tab-sub-wrapper';

      groupedCategories.forEach(cat => {
        let displayName = cat.name;
        if (displayName === 'システム開発') {
          displayName = '開発';
        }

        const btn = document.createElement('button');
        btn.textContent = displayName;
        btn.className = 'tab-btn';
        if (cat.name === currentTab) btn.classList.add('active');
        
        btn.onclick = () => {
          currentTab = cat.name;
          currentRole = ''; 
          searchQuery = ''; 
          document.getElementById('search-box').value = '';   
          
          renderTabs();    
          renderFilters(); 
          renderCards();   
        };

        if (cat.name === 'すべて') {
          allWrapper.appendChild(btn);
        } else {
          subWrapper.appendChild(btn);
        }
      });

      container.appendChild(allWrapper);
      container.appendChild(subWrapper);
    }

    function renderFilters() {
      const container = document.getElementById('filter-container');
      container.innerHTML = '';

      const targetCat = groupedCategories.find(c => c.name === currentTab);
      const roles = targetCat ? targetCat.roles : [];

      const allSpan = createFilterSpan('すべて', '', currentRole === '');
      container.appendChild(allSpan);

      roles.forEach(role => {
        const span = createFilterSpan(role, role, currentRole === role);
        container.appendChild(span);
      });
    }

    function createFilterSpan(text, roleValue, isActive) {
      const span = document.createElement('span');
      span.textContent = text;
      span.className = 'filter-link';
      if (isActive) span.classList.add('active');
      
      span.onclick = () => {
        currentRole = roleValue;
        renderFilters(); 
        renderCards();   
      };
      return span;
    }

    /* 動的ステータスバーの表示更新 */
    function updateStatusBar(count) {
      const conditionTextEl = document.getElementById('status-condition-text');
      const countNumEl = document.getElementById('status-count-num');
      
      let conditions = [];
      let displayTabName = currentTab || 'すべて';
      if (displayTabName === 'システム開発') displayTabName = '開発';

      conditions.push(displayTabName);

      if (currentRole) {
        conditions.push(`職種: ${currentRole}`);
      }

      const query = searchQuery.trim();
      if (query) {
        conditions.push(`キーワード: "${query}"`);
      }

      conditionTextEl.innerHTML = `条件：${conditions.join(' / ')}`;
      countNumEl.textContent = count;
    }

    function renderCards() {
      const container = document.getElementById('card-list');
      
      const filtered = allEmployees.filter(emp => {
        if (searchQuery) {
          const query = searchQuery.toLowerCase().trim();
          const keywords = query.split(/\s+/);
          const gradeInfo = gradesMap[emp.grade] || {};
          const feeVal = gradeInfo.fee ? `${gradeInfo.fee}万` : '';

          const target = `
            ${emp.id} ${emp.department} ${emp.role} ${emp.gender} ${emp.public_age} ${emp.start_date} ${emp.experience_area} 
            ${emp.history} ${emp.detail} ${feeVal} ${emp.years}
          `.toLowerCase();
          return keywords.every(word => target.includes(word));
        }
        
        const isTabMatch = (currentTab === 'すべて' || emp.department === currentTab);
        const isRoleMatch = currentRole === '' || emp.role === currentRole;
        return isTabMatch && isRoleMatch;
      });

      // 動的ステータスバーの件数・条件を更新
      updateStatusBar(filtered.length);

      if (filtered.length === 0) {
        container.innerHTML = '<div style="text-align:center; color:#888;">該当する社員はいません。</div>';
        refreshFloatingButton();
        return;
      }

      let html = '';
      filtered.forEach(emp => {
        const pdfLink = emp.pdf_url ? emp.pdf_url : '#';
        const pdfClass = emp.pdf_url ? '' : 'disabled';
        
        const gradeInfo = gradesMap[emp.grade] || {};
        const feeVal = gradeInfo.fee || '-';

        let metaHtml = '';
        if (emp.gender || emp.public_age) {
          const gender = emp.gender ? emp.gender : undefined;
          const public_age = emp.public_age ? emp.public_age : undefined;

          const metaText = [gender, public_age]
            .filter(value => value !== undefined)
            .join(' / ');

          metaHtml = `<span class="p-job-meta">${metaText}</span>`;
        }

        let expTagsHtml = '-';
        if (emp.experience_area) {
          const tags = emp.experience_area.split(/[,、\/\n\r\s]+/);
          expTagsHtml = '<div class="p-job-tags">' + 
            tags.filter(t => t.trim() !== '')
                .map(t => `<span class="p-job-tag">${t.trim()}</span>`)
                .join('') + 
            '</div>';
        }

        const isChecked = selectedEngineers.some(e => e.id === emp.id);

        html += `
          <div class="p-job-card">
            <div class="p-job-header">
              <!-- カード左上：「選択」ラベル付きチェックボックス -->
              <label class="p-job-card-select">
                <input type="checkbox" class="card-checkbox" value="${emp.id || ''}" 
                       data-role="${emp.role || ''}" 
                       data-gender="${emp.gender || ''}" 
                       data-age="${emp.public_age || ''}" 
                       ${isChecked ? 'checked' : ''}
                       onchange="updateSelectionStatus(this)">
                <span>選択</span>
              </label>

              <div class="p-job-info">
                <h3 class="p-job-title">${fieldLabels.id || 'ID'}：${emp.id || '-'} ／ ${emp.role || ''}</h3>
                ${metaHtml}
              </div>
              <div class="p-job-btn-group">
                <div class="p-job-btn">
                  <a href="${pdfLink}" target="_blank" onclick="google.script.run.writeDisplaySkillSheetLog('${emp.id}');" class="${pdfClass}">スキルシート</a>
                </div>
              </div>
            </div>
            <div class="p-job-block-wrap">
              <div class="p-job-block">
                <div class="p-job-label">プロフィール</div>
                <dl class="p-job-list">
                  
                  <div class="p-job-list-item">
                    <dt>派遣料金：</dt>
                    <dd>${feeVal || '-'}万（140～180H）</dd>
                  </div>

                  <div class="p-job-list-item">
                    <dt>${fieldLabels.years || '経験年数'}：</dt>
                    <dd>${emp.years || '-'}</dd>
                  </div>

                  <div class="p-job-list-item">
                    <dt>${fieldLabels.experience_area || '経験領域'}：</dt>
                    <dd>${expTagsHtml}</dd>
                  </div>

                  <div class="p-job-list-item">
                    <dt>${fieldLabels.start_date || '就業可能日'}：</dt>
                    <dd>${emp.start_date || '-'}</dd>
                  </div>

                  <div class="p-job-list-item">
                    <dt>${fieldLabels.history || '就業実績'}：</dt>
                    <dd>${emp.history || '-'}</dd>
                  </div>

                  <!-- ポートフォリオ（次回改修時に使用するため保留）
                  <div class="p-job-list-item">
                    <dt>ポートフォリオ：</dt>
                    <dd class="p-job-portfolio-links">
                      <a href="#" target="_blank">社内労務管理システム</a>
                    </dd>
                  </div>
                  -->

                </dl>
              </div>
              <div class="p-job-block">
                <div class="p-job-label">経験・スキル</div>
                <p class="p-job-text">${emp.detail || ''}</p>
              </div>
            </div>
          </div>
        `;
      });
      container.innerHTML = html;
      refreshFloatingButton();
    }

    /* チェックボックスの変更イベントハンドラ */
    function updateSelectionStatus(checkboxElement) {
      if (checkboxElement) {
        const item = {
          id: checkboxElement.value,
          role: checkboxElement.dataset.role,
          gender: checkboxElement.dataset.gender,
          age: checkboxElement.dataset.age
        };

        if (checkboxElement.checked) {
          if (!selectedEngineers.some(e => e.id === item.id)) {
            selectedEngineers.push(item);
          }
        } else {
          selectedEngineers = selectedEngineers.filter(e => e.id !== item.id);
        }
      }
      refreshFloatingButton();
    }

    /* すべて選択 / すべて解除の切替機能 */
    function toggleSelectAll() {
      const visibleCheckboxes = document.querySelectorAll('.card-checkbox');
      const isAllChecked = visibleCheckboxes.length > 0 && Array.from(visibleCheckboxes).every(cb => cb.checked);

      visibleCheckboxes.forEach(cb => {
        cb.checked = !isAllChecked;
        const item = {
          id: cb.value,
          role: cb.dataset.role,
          gender: cb.dataset.gender,
          age: cb.dataset.age
        };
        if (!isAllChecked) {
          if (!selectedEngineers.some(e => e.id === item.id)) {
            selectedEngineers.push(item);
          }
        } else {
          selectedEngineers = selectedEngineers.filter(e => e.id !== item.id);
        }
      });

      refreshFloatingButton();
    }

    /* フローティングボタンおよび全選択ボタン状態更新 */
    function refreshFloatingButton() {
      const visibleCheckboxes = document.querySelectorAll('.card-checkbox');
      const selectAllBtn = document.getElementById('select-all-btn');

      if (selectAllBtn) {
        if (visibleCheckboxes.length > 0 && Array.from(visibleCheckboxes).every(cb => cb.checked)) {
          selectAllBtn.textContent = '選択を解除';
        } else {
          selectAllBtn.textContent = 'すべて選択';
        }
      }

      const btn = document.getElementById('floating-cta-btn');
      const btnText = document.getElementById('floating-btn-text');
      const count = selectedEngineers.length;

      if (count === 0) {
        btn.classList.remove('visible');
      } else {
        btnText.textContent = `商談依頼 (${count}名)`;
        btn.classList.add('visible');
      }
    }

    /* 選択中のエンジニア情報でモーダルを開く関数 */
    function openSelectedModal() {
      if (selectedEngineers.length === 0) return;
      openModalForSelectedList(selectedEngineers);
    }

    // --- モーダル・その他機能 ---
    
    /* ★単一/複数選択に応じてモーダル表示内容を動的制御（人数分の個別の入力欄を自動生成） */
    function openModalForSelectedList(list) {
      const singleGroup = document.getElementById('modal-single-engineer-group');
      const multiGroup = document.getElementById('modal-multi-engineer-group');

      if (list.length > 1) {
        // 複数選択時：エンジニアの人数分（3名なら3つ）入力欄（input）を生成
        singleGroup.style.display = 'none';
        multiGroup.style.display = 'flex';

        let html = '';
        const ids = [];
        list.forEach((item, index) => {
          ids.push(item.id || '');
          const val = `ID：${item.id || '-'}、ポジション：${item.role || '-'}、性別：${item.gender || '-'}、年代：${item.age || '-'}`;
          html += `
            <div style="width: 100%;">
              <input type="text" value="${val}" class="form-input" readonly style="background:#e9ecef !important; font-size: 0.88rem;">
            </div>
          `;
        });
        multiGroup.innerHTML = html;

        // 隠し入力値（GASフォーム送信データ用）にセット
        document.getElementById('m-id').value = ids.join(', ');
        document.getElementById('m-role').value = '複数選択';
        document.getElementById('m-gender').value = '-';
        document.getElementById('m-age').value = '-';

      } else {
        // 単一選択時：従来の2列グリッド枠表示
        singleGroup.style.display = 'grid';
        multiGroup.style.display = 'none';

        const item = list[0] || {};
        document.getElementById('m-id').value = item.id || '';
        document.getElementById('m-role').value = item.role || '';
        document.getElementById('m-gender').value = item.gender || '';
        document.getElementById('m-age').value = item.age || '';
      }

      document.getElementById('request-modal').classList.add('active');
      if (window.innerWidth <= 768) {
        document.body.style.overflow = 'hidden';
      }
      handleProjectStatusChange();
      checkFormValidity();
    }

    function closeModal() {
      document.getElementById('request-modal').classList.remove('active');
      document.body.style.overflow = '';
      document.getElementById('negotiation-form').reset();

      const textareas = document.querySelectorAll('textarea.auto-resize');
      textareas.forEach(t => t.style.height = '38px');

      document.getElementById('method-detail-group').style.display = 'none';
      
      const scheduleContainer = document.getElementById('schedule-container');
      const rows = scheduleContainer.querySelectorAll('.schedule-row');
      rows.forEach((row, index) => {
        if (index >= 3) {
          row.remove();
        }
      });
      scheduleCount = 3;
      handleProjectStatusChange();
      checkFormValidity();
    }

    /* 商談候補日時の行追加機能 */
    function addScheduleRow() {
      scheduleCount++;
      const scheduleContainer = document.getElementById('schedule-container');
      const newRow = document.createElement('div');
      newRow.className = 'schedule-row';
      newRow.dataset.rowIndex = scheduleCount;

      newRow.innerHTML = `
        <div class="schedule-top-group">
          <span class="row-num" style="font-weight:bold; min-width:25px;">${scheduleCount}&nbsp;</span>
          <input type="date" name="date${scheduleCount}" class="form-input">
          <button type="button" class="btn-remove-schedule" onclick="removeScheduleRow(this)" title="行を削除">&times;</button>
        </div>
        <div class="time-range-wrap">
          <div class="time-group">
            <select name="time${scheduleCount}_start_h" class="form-select time-hour" style="width:52px;"></select>時
            <select name="time${scheduleCount}_start_m" class="form-select time-min" style="width:52px;"></select>分
          </div>
          ～
          <div class="time-group">
            <select name="time${scheduleCount}_end_h" class="form-select time-hour" style="width:52px;"></select>時
            <select name="time${scheduleCount}_end_m" class="form-select time-min" style="width:52px;"></select>分
          </div>
        </div>
      `;
      scheduleContainer.appendChild(newRow);

      populateRowTimeOptions(newRow);
      checkFormValidity();
    }

    /* 追加された候補日時行の削除処理 */
    function removeScheduleRow(btnElement) {
      const row = btnElement.closest('.schedule-row');
      row.remove();
      reindexScheduleRows();
      checkFormValidity();
    }

    /* 行削除後に番号および name 属性を再割り当て */
    function reindexScheduleRows() {
      const rows = document.querySelectorAll('#schedule-container .schedule-row');
      scheduleCount = rows.length;
      rows.forEach((row, idx) => {
        const num = idx + 1;
        row.dataset.rowIndex = num;
        
        const numSpan = row.querySelector('.row-num');
        if (numSpan) {
          const isRequired = num <= 3;
          numSpan.innerHTML = `${num}${isRequired ? '<span class="required-mark">*</span>' : '&nbsp;'}`;
        }

        const dateInput = row.querySelector('input[type="date"]');
        if (dateInput) dateInput.name = `date${num}`;

        const hourSelects = row.querySelectorAll('.time-hour');
        const minSelects = row.querySelectorAll('.time-min');

        if (hourSelects.length >= 2) {
          hourSelects[0].name = `time${num}_start_h`;
          hourSelects[1].name = `time${num}_end_h`;
        }
        if (minSelects.length >= 2) {
          minSelects[0].name = `time${num}_start_m`;
          minSelects[1].name = `time${num}_end_m`;
        }
      });
    }

    /* 実施方法選択時の動的切り替え */
    function handleMethodChange() {
      const selected = document.querySelector('input[name="method"]:checked');
      const detailGroup = document.getElementById('method-detail-group');
      const label = document.getElementById('method-detail-label');
      const input = document.getElementById('method-detail-input');

      if (!selected) {
        detailGroup.style.display = 'none';
        return;
      }

      if (selected.value === '対面' || selected.value === 'どちらでも可') {
        detailGroup.style.display = 'block';
        label.innerHTML = '対面での実施場所（住所）<span class="required-mark">*</span>';
        input.placeholder = '対面で実施する際の住所等をご記入ください';
      } else {
        detailGroup.style.display = 'none';
        input.value = '';
      }

      checkFormValidity();
    }

    /* 全必須項目のチェック＆ボタン状態制御 */
    function checkFormValidity() {
      const form = document.getElementById('negotiation-form');
      const submitBtn = document.getElementById('submit-btn');

      // 1. 貴社情報の入力確認
      const companyName = form.companyName.value.trim();
      const contactName = form.contactName.value.trim();
      const url = form.url.value.trim();
      const email = form.email.value.trim();
      
      // 2. 案件状況および案件詳細の入力確認
      const statusSelected = form.querySelector('input[name="projectStatus"]:checked');

      let isProjectValid = false;
      if (statusSelected) {
        if (statusSelected.value === '未定') {
          // 「未定」の場合：「その他」が必須
          const otherNotes = form.otherNotes.value.trim();
          isProjectValid = (otherNotes !== '');
        } else if (statusSelected.value === '確定') {
          // 「確定」の場合：案件詳細各項目が必須
          const projectName = form.projectName.value.trim();
          const workHours = form.workHours.value.trim();
          const overtime = form.overtime.value.trim();
          const workDays = form.workDays.value.trim();
          const station = form.station.value.trim();
          const workStyle = form.workStyle.value.trim();
          const jobDescription = form.jobDescription.value.trim();
          const environment = form.environment.value.trim();

          isProjectValid = projectName !== '' && 
                           workHours !== '' && 
                           overtime !== '' && 
                           workDays !== '' && 
                           station !== '' && 
                           workStyle !== '' && 
                           jobDescription !== '' && 
                           environment !== '';
        }
      }

      // 3. 実施方法の選択確認
      const methodSelected = form.querySelector('input[name="method"]:checked');

      // 4. 実施方法が「対面」「どちらでも可」の場合の場所入力必須チェック
      let isLocationValid = true;
      if (methodSelected && (methodSelected.value === '対面' || methodSelected.value === 'どちらでも可')) {
        const locationVal = form.location ? form.location.value.trim() : '';
        isLocationValid = (locationVal !== '');
      }

      // 全必須項目チェック（※商談候補日時は活性化判定から除外）
      const isValid = companyName !== '' && 
                      contactName !== '' && 
                      url !== '' && 
                      email !== '' && 
                      statusSelected !== null &&
                      isProjectValid && 
                      methodSelected !== null &&
                      isLocationValid;

      submitBtn.disabled = !isValid;
    }

    function handleFormSubmit(e) {
      e.preventDefault();
      const btn = document.getElementById('submit-btn');
      btn.disabled = true;
      btn.textContent = '送信中...';

      const formData = new FormData(e.target);
      const data = {};
      
      formData.forEach((value, key) => {
        data[key] = value;
      });

      google.script.run
        .withSuccessHandler(() => {
          alert('商談依頼を送信しました。担当者よりご連絡いたします。');
          btn.textContent = '依頼する';
          closeModal();
        })
        .withFailureHandler((err) => {
          alert('送信に失敗しました: ' + err.message);
          btn.disabled = false;
          btn.textContent = '依頼する';
        })
        .sendNegotiationRequest(data);
    }

    function handleScroll() {
      const btn = document.getElementById('scroll-top-btn');
      if (window.scrollY > 300) {
        btn.classList.add('visible');
      } else {
        btn.classList.remove('visible');
      }
    }

    function scrollToTabs() {
      const element = document.getElementById('tab-menu');
      if (element) {
        const y = element.getBoundingClientRect().top + window.pageYOffset - 80;
        window.scrollTo({top: y, behavior: 'smooth'});
      }
    }

    function showError(err) {
      const userMessage = `
        <div style="text-align:center; padding:40px; color:#666;">
          <h3 style="color:#F58220; margin-bottom:10px;">システムエラーが発生しました</h3>
          <p>申し訳ありませんが、データ読み込みに失敗しました。</p>
          <p style="font-size:0.85rem; color:#888;">${err ? err.message : ''}</p>
        </div>
      `;
      document.getElementById('card-list').innerHTML = userMessage;
    }
  </script>
</body>
</html>
