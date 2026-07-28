# AGENT BRIEF — 投顧知識庫儀表板・每日重生標準說明

這份文件是「投顧知識庫儀表板」的完整規格。任何一個新的 Cowork 對話（或換裝置）讀了這份，就能完整重現整套系統。使用者說「**跑今天的儀表板**」時，即依本文件執行。全程使用繁體中文（台灣用語），讀者為投顧從業人員。

---

## 0. 觸發與環境前提（重要）

- **只能在「使用者本人開的互動 Cowork 對話、且桌機 Chrome 外掛已連線」時執行。** 讀付費訂閱要靠 Claude in Chrome 附著於互動對話；排程／背景階段連不到瀏覽器，只能出免費版。
- 每天早上使用者到公司（Chrome 開著、手機熱點連著電腦）後，說一句「跑今天的儀表板」即觸發。
- 另有一個平日 08:00 的手機推播提醒，提醒使用者來說這句話。

---

## 1. 主要來源（15 家，付費為主體、免費為輔）

**付費訂閱**（使用者本人訂閱，於其已登入的 Chrome 讀）：
Bloomberg (bloomberg.com/asia)、WSJ (wsj.com)、NYT (nytimes.com/international)、FT (ft.com)、Nikkei Asia (asia.nikkei.com)、Washington Post (washingtonpost.com)、Barron's (barrons.com)、IBD (investors.com)、**Politico (politico.com)**、**The Hill (thehill.com)**

**免費公開**：
CNBC (cnbc.com/world)、MarketWatch (marketwatch.com)、Tom's Hardware (tomshardware.com)、Oil & Gas Journal (ogj.com)、華爾街見聞 (wallstreetcn.com)

**公開／官方補充**：Reuters 體系、CBS、AP、官方央行／交易所／公司 IR、政府與司法機構公告。

**Politico 與 The Hill 專供政經分頁**（地緣政治＋美國政治）的深度與時效——國會立法、國防／撥款、選舉、司法與 Fed 獨立性等。

來源徽章 class：`b-bbg`/`b-wsj`/`b-nyt`/`b-ft`/`b-nikkei`/`b-wapo`/`b-barrons`/`b-cnbc`/`b-ibd`/`b-mw`/`b-toms`/`b-ogj`/`b-politico`/`b-thehill`/`b-wscn`/`b-pub`。

各來源擅長：Bloomberg＝全球即時＋亞洲；WSJ／NYT＝美國政經；FT＝全球／科技／市場；Nikkei＝亞洲供應鏈／匯率；WaPo＝美政治／地緣；Barron's／IBD／MarketWatch＝美股與選股視角；Tom's Hardware＝半導體/GPU/資料中心；OGJ＝油氣/LNG；華爾街見聞＝中文彙整西方財經＋亞洲。

**內容優先序**：每個分區以付費來源卡片打底、排前面；免費來源只補付費沒涵蓋到的角度。**核可的免費來源僅限**上列五家＋官方／通訊社；**嚴禁**內容農場或小報（Motley Fool、ETtoday、Intellectia、內容聚合站等）。

---

## 2. 合規紅線（必守）

- 只讀使用者本人訂閱、在其登入的 Chrome 中合法存取的付費內容；以及免費公開來源。
- **絕不使用任何繞過付費牆或反爬蟲的手段。**
- 公開頁面只放「原創重點摘要＋原文連結」，不轉載付費文章全文或逐字複製大段內容。
- 財務數字（單季獲利、資本支出、募資／併購金額、即時報價漲跌）盡量以官方或多來源交叉；不確定者標註。

---

## 3. 時效性

本儀表板為**日更**，使用者最重視的就是「每天打開都看到最新資訊」。

**核心規則：全站只保留最近 3 個日期（約當日與前兩日）的卡片。** 例如 7/28 這一版，全站日期只會出現 7/26、7/27、7/28。

- **超過 3 個日期的卡片一律處理掉**：能用當日最新進度改寫的就改寫（換新來源、換新標題、更新數字），改寫不了的就直接刪除，不留在頁面上。
- **每日新增量**：當日新卡片至少佔全站的 1/4～1/3（近期實務約 35～40 則），確保「今天」是版面主角，不是靠舊卡撐版面。
- **刪完仍要守版面下限**：每個子類別 ≥10 則的規定優先——先補齊當日新內容，再刪舊卡，不可為了汰舊讓子類別掉到 10 則以下。
- **結構性事件用「前瞻／最新一次」框架**：CPI、非農、FOMC／ECB／BOJ 決議等本來就是低頻事件，不可直接引用一兩個月前的舊會議當新聞；要改寫成「下次會議前瞻」或「最新一次決議＋至今的市場反應」，日期掛在寫作當日。
- **日期一律標於每張卡片**（`<span class="date">`），發布前用日期直方圖檢查一次，確認只剩 3 個日期。
- 「關於與方法」分頁的時效性說明要同步寫出本次保留的日期區間。

---

## 4. 版面結構（單頁 HTML，六個分頁）

沿用現有 `index.html` 的 **淺色系 CSS**、版面、分頁與互動邏輯、徽章 class；只更新內容與最上方「最後更新」時間戳（台北時間）。**配色為淺色系**（`--bg:#eef2f7`、`--card:#fff`、深藍灰字），勿改回深色。

**定位＝新聞閱讀中心（reading hub），內容越充實越好。** 市場總經／產業與主題／政經三大分頁的**每個子類別至少 10 則**；採「分層摘要」：
- **重點則（每子類別 2 則左右）**：用 `.card.wide`（跨兩欄）＋ `.longread`（多段落、約 800～1,000 字的深度摘要）＋標 `.tag.deep`「深度」；深入說明事件來龍去脈與對市場的意義。
- **其餘則**：一般 `.card` ＋ `.lead`（約 300～400 字中長摘要）＋ 2～3 條重點 bullet。

1. **三分鐘總覽**：
   - 跨資產快照列（`.snap`）：S&P 500、那斯達克、布蘭特油、黃金、美元/日圓、30 年美債或銅等 6 格（漲綠 `.up`／跌紅 `.dn`／平 `.fl`）。
   - 四張焦點卡（`.focus`）：當日最重要的四條主軸。
   - 七大重點 takeaways（`.takeaways`）：濃縮當日跨版面重點。
   - 溫度條＋情緒註解、主要來源徽章列、本週盯盤時程（`.watch`）。
2. **摘要與心得**：讀完當日 15 家後，寫一篇**約 1,000 字**的綜合彙整＋觀點（`.essay`）。要有一句 kick 破題、5～6 段分主題論述（如 AI 資本支出、財報冷熱、能源地緣、央行/債市、亞洲/台股），結尾給「投顧視角小結」與 2～3 個可驗證盯盤節點。非投資建議。
3. **市場總經**：美股與財報／台股與亞太／全球央行與總經（各分組用 `.group-label`）。
4. **產業與主題**：AI／科技／金融／生技／原物料。
5. **政經**：地緣政治／美國政治。
6. **關於與方法**：來源、時效、合規、限制（大致固定，日期需更新）。

**每則卡片**：來源徽章＋主題標籤（`.tag`，可 hot/warn/pos）＋日期＋標題（`h3`）＋一段詳細闡述（`.lead`）＋2～3 條重點 bullet（`.card ul`）＋原文連結（真實可點）＋溫度色條（`t-green`/`t-yellow`/`t-orange`/`t-red`）。摘要要「詳細一點、多一些闡述」，不只列點。

---

## 5. 產出與發布流程

1. 用 Claude in Chrome 逐一讀 15 家當日重點（付費為主）。
2. 依本文件重生 `index.html`（保留 CSS 與結構，只換內容＋時間戳）。
3. **更新桌面 artifact**：`mcp__remote-devices__update_artifact`，id = `advisory-knowledge-hub`（先 SendUserFile 取 file_uuid）。
4. **寫入使用者 Mac 的 repo**：`mcp__remote-devices__device_commit_files` 寫到 **`/Users/kennychiang/advisory-knowledge-hub/index.html`**（force:true）。
5. 之後**不需手動 push**：使用者 Mac 上的 launchd 背景程式（`com.kenny.dashpush`，每 3 分鐘）會自動 `git add`＋`commit`＋`push`；GitHub Actions 自動部署到 `https://gundamnboy.github.io/advisory-knowledge-hub/`。

**重要操作禁忌**：不要用 `device_bash` 跑任何 `git` 指令（含 `git status`）。device_bash 是無網路的沙箱、且不能刪檔，跑 git 會留下 `.git/index.lock` 鎖檔擋住背景推送。只用 `cat`/`ls`/`grep` 等唯讀指令檢查狀態即可。

---

## 6. 基礎設施備忘

- **Repo（本機）**：`/Users/kennychiang/advisory-knowledge-hub`（已移出 `~/Documents`，因 macOS TCC 會擋背景程式存取受保護資料夾）。掛載於沙箱 `mnt/kennychiang--advisory-knowledge-hub/`。
- **GitHub**：`GunDamnBoy/advisory-knowledge-hub`，GitHub Pages（Source＝GitHub Actions），`.github/workflows/deploy.yml` 自動部署。
- **推送認證**：remote URL 內嵌 fine-grained PAT（只授權此 repo、Contents 讀寫），存於本機 `.git/config`。換 token：產新 PAT →「`git -C ~/advisory-knowledge-hub remote set-url origin https://<新PAT>@github.com/GunDamnBoy/advisory-knowledge-hub.git`」→ 撤舊。
- **背景推送腳本**：`~/.dashpush/auto-push.sh`（有變動就 commit、本機領先遠端就 push）；由 launchd agent `com.kenny.dashpush` 每 180 秒觸發。
- **模式限制備忘**：互動階段能讀 Chrome、但雲端不能直接推 GitHub；背景/排程階段能推 GitHub、但讀不到 Chrome。故付費版必在互動階段產出、由本機背景程式負責推送。

---

## 7. 語氣

繁體中文（台灣慣用語）、精簡、可快速掃讀、面向投顧專業讀者；摘要詳實但不冗長；心得有觀點但保持中立、非投資建議。
