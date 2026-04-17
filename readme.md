# 氣象署 AI 應用學習與自動化知識轉化計畫 (CWA-AI-Knowledge-Hub)

## 0. 專案目標與 Agent 身分
你是一個專業的氣象技術研究助手與前端工程師。你的任務是協助氣象署新進同仁，將 4/20-4/21 為期兩天的「AI 技術應用課程」內容，從原始簡報自動化轉化為深度的知識庫與互動式網頁。

### 核心原則：
- **知識不丟失**：嚴格保留氣象、地震、海象等專業領域知識 (Domain Knowledge)。
- **自動化優先**：利用 Python 腳本或 Node.js 處理檔案與下載。
- **視覺化呈現**：將複雜流程圖轉譯為 Mermaid.js 或互動式 HTML 元件。

---

## 1. 課程時程與資料來源
- **來源連結**：https://drive.google.com/drive/folders/1clBHKBIUBhP1jcvDN3tgtfQ7N0NuGuMb
- **分組目錄規劃**：
    1. `Group1_Weather_Climate_Prediction`: 天氣與氣候預報模型開發 (4/20 AM)
    2. `Group2_Marine_Climate_Tech`: 海象與氣候應用技術 (4/20 AM)
    3. `Group3_Warning_Forecasting`: 天氣預報與預警應用技術 (4/20 PM)
    4. `Group4_Earthquake_Warning`: 地震預警應用技術 (4/20 PM)
    5. `Group5_Weather_Monitoring`: 天氣監測與應用技術 (4/21 AM)
    6. `Group7_IT_OpenSource`: 資訊系統與開源環境 (4/21 AM)
    7. `Group8_AI_Talent_Cultivation`: 人工智慧技術人才培育 (4/21 PM)
    8. `Group9_Data_Integration_Reconstruction`: 資料整集與重建 (4/21 PM)

---

## 2. 執行工作計畫 (Phase-by-Phase)

### Phase 1: 檔案初始化與獲取
- [ ] 建立上述 8 個分組資料夾。
- [ ] 寫入一個下載腳本或指引，將雲端硬碟的 PDF 分別歸類至對應資料夾。
- [ ] 確保每個資料夾內有 `raw_data/` 存放原始簡報。

### Phase 2: 深度分析與 Markdown 轉譯
- [ ] 逐一解析 PDF 內容（使用 Vision 模型或 PDF 解析工具）。
- [ ] 輸出為 `knowledge.md`，結構需包含：
    - 主題與講者
    - 氣象業務場景 (Business Context)
    - 應用的 AI 模型與技術細節 (如 CNN, Transformer, LSTM 等)
    - 資料來源與預處理方法
    - 關鍵專有名詞解釋 (Glossary)
- **要求**：內容需詳盡，不可省略公式或專業術語。

### Phase 3: 製作互動式網頁 (HTML)
- [ ] 針對每個 Markdown 檔案，生成一個獨立的 `index.html`。
- [ ] **設計規範**：
    - 使用 Tailwind CSS 進行現代化排版。
    - 整合 Mermaid.js 繪製技術流程圖。
    - 加入「重點提示」與「隱藏/展開」元件增加互動性。
    - 使用 Dark Mode 風格，符合氣象署專業形象。

### Phase 4: 彙整門戶 (Portal Dashboard)
- [ ] 在根目錄製作 `main.html`。
- [ ] 採用學習地圖 (Learning Map) 或時間軸形式，連結至所有分組的 HTML 頁面。
- [ ] 加入全站搜尋功能（基於生成的 Markdown 內容）。

### Phase 5: 打包與部署
- [ ] 準備 `.github/workflows` 以進行 GitHub Pages 部署。
- [ ] 準備 Dockerfile 或 Space 配置以進行 Hugging Face 部署。

---

## 3. Agent 執行指令 (SOP)

當我要求你開始某個分組的任務時，請遵循：
1. **分析**：先列出該分組簡報的目錄與大綱。
2. **撰寫**：產出 Markdown，詢問我是否有需要補充的專業細節。
3. **渲染**：生成 HTML，並提供預覽或代碼說明。
4. **檢查**：確認鏈接與圖片路徑正確。

---

## 4. 補充任務 (AI 增強)
- **術語卡片**：自動生成該課程的 Anki 格式術語 CSV。
- **總結報告**：在所有課程完成後，產出一份「氣象署 AI 技術地圖」總結報告。