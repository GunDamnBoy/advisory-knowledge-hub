# 投顧知識庫儀表板 · Investment Advisory Knowledge Hub

為投顧從業人員設計的每日知識庫儀表板，把分散在各大財經媒體的重點濃縮成可快速瀏覽的單頁網站，涵蓋美股與美國總經、台股與亞太、全球央行，AI／半導體、金融併購、能源原物料等產業主題，以及地緣政治與美國政治。

**線上版**：<https://gundamnboy.github.io/advisory-knowledge-hub/>

## 主要來源（15 家）

- **付費訂閱**（使用者本人正式訂閱，於自己登入的瀏覽器中合法存取）：Bloomberg、WSJ 華爾街日報、NYT 紐約時報、FT 金融時報、Nikkei Asia 日經亞洲、Washington Post、Barron's、IBD 投資人商報、Politico、The Hill
- **免費公開**：CNBC、MarketWatch、Tom's Hardware、Oil & Gas Journal、華爾街見聞
- 公開／官方補充：Reuters 體系、CBS、AP、官方央行／交易所／公司 IR、政府與司法機構公告等

## 合規原則

- **不使用任何繞過付費牆或反爬蟲的手段**；付費內容一律以使用者本人訂閱、在其登入環境下閱讀，亦不使用 archive 鏡像站或快取。
- 公開頁面僅呈現**原創的重點摘要 ＋ 原文連結**，不轉載付費文章全文，以尊重來源方著作權與使用者訂閱權益。

## 更新與封存

| 項目 | 內容 |
|------|------|
| **頻率** | **一週七天，每天台北時間 07:30** 自動更新（排程任務 `advisory-dashboard-daily`） |
| **執行機器** | 家中 MacBook Pro（24 小時開機），需 Claude 桌面版開啟、Chrome 外掛已連線且付費站台維持登入 |
| **單日時效** | 每一天的版本只保留**最近 3 個日期**的卡片，當日新卡佔全站 1/4～1/3，每個子類別 ≥10 則 |
| **歷史封存** | **每天的版本永久保留**，用頁面最上方的日期切換列可回看任何一天；不設汰除 |

- **內容產生**：排程的 Claude 工作階段依 `AGENT_BRIEF.md` 產出 `data/YYYY-MM-DD.json`，並把當天加進 `data/index.json`。
- **發布**：本機 launchd（`com.kenny.dashpush`，每 180 秒）自動 commit 並 push；GitHub Actions 再自動部署到 GitHub Pages。

## 檔案結構

```
.
├── index.html                    # 單頁應用外殼：CSS ＋ 渲染邏輯 ＋ 日期切換列（約 23KB）
├── data/
│   ├── index.json                # 封存索引（days 陣列，由新到舊）
│   ├── 2026-08-02.json           # 每日內容，一天一檔，永久保留
│   └── 2026-07-30.json
├── AGENT_BRIEF.md                # 每日產出的完整規格（含 JSON schema）
├── README.md
└── .github/workflows/deploy.yml  # GitHub Pages 自動部署
```

> **本機開啟注意**：`index.html` 需要用 `fetch()` 讀 `data/*.json`，直接用 `file://` 開會被瀏覽器的安全性限制擋掉。請改用線上版，或在資料夾內執行 `python3 -m http.server` 後以 `localhost` 瀏覽。

## 免責聲明

本儀表板為新聞彙整與研究輔助工具，**非投資建議**。摘要為濃縮版本，可能遺漏原文細節或有時間落差；數字引用前建議回查官方來源。地緣與市場變數方向可能快速反轉，請以最新一則與原始來源為準。
