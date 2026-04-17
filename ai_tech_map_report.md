# 氣象署 AI 技術地圖：總結報告

> 115 年新進人員教育訓練・7 組課程全景彙整  
> 自動產生日期：2025-07

---

## 一、全局概覽

中央氣象署（CWA）的 AI 技術布局已涵蓋**預報模型、觀測監測、地震預警、資訊基礎設施、人才培育**五大領域，形成從基礎研究到作業化部署的完整價值鏈。本報告基於 7 個分組共 130+ 頁投影片的知識萃取結果，描繪 CWA AI 技術全景。

---

## 二、技術領域與核心模型

### 2.1 天氣與氣候預報（分組一、三）

| 方向 | 關鍵技術 | 現況 |
|------|----------|------|
| 全球 MLWP | Pangu-Weather, GraphCast, GenCast, FourCastNet, NeuralGCM, Aurora | 6 模型已整合評估、颱風路徑優於 NWP |
| 颱風 AI | DLTC, TCSA, 18 模型整合 | 24h 路徑誤差年減 12%，優於 JTWC/JMA 13-16% |
| 即時預報 QPN | MIMQPN, DeepQPF, Nested-Unet, Swin-Transformer | 0-6 小時降水預報作業化 |
| 後處理 | GAN/Transformer 偏差校正、25km→5km 降尺度 | WEPS-AI 系統運行中 |

**CWA 策略**：雙軌並行——應用開源 MLWP + 自主開發區域模型。AI 定位為「預報員的計算輔助工具」，非取代。

### 2.2 海象與氣候應用（分組二）

| 方向 | 關鍵技術 | 現況 |
|------|----------|------|
| 季節氣候 | BMA 多模型整合 | 作業化 |
| AI 降尺度 | CorrDiff (NVIDIA 合作) | 25km→2km，開發中 |
| 高解析資料 | TReAD (2km/45yr), TaiSA (1km/25yr) | 已發布 |
| 異常波浪 | YOLO 影像辨識 + ANN/RF/SVM/LSTM | 21 站監測、高風險命中率 >90% |

### 2.3 地震預警（分組四）

| 方向 | 關鍵技術 | 現況 |
|------|----------|------|
| 波相辨識 | AI Phase Picking (P/S 波) | 已達上線水準 |
| 震度預估 | 物理約束 ML | ±1 級準確率 92% (2024/11 甲仙 M5.4) |
| 未來部署 | 邊緣運算 (Edge Computing) | 規劃中，降低傳輸延遲 |

**核心觀測網**：CWBSN + TSMIP ≈ 550 站。

### 2.4 天氣監測（分組五）

| 觀測源 | AI 應用 | 模型 |
|--------|---------|------|
| 雷達 | 對流胞追蹤、回波外推 | 3D CNN, Residual Diffusion |
| 衛星 | 降水估計、颱風中心定位 | MOE + Continual Learning, Uncertainty DL |
| 日射量 | 0-6h 日射量即時預報 | DGMR, GAN, Diffusion |
| 地面 | 低能見度辨識 | Sobel 邊緣檢測, SLOMO 插幀 |

### 2.5 HPC 基礎設施（分組七）

| 規格 | 數值 |
|------|------|
| CPU | 5,760× A64FX (Arm, 7nm) → 10 PFlops |
| GPU | 192× NVIDIA A100 → 2 PFlops |
| 總算力 | 12 PFlops |
| 儲存 | 10 PB (NVMe → Cache → HDD 分層) |
| 網路 | InfiniBand 200G + TofuD 6D Mesh/Torus |
| 散熱 | 浸沒式液冷 → 低 PUE、低噪音 |

### 2.6 人才培育（分組八）

**五站式學習旅程**：

```
Station 1 (AI 基礎) → Station 2 (CNN 實作) → Station 3 (U-Net/GAN) → Station 4 (Transformer/DWP) → Station 5 (雲端推論/FCNv2)
```

**三種角色定位**：規劃者 → 應用者 → 開發者

**關鍵指標**：課程滿意度 100%、講師滿意度 94%

**115 年展望**：AI 資源池上線、LLM 整合、AI-Ready 觀測資料建構

---

## 三、跨組技術堆疊

### 3.1 模型架構分布

```
Transformer 家族 ─── Swin-Transformer (分組三) / Vision Transformer (分組一)
CNN 家族 ────────── 3D CNN (分組五) / U-Net & Nested-Unet (分組三/八)
GAN 家族 ────────── DGMR (分組五) / 偏差校正 GAN (分組三)
Diffusion 家族 ──── CorrDiff (分組二) / Residual Diffusion (分組五) / GenCast (分組一)
RNN 家族 ────────── ConvLSTM / trajGRU (分組五) / LSTM (分組二)
GNN 家族 ────────── GraphCast (分組一)
統計集成 ────────── BMA (分組二) / MOE (分組五)
```

### 3.2 資料流全景

```
觀測 (雷達/衛星/地面/地震)
  ↓ 品質控制 + 前處理
再分析場 (ERA5, TReAD, TaiSA)
  ↓ AI 訓練
MLWP / AI 模型
  ↓ 後處理 + 降尺度
作業化預報 / 預警產品
  ↓ 邊緣部署 / 雲端推論
終端使用者 (預報員 / 公眾 / 決策者)
```

---

## 四、技術成熟度評估

| 技術 | TRL* | 狀態 |
|------|------|------|
| AI 颱風路徑整合預報 | 8-9 | 🟢 作業化 |
| QPN 定量降水即時預報 | 7-8 | 🟢 作業化 |
| BMA 季節氣候預報 | 8-9 | 🟢 作業化 |
| 異常波浪 YOLO 監測 | 7-8 | 🟢 作業化 |
| AI 波相辨識 (P/S 波) | 7 | 🟡 準作業 |
| DGMR 日射量預報 | 6-7 | 🟡 實驗 |
| CorrDiff AI 降尺度 | 5-6 | 🟡 開發中 |
| 全球 MLWP 評估 | 6-7 | 🟡 評估中 |
| 邊緣運算地震預警 | 4-5 | 🔵 規劃中 |
| AI-Ready 觀測資料 | 3-4 | 🔵 規劃中 |
| LLM 整合應用 | 2-3 | 🔵 探索中 |

*TRL = Technology Readiness Level (1-9)

---

## 五、戰略觀察

1. **MLWP 是最大機遇**：全球 AI 天氣模型（Pangu、GraphCast、GenCast）展現與 NWP 互補甚至超越的潛力，CWA 應持續深化區域化。
2. **Diffusion Model 成為新主力**：已橫跨降尺度 (CorrDiff)、即時預報 (Residual Diffusion)、系集預報 (GenCast) 三大場景。
3. **NVIDIA 合作是關鍵槓桿**：CorrDiff 合作案若成功，可建立 CWA 在東亞區域 AI 降尺度的技術領先地位。
4. **邊緣運算是下一步**：地震預警的 Edge Computing 部署將是 CWA 首個端側 AI 應用案例。
5. **人才缺口仍待關注**：五站式培訓建立了良好基礎，但從 100% 滿意度到實際產出模型仍需持續投入。
6. **HPC 是底層基石**：12 PFlops 算力為所有 AI 訓練提供保障，A100 GPU 是 MLWP 本地化的關鍵。

---

## 六、建議下一步

| 優先級 | 事項 | 相關分組 |
|--------|------|----------|
| P0 | 建立 MLWP 模型作業化 SOP，定義 AI 預報納入作業流程的標準 | 一、三 |
| P0 | 完成 AI 波相辨識上線部署 | 四 |
| P1 | 推進 CorrDiff 降尺度至 TRL 7+ | 二 |
| P1 | 擴大 MOE + Continual Learning 衛星降水應用 | 五 |
| P2 | 啟動邊緣運算 PoC（地震站 AI 晶片選型） | 四 |
| P2 | 建構 AI-Ready 觀測資料管線 | 八 |
| P3 | 探索 LLM 在氣象文字產品生成的應用 | 八 |

---

*本報告由 CWA AI Knowledge Hub 自動生成，基於 115 年教育訓練 7 組簡報的知識萃取結果。*
