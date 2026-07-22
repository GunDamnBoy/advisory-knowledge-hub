# AGENT BRIEF — 每日重生內容標準作業說明

這份文件是每日排程工作階段重生 `index.html` 時遵循的標準說明。目標：產出一份當日投顧知識庫儀表板，維持既有版面與風格，只更新內容。

## 觸發與時區

- 每個**交易日**（週一至週五）早上 **07:30（台北，UTC+8）** 執行。
- 對應 UTC cron：`30 23 * * 0-4`（UTC 週日至週四 23:30 = 台北週一至週五 07:30）。

## 涵蓋範圍（分頁與分區）

1. **每日總覽**：一分鐘總覽（3 個焦點卡＋5 條 takeaways）、本週重點盯盤時程。
2. **市場總經**：美股與美國總經、台股、全球央行與總經。
3. **產業與主題**：AI、科技、金融、生技、原物料。
4. **政經**：地緣政治、美國政治。
5. **關於與方法**：來源、合規、限制、規劃（大致固定，日期需更新）。

## 來源優先序

主要來源共 13 家（對應徽章）：

- **付費訂閱（使用者本人，登入瀏覽器讀）**：Bloomberg `b-bbg`、WSJ `b-wsj`、NYT `b-nyt`、FT `b-ft`、Nikkei Asia `b-nikkei`、Washington Post `b-wapo`、Barron's `b-barrons`、IBD `b-ibd`。
- **免費公開**：CNBC `b-cnbc`、MarketWatch `b-mw`、Tom's Hardware `b-toms`、Oil & Gas Journal `b-ogj`、華爾街見聞 `b-wscn`（wallstreetcn.com）。
- **公開／官方補充** `b-pub`：Reuters 體系、CBS、AP、官方央行／交易所／公司 IR、政府與司法機構公告。

各來源擅長領域（供分區取材參考）：Nikkei＝亞洲供應鏈／匯率；Tom's Hardware＝半導體/GPU/資料中心；OGJ＝油氣/LNG（原物料）；MarketWatch/IBD/Barron's＝美股與選股視角；WaPo＝美政治/地緣；CNBC＝即時盤勢與全球；華爾街見聞＝中文彙整西方財經。

### 模式差異

- **每日自動版（無瀏覽器）**：以免費公開來源（CNBC、MarketWatch、Tom's Hardware、OGJ、華爾街見聞）＋WebSearch 跨源彙整。**不得**嘗試繞過付費牆或反爬蟲。
- **加強版（使用者在場、Chrome 已登入）**：可透過 Claude in Chrome，在使用者已登入的分頁讀取其本人訂閱 8 家（Bloomberg／WSJ／NYT／FT／Nikkei／WaPo／Barron's／IBD）的全文重點。

## 合規紅線（必守）

- 不使用任何繞過付費牆／反爬蟲手段。
- 公開頁面只放**原創重點摘要＋原文連結**，不轉載付費文章全文（勿逐字複製大段內容）。
- 財務數字（單季獲利、募資／併購金額等）盡量以官方 IR 或多來源交叉為準；不確定者標註。

## 每則卡片格式

- 來源徽章（`b-bbg` / `b-wsj` / `b-nyt` / `b-ft` / `b-wscn` / `b-pub`）＋主題標籤＋日期。
- 標題（繁體中文，台灣用語）。
- 2～3 條重點摘要（bullet），濃縮到投顧一眼看懂；地緣／政策類點出對市場影響。
- 溫度色條：`t-green`（正向）/ `t-yellow`（留意）/ `t-orange`（警戒）/ `t-red`（高風險）。
- 來源連結 `href` 指向可點的原文（FT 若無單篇連結，暫連對應版面）。

## 產出

- 只改 `index.html` 的內容與最上方「最後更新」時間戳；保留 CSS、版面結構與互動邏輯。
- commit（訊息如 `chore: daily refresh YYYY-MM-DD`）後推送至 `main`，由 Actions 自動部署。

## 語氣

- 繁體中文（台灣慣用語）、精簡、可快速掃讀；面向投顧專業讀者。
