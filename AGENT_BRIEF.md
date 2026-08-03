# AGENT BRIEF — 投顧知識庫儀表板・每日重生標準說明

這份文件是「投顧知識庫儀表板」的完整規格。任何一個新的 Cowork 對話（或換裝置）讀了這份，就能完整重現整套系統。使用者說「**跑今天的儀表板**」時，即依本文件執行。全程使用繁體中文（台灣用語），讀者為投顧從業人員。

---

## 0. 觸發與環境前提（重要）

- **執行機器＝家中的 MacBook Pro（使用者名稱 `kenny`）**，該機 24 小時開機，**一週七天每日更新（含週六日與國定假日）**。辦公室那台已停用（launchd 代理已 unload），不再作為發布機器。
- **固定排程：每天台北時間 07:30**，排程任務 ID＝`advisory-dashboard-daily`。刻意與 09:00 的 `podcast-digest-daily` 錯開，避免兩個任務搶 Chrome。
- 執行前提：**該台 Mac 醒著、Claude 桌面版開著、`advisory-knowledge-hub` 已加入連線資料夾、Chrome 外掛已連線且各付費站台維持登入狀態。**
- 讀付費訂閱要靠 Claude in Chrome 附著於對話；若該次執行連不到瀏覽器，只能以免費公開來源產出，並在「關於與方法」註明本次未涵蓋付費來源。
- 觸發方式有二：(a) 使用者在互動對話說「跑今天的儀表板」；(b) 每日 07:30 排程自動觸發（排程開的是**全新對話、沒有任何記憶**，所以一切以本文件為準）。
- **週末與清淡日不得跳過。** 新聞量少時改用第 3 節的「前瞻／最新一次」框架把版面補滿，並在心得中誠實說明當日是清淡日；**絕不可為了湊數而放舊聞或編造內容**。

---

## 1. 主要來源（19 家，付費為主體、免費為輔）

**付費訂閱**（使用者本人訂閱，於其已登入的 Chrome 讀）：
Bloomberg (bloomberg.com/asia)、WSJ (wsj.com)、NYT (nytimes.com/international)、FT (ft.com)、Nikkei Asia (asia.nikkei.com)、Washington Post (washingtonpost.com)、Barron's (barrons.com)、IBD (investors.com)、**Politico (politico.com)**、**The Hill (thehill.com)**

**免費公開**：
**Reuters (reuters.com)**、CNBC (cnbc.com/world)、MarketWatch (marketwatch.com)、Tom's Hardware (tomshardware.com)、Oil & Gas Journal (ogj.com)、華爾街見聞 (wallstreetcn.com)、**鉅亨網 Anue (news.cnyes.com)**、**MoneyDJ (moneydj.com)**

**官方／數據源**：**TWSE 台灣證券交易所與公開資訊觀測站 (twse.com.tw / mops.twse.com.tw)**、Fed／BOJ／ECB／日本財務省、EIA、CME FedWatch、美國財政部、公司 IR、政府與司法機構公告；另有 AP、CBS 等通訊社。

**Politico 與 The Hill 專供政經分頁**（地緣政治＋美國政治）的深度與時效——國會立法、國防／撥款、選舉、司法與 Fed 獨立性等。

來源徽章 class：`b-bbg`/`b-wsj`/`b-nyt`/`b-ft`/`b-nikkei`/`b-wapo`/`b-barrons`/`b-cnbc`/`b-ibd`/`b-mw`/`b-toms`/`b-ogj`/`b-politico`/`b-thehill`/`b-wscn`/`b-reuters`/`b-anue`/`b-moneydj`/`b-twse`/`b-pub`。
（卡片 `src` 值＝去掉 `b-` 前綴：`bbg`、`wsj`、…、`reuters`、`anue`、`moneydj`、`twse`、`pub`。`pub` 保留給上列以外的通訊社與官方公告，**Reuters 一律用 `reuters` 而非 `pub`**。）

各來源擅長：Bloomberg＝全球即時＋亞洲；WSJ／NYT＝美國政經；FT＝全球／科技／市場；Nikkei＝亞洲供應鏈／匯率；WaPo＝美政治／地緣；Barron's／IBD／MarketWatch＝美股與選股視角；Tom's Hardware＝半導體/GPU/資料中心；OGJ＝油氣/LNG；華爾街見聞＝中文彙整西方財經＋亞洲；**Reuters＝亞洲時區最快、官方聲明與 Kpler／LSEG 數據的一手轉述、無付費牆摩擦**；**鉅亨網＝台股盤勢與台灣本地財經**；**MoneyDJ＝台廠供應鏈與個股拆解**；**TWSE／公開資訊觀測站＝月營收、三大法人買賣超、融資餘額、法說會行事曆等官方數據**。

**內容優先序**：每個分區以付費來源卡片打底、排前面；免費來源只補付費沒涵蓋到的角度。**核可的免費來源僅限**上列八家＋官方／數據源／通訊社；**嚴禁**內容農場或小報（Motley Fool、ETtoday、Intellectia、內容聚合站等）。

### 1.1 讀取方法與付費牆判斷（2026/08/03 修訂，很重要）

**不要用導覽列有沒有「Sign In」來判斷能不能讀。** 這是錯的判準，2026/08/03 那一輪就是因此誤判。實測：Bloomberg 與 Barron's 的導覽列**永遠**顯示 Sign In／Subscribe Now，但文章內文照樣完整載入。

**正確的判斷方式——用實際取到的內文量：**

1. `navigate` 之後**先等 3–5 秒**讓 SPA 完成渲染，不要立刻讀。
2. **主要讀法是 `javascript_tool`**，抓 `article p` 這類選擇器並過濾掉短句：
   ```js
   await new Promise(r=>setTimeout(r,4000));
   const paras=[...document.querySelectorAll('article p, main p, [class*="ArticleBody"] p, [class*="body-content"] p')]
     .map(p=>p.innerText.trim()).filter(x=>x.length>60);
   JSON.stringify({n:paras.length, chars:paras.join(' ').length, text:paras.join('\n')});
   ```
3. **判定標準**：段落數 ≥8 且內文字數 ≥1,500 → 視為完整取得，正常成卡。
   段落數 ≤3 或內文字數 <800，**且**頁面出現明確的攔截字串（Barron's 的 "Continue reading this article with a Barron's subscription"、WSJ 的訂閱牆元件）→ 才算真的被擋。
4. **`get_page_text` 在 Bloomberg、Barron's、MarketWatch 上會嚴重低估內文**（只回傳前 1–3 段或側欄）。它只適合當快速掃標題用，**不可以拿它的結果來斷定文章被付費牆擋住**。

**Barron's 與 IBD 的規則**：依上述標準實測後再決定。**確認被擋才**停止逐篇嘗試、只取首頁公開資訊且不單獨成卡，並在 `run` 欄記錄。**可正常讀取時，Barron's 讀 6–8 篇、IBD 讀 4–6 篇**——這兩家的美股選股與週展望視角是其他來源沒有的，不要輕易放棄。

---

## 2. 合規紅線（必守）

- 只讀使用者本人訂閱、在其登入的 Chrome 中合法存取的付費內容；以及免費公開來源。
- **絕不使用任何繞過付費牆或反爬蟲的手段。**
- 公開頁面只放「原創重點摘要＋原文連結」，不轉載付費文章全文或逐字複製大段內容。
- 財務數字（單季獲利、資本支出、募資／併購金額、即時報價漲跌）盡量以官方或多來源交叉；不確定者標註。

---

## 3. 時效性與歷史封存

本儀表板為**日更（一週七天）**，使用者最重視的就是「每天打開都看到最新資訊」。

**核心規則：每一天的版本，全站只保留最近 3 個日期（約當日與前兩日）的卡片。** 例如 7/28 這一版，全站日期只會出現 7/26、7/27、7/28。

**重要：這條規則只約束「單一天的版本內部」，不是刪除歷史。** 自 2026/08/02 起改為封存制——**每天的版本都獨立存成 `data/YYYY-MM-DD.json` 永久保留**，使用者可用頁面最上方的日期切換列回看任何一天。**絕對不要刪除或覆寫舊的日期檔**，也不要為了「汰舊」去動 `data/` 裡前幾天的 JSON。每天要做的是**新增一個檔案**，不是改寫昨天的檔案。

- **超過 3 個日期的卡片一律處理掉**：能用當日最新進度改寫的就改寫（換新來源、換新標題、更新數字），改寫不了的就直接刪除，不留在頁面上。
- **每日新增量**：當日新卡片至少佔全站的 1/4～1/3（近期實務約 **35～45 則**），確保「今天」是版面主角，不是靠舊卡撐版面。
- **刪完仍要守版面下限**：每個子類別 ≥10 則的規定優先——先補齊當日新內容，再刪舊卡，不可為了汰舊讓子類別掉到 10 則以下。
- **結構性事件用「前瞻／最新一次」框架**：CPI、非農、FOMC／ECB／BOJ 決議等本來就是低頻事件，不可直接引用一兩個月前的舊會議當新聞；要改寫成「下次會議前瞻」或「最新一次決議＋至今的市場反應」，日期掛在寫作當日。
- **日期一律標於每張卡片**（卡片 dict 的 `date` 欄），發布前用日期直方圖檢查一次，確認只剩 3 個日期。
- 「關於與方法」分頁的時效性說明要同步寫出本次保留的日期區間。

---

## 3.5 封存架構（2026/08/02 起）

`index.html` 已改為**讀 JSON 的單頁應用**，內容與外殼分離。每天產出的是資料檔，不是 HTML。

```
index.html            # 外殼：CSS ＋ 渲染邏輯 ＋ 日期切換列（約 23KB，很少需要改）
data/index.json       # 封存索引：days 陣列，由新到舊
data/2026-08-02.json  # 每日內容，一天一個檔，永久保留
data/2026-07-30.json
```

**`data/index.json`**：

```json
{ "updated": "2026/08/02 18:40 (台北) · 週日盤前",
  "count": 2,
  "days": [ { "date": "2026-08-02", "weekday": "週日",
              "stamp": "2026/08/02 18:40 (台北) · 週日盤前",
              "headline": "當日心得標題", "cards": 131,
              "keptDates": ["2026/07/31","2026/08/01","2026/08/02"],
              "file": "data/2026-08-02.json" } ] }
```

**`data/YYYY-MM-DD.json`** 的頂層鍵：`date`／`weekday`／`stamp`／`headline`／`keptDates`／`cards`／`overview`／`essay`／`sections`／`about`。

- `overview`：`snap`（6 格，各含 `k`/`v`/`tone`，tone＝`up`/`dn`/`fl`）、`focus`（4 張，`k`/`v`）、`takeawaysTitle`、`takeaways`（7 條）、`thermo`（`level`/`note`）、`watch`（`d`/`t`）
- `essay`：`title`／`by`／`kick`／`paras`（5–6 段）
- `sections`：三個區塊（id＝`macro`/`industry`/`politics`），各含 `title`/`en`/`intro`/`groups`；`groups` 內為 `label`/`accent`（``/`tw`/`macro`/`mat`）/`cards`
- **卡片 dict**：`src`（來源代碼）／`tag`／`tagcls`（``/`hot`/`warn`/`pos`）／`date`（`YYYY/MM/DD`）／`title`／`deep`（bool）／`body`（deep 時為段落 list，否則字串）／`bullets`／`url`／`tone`（`t-green`/`t-yellow`/`t-orange`/`t-red`）
- `about`：`timeliness`／`notes`（list）／`access`／`run`／`limits`

**欄位值可含 `<b>`、`<strong>`、`<span>` 等行內 HTML**，由前端 `innerHTML` 渲染，寫入時請自行確保標籤成對。

**每日發布動作只有兩個**：(1) 新增 `data/<今天>.json`；(2) 把今天這筆 **加進** `index.json` 的 `days` 並依日期由新到舊排序。**不要動任何既有的日期檔。** 若同一天重跑，覆蓋當天那一個檔即可。

---

## 4. 版面結構（六個分頁）

沿用現有 `index.html` 的 **淺色系 CSS**、版面、分頁與互動邏輯、徽章 class；只更新資料與 `stamp`（台北時間）。**配色為淺色系**（`--bg:#eef2f7`、`--card:#fff`、深藍灰字），勿改回深色。頁面最上方為**日期切換列**（顯示最近 7 天，更早的收進下拉選單）。

**定位＝新聞閱讀中心（reading hub），內容越充實越好。** 市場總經／產業與主題／政經三大分頁的**每個子類別至少 10 則**；採「分層摘要」：
- **重點則（每子類別 2 則左右）**：用 `.card.wide`（跨兩欄）＋ `.longread`（多段落、約 800～1,000 字的深度摘要）＋標 `.tag.deep`「深度」；深入說明事件來龍去脈與對市場的意義。
- **其餘則**：一般 `.card` ＋ `.lead`（約 300～400 字中長摘要）＋ 2～3 條重點 bullet。

1. **三分鐘總覽**：
   - 跨資產快照列（`.snap`）：S&P 500、那斯達克、布蘭特油、黃金、美元/日圓、30 年美債或銅等 6 格（漲綠 `.up`／跌紅 `.dn`／平 `.fl`）。
   - 四張焦點卡（`.focus`）：當日最重要的四條主軸。
   - 七大重點 takeaways（`.takeaways`）：濃縮當日跨版面重點。
   - 溫度條＋情緒註解、主要來源徽章列、本週盯盤時程（`.watch`）。
2. **摘要與心得**：讀完當日 19 家後，寫一篇**約 1,000 字**的綜合彙整＋觀點（`.essay`）。要有一句 kick 破題、5～6 段分主題論述（如 AI 資本支出、財報冷熱、能源地緣、央行/債市、亞洲/台股），結尾給「投顧視角小結」與 2～3 個可驗證盯盤節點。非投資建議。
3. **市場總經**（section id＝`macro`）：**美股與財報**／**央行、利率與匯率**／**台股與亞太**（各分組用 `.group-label`）。
4. **產業與主題**（section id＝`industry`）：**AI 與半導體**／**金融、併購與企業**／**能源與原物料**。
5. **政經**（section id＝`politics`）：**地緣政治（中東與戰事）**／**美國政治與政策**。

**子類別固定為以上八組**，`≥10 則`的下限逐組計算。要增減子類別必須同時改本節、排程 prompt 與既有資料檔的分組結構，不可只在其中一處新增分組。生技與原物料不另立子類別：生技併入「金融、併購與企業」，原物料併入「能源與原物料」。
6. **關於與方法**：來源、時效、合規、限制（大致固定，日期需更新）。

**每則卡片**：來源徽章＋主題標籤（`.tag`，可 hot/warn/pos）＋日期＋標題（`h3`）＋一段詳細闡述（`.lead`）＋2～3 條重點 bullet（`.card ul`）＋原文連結（真實可點）＋溫度色條（`t-green`/`t-yellow`/`t-orange`/`t-red`）。摘要要「詳細一點、多一些闡述」，不只列點。

---

## 5. 產出與發布流程

1. **先讀 `data/index.json`**，確認今天是否已產出（同日重跑就覆蓋當天的檔），並看昨天的 `keptDates` 以決定今天要汰換哪些日期。
2. 用 Claude in Chrome 逐一讀 19 家當日重點（付費為主）。建議開 **6 個 subagent 平行分組**，每個先自己開新分頁再作業：
   - A：Bloomberg ＋ WSJ
   - B：FT ＋ NYT ＋ WaPo
   - C：Nikkei ＋ 華爾街見聞 ＋ CNBC ＋ MarketWatch（**並負責全套市場數據**）
   - D：**Reuters ＋ Tom's Hardware ＋ OGJ**
   - E：Politico ＋ The Hill ＋ Barron's ＋ IBD（後兩家先做登入狀態測試，見第 1 節）
   - F：**鉅亨網 ＋ MoneyDJ ＋ TWSE／公開資訊觀測站**（台股專組）
3. **每日必抓的官方數據**（F 組與 C 組分工）：
   - 台股：加權指數與櫃買收盤、**三大法人買賣超**、**融資餘額**、當日重要月營收與法說會（TWSE／MOPS）
   - 利率：**CME FedWatch 的下次會議升降息機率**（不要只引用媒體轉述的百分比）
   - 能源：**EIA 週報庫存**（週三）、每季**美國財政部再融資公告（QRA）**的日期與規模
   - 匯率：日本財務省的干預實績公布（月底）與 BOJ 貨幣市場初步數據
4. 依本文件與第 3.5 節的 schema 產生 `data/<今天>.json`，並把今天加進 `index.json` 的 `days`。
5. **直接用檔案工具寫入** `/Users/kenny/advisory-knowledge-hub/data/`。`index.html` 是外殼，**除非要改版面，否則不需要動它**。
6. 之後**不需手動 push**：使用者 Mac 上的 launchd 背景程式（`com.kenny.dashpush`，每 3 分鐘）會自動 `git add`＋`commit`＋`push`；GitHub Actions 自動部署到 `https://gundamnboy.github.io/advisory-knowledge-hub/`。
7. **發布前自我檢查**（做不到就不要發）：
   - 日期直方圖只剩 3 個日期
   - 當日新卡佔全站 1/4～1/3
   - 每個子類別 ≥10 則
   - 每張卡片都有真實可點的原文連結
   - **當日新卡不得與既有卡片共用同一原文連結**（同一篇文章不重複成卡；程式化比對 `url` 即可）
   - **每張卡片的 `src` 值必須在第 1 節的徽章清單內**，否則前端會渲染出沒有樣式的空徽章
   - JSON 可被 `json.load` 正常解析、`index.json` 的 `days` 已含今天且由新到舊排序
8. 等 2–4 分鐘後抓 `https://gundamnboy.github.io/advisory-knowledge-hub/data/index.json` 驗證 `days[0].date` 是今天。若拿到舊內容可能是 CDN 快取，改用 Chrome 以 `cache:'no-store'` 重抓確認。

**時間預算**：19 家的目標是 **07:30 開始、11:30 前完成產出**。若進度落後，**依序砍以下項目**，不要砍到版面下限：(1) 深度卡由每子類別 2 張降為 1 張；(2) 每家的閱讀篇數各減三分之一。**不可砍的是**：市場數據、台股官方數據、每子類別 ≥10 則、當日新卡佔比，以及「關於與方法」的 `run` 欄如實記錄。

**Barron's 與 IBD 不再列入降級項目。** 舊版把「砍 Barron's 與 IBD 的逐篇嘗試」列為第一階降級，那是建立在「這兩家常被付費牆擋住、試了也是白試」的錯誤前提上；第 1.1 節已證實兩家內文可完整讀取，砍它們等於白白丟掉美股選股視角。要省時間請從深度卡張數下手。

**重要操作禁忌**：不要跑任何 `git` 指令（含 `git status`）。沙箱無網路、且不能刪檔，跑 git 會留下 `.git/index.lock` 鎖檔擋住背景推送。只用 `cat`/`ls`/`grep` 等唯讀指令檢查狀態即可。

---

## 6. 基礎設施備忘

- **Repo（本機）**：`/Users/kenny/advisory-knowledge-hub`（家中 MacBook Pro；放在家目錄下，不要移進 `~/Documents`，因 macOS TCC 會擋背景程式存取受保護資料夾）。掛載於沙箱 `mnt/kenny--advisory-knowledge-hub/`（實際掛載名稱以當下 `ls` 為準）。分支＝`main`。
- **GitHub**：`GunDamnBoy/advisory-knowledge-hub`，GitHub Pages（Source＝GitHub Actions），`.github/workflows/deploy.yml` 自動部署。
- **推送認證**：fine-grained PAT `home-mac push`（只授權此 repo 與 podcast repo、Contents 讀寫），**存於 macOS 鑰匙圈**（`git config --global credential.helper osxkeychain`），**不內嵌於 remote URL、不以明碼存在任何檔案中**。換 token：產新 PAT → 在終端機手動 `git push` 一次、於提示輸入新 token（Username＝`GunDamnBoy`）→ 鑰匙圈自動覆蓋 → 撤舊。**任何情況下都不要把 token 寫進檔案或 remote URL。**
- **背景推送腳本**：`~/.dashpush/auto-push.sh`（有變動就 commit、本機領先遠端就 push）；由 launchd agent `com.kenny.dashpush` 每 180 秒觸發。
- **排程任務**：`advisory-dashboard-daily`，cron `30 7 * * *`（台北時間，一週七天）。另一個任務 `podcast-digest-daily` 排在 09:00，兩者刻意錯開。
- **Chrome 連線（2026/08/03 確認）**：帳號上同時掛著兩個 Chrome 擴充功能實例，`list_connected_browsers` 會回傳 2 台，且**清單裡的 `name` 一律顯示為 Browser 1／Browser 2，不會反映使用者在擴充功能裡取的名字**，`isLocal` 兩台也都是 `true`，無法用來分辨。對應關係如下：
  - **`8f82131f-7af7-4a5d-a5d7-93677f4e3884` ＝ HOME（家中 MacBook Pro，發布機器，各家訂閱在此登入）→ 一律選這台。**
  - `120b7860-d389-4e1a-9c77-6b590e5a9881` ＝ WORK（辦公室那台，已停用為發布機器，勿使用）。
  - 排程情境**不要呼叫 AskUserQuestion 詢問**，直接 `select_browser("8f82131f-7af7-4a5d-a5d7-93677f4e3884")`。若該 deviceId 不在清單中，才退而選 `connectedAt` 最大的那一台，並在 `run` 欄註明。
  - 選定後務必做一次可用性測試（讀一篇付費來源文章、確認取得完整內文）再開始正式作業。
- **容量**：每日 JSON 約 200KB，一年約 70MB，GitHub Pages 綽綽有餘，因此**歷史全部保留、不設汰除**。若未來單日檔案明顯變大，優先檢查是不是深度卡寫太多，而不是刪歷史。
- **模式限制備忘**：互動階段能讀 Chrome、但雲端不能直接推 GitHub；背景/排程階段能推 GitHub、但讀不到 Chrome。故付費版必在互動階段產出、由本機背景程式負責推送。

---

## 7. 語氣

繁體中文（台灣慣用語）、精簡、可快速掃讀、面向投顧專業讀者；摘要詳實但不冗長；心得有觀點但保持中立、非投資建議。

---

## 8. 變更紀錄（CHANGELOG）

**維護規則**：這份 brief 與排程任務 `advisory-dashboard-daily` 的 prompt 是**一組兩份**，改任一邊都必須同步另一邊，並在本節加一筆。詳見 `MAINTENANCE.md`。日期由新到舊。

### 2026-08-03（第 2 次修訂 · 讀取方法與瀏覽器綁定）

- **修正付費牆判斷方式（重要）**：新增第 1.1 節。原本以「導覽列是否出現 Sign In」判斷來源可否讀取，**這是錯的**——Bloomberg 與 Barron's 的導覽列永遠顯示 Sign In／Subscribe Now，但內文照常完整載入。改為以實際取得的內文量判斷（段落數 ≥8 且 ≥1,500 字視為完整）。
- **改變主要讀法**：`get_page_text` 在 Bloomberg、Barron's、MarketWatch 上會嚴重低估內文，僅適合掃標題。正式讀取改用 `javascript_tool` 抓 `article p`，並先等 3–5 秒讓頁面渲染。
- **綁定瀏覽器 deviceId**：第 6 節新增 HOME／WORK 對應表。`list_connected_browsers` 回傳的 `name` 不反映使用者命名、`isLocal` 兩台皆為 true，無法分辨，故直接寫死 HOME 的 deviceId。
- **影響**：8/3 當日版本因此誤判而未收錄任何 Barron's 卡片，Bloomberg 亦僅採用部分段落；該日 `about.run` 已加註更正說明。

### 2026-08-03（第 1 次修訂 · 來源擴充）

- **來源自 15 家擴充為 19 家**：Reuters 由「公開／官方補充」升格為具名來源（徽章 `reuters`，不再併入 `pub`）；新增鉅亨網（`anue`）、MoneyDJ（`moneydj`）、TWSE 與公開資訊觀測站（`twse`）。動機是台灣本地內容過薄——8/3 當天「台股與亞太」子類別沒有任何一則來自台灣媒體。
- **`index.html` 同步**：新增四個徽章 CSS 與 `BADGE` 對應，`SRCBAR` 由 15 擴為 19。這是少數需要動外殼的情況。
- **subagent 分組改為 6 組**（原 5 組），新增台股專組（F）與 Reuters 組（D）。
- **新增每日必抓的官方數據**：台股三大法人買賣超與融資餘額、CME FedWatch 機率、EIA 週報庫存。動機是先前在盯盤時程列出「融資餘額」當追蹤指標，卻沒有對應的資料來源。
- **新增兩條發布前檢查**：當日新卡不得與既有卡片共用同一原文連結（8/3 首次建檔時抓到 9 張重複）；每張卡片的 `src` 必須在徽章清單內。
- **新增時間預算與降級順序**：目標 11:30 前完成，落後時的取捨有明確優先序。

### 2026-08-02

- 改為封存制：`index.html` 拆成外殼＋`data/*.json`，每日獨立存檔永久保留，頁面最上方加日期切換列（第 3.5 節）。
