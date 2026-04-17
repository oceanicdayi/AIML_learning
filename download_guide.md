# 雲端硬碟檔案下載指引

## 來源連結
https://drive.google.com/drive/folders/1clBHKBIUBhP1jcvDN3tgtfQ7N0NuGuMb

## 方法一：手動下載（最簡單）

1. 開啟上方 Google Drive 連結
2. 對照下方分組對應表，將 PDF 簡報下載至對應的 `raw_data/` 資料夾
3. 若雲端硬碟已有分組子資料夾，直接對資料夾右鍵 → 下載（會自動打包為 ZIP）

### 分組對應表

| 分組 | 主題 | 時段 | 資料夾路徑 |
|------|------|------|-----------|
| Group1 | 天氣與氣候預報模型開發 | 4/20 AM | `Group1_Weather_Climate_Prediction/raw_data/` |
| Group2 | 海象與氣候應用技術 | 4/20 AM | `Group2_Marine_Climate_Tech/raw_data/` |
| Group3 | 天氣預報與預警應用技術 | 4/20 PM | `Group3_Warning_Forecasting/raw_data/` |
| Group4 | 地震預警應用技術 | 4/20 PM | `Group4_Earthquake_Warning/raw_data/` |
| Group5 | 天氣監測與應用技術 | 4/21 AM | `Group5_Weather_Monitoring/raw_data/` |
| Group7 | 資訊系統與開源環境 | 4/21 AM | `Group7_IT_OpenSource/raw_data/` |
| Group8 | 人工智慧技術人才培育 | 4/21 PM | `Group8_AI_Talent_Cultivation/raw_data/` |
| Group9 | 資料整集與重建 | 4/21 PM | `Group9_Data_Integration_Reconstruction/raw_data/` |

## 方法二：使用 gdown（Python 自動下載）

### 安裝
```bash
pip install gdown
```

### 下載整個資料夾
```bash
gdown --folder "https://drive.google.com/drive/folders/1clBHKBIUBhP1jcvDN3tgtfQ7N0NuGuMb" -O ./downloads
```

> **注意**：若資料夾為「僅限查看」而非公開，gdown 可能無法下載，需改用方法一。

### 下載後分類腳本
下載完成後，執行 `scripts/sort_downloads.py` 將檔案依關鍵字自動歸類。

## 方法三：使用 rclone（進階）

適合需要同步大量檔案的情境：
```bash
# 1. 安裝 rclone: https://rclone.org/install/
# 2. 設定 Google Drive remote
rclone config

# 3. 同步資料夾
rclone copy gdrive:"AI教育訓練簡報" ./downloads --progress
```

## 下載完成後

確認每個 `raw_data/` 資料夾內至少有對應的 PDF 檔案，即可進入 Phase 2（深度分析與 Markdown 轉譯）。
