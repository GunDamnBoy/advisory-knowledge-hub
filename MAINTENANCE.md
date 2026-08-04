# MAINTENANCE — 投顧知識庫儀表板・維護說明

**這份文件是給「要修改這套系統」的人（或 Claude）看的，不是給執行每日產出的人看的。**
每日產出請看 `AGENT_BRIEF.md`。

想改動任何東西時，最快的方式是開一個新對話輸入 `/advisory-maintain`，或直接說「讀 MAINTENANCE.md」。

---

## 1. 這套系統由哪些東西定義

| # | 檔案／位置 | 角色 | 誰會讀它 |
|---|---|---|---|
| 1 | `~/advisory-knowledge-hub/AGENT_BRIEF.md` | **完整規格**：來源清單、讀取方法、時效原則、JSON schema、版面結構、合規紅線 | 每日排程在第 0 步完整讀過 |
| 2 | 排程任務 `advisory-dashboard-daily` 的 prompt | **執行手冊**：當天的步驟、分組、檢查清單。內容是 brief 的濃縮版 | 排程觸發時直接執行 |
| 3 | `~/advisory-knowledge-hub/index.html` | 前端外殼：CSS、渲染邏輯、日期切換列、來源徽章 | 瀏覽器 |
| 4 | `~/advisory-knowledge-hub/data/*.json` | 每日內容，永久封存 | `index.html` |

**最重要的一條規則：第 1 項與第 2 項是一組兩份，改任一邊都必須同步另一邊。**
兩者不同步時，排程會拿到互相矛盾的指示，而且不會報錯——它會安靜地照其中一份做。

改完務必在 `AGENT_BRIEF.md` 第 8 節「變更紀錄」加一筆，寫清楚**為什麼改**（動機通常比改了什麼更難重建）。

排程 prompt 沒有版本控制，只有 `AGENT_BRIEF.md` 在 git 裡。所以**brief 才是真正的來源**，prompt 是它的投影。

---

## 2. 修改的標準流程

1. 讀 `AGENT_BRIEF.md`（全部）與排程 prompt（用 `list_scheduled_tasks` 取得 `path` 後 Read）。
2. **先比對兩者是否已經不同步**，有的話先修好再談新需求。
3. 改 `AGENT_BRIEF.md`。
4. 用 `mcp__scheduled-tasks__update_scheduled_task` 同步排程 prompt。
5. 在第 8 節加變更紀錄。
6. 若動到來源清單，記得 `index.html` 的徽章也要加（見第 4 節）。
7. **不要跑任何 git 指令**（含 `git status`）——本機 `com.kenny.dashpush` 每 180 秒自動推送，跑 git 會留下 `.git/index.lock` 擋住推送。要看狀態只用 `cat`／`ls`／`grep`。

---

## 3. 已知的坑（踩過才寫進來的，不要再踩一次）

- **不要用導覽列有沒有 Sign In 判斷付費牆。** Bloomberg 與 Barron's 永遠顯示 Sign In，但內文完整。判準是實際取得的段落數與字數。詳見 brief 第 1.1 節。
- **`get_page_text` 在 Bloomberg、Barron's、MarketWatch 上會嚴重低估內文**，只回傳前 1–3 段或側欄。正式讀取要用 `javascript_tool` 抓 `article p`，並先等 3–5 秒。
- **同一篇文章不要重複成卡。** 當日新卡若與保留下來的舊卡共用同一 `url`，等於版面上出現兩張同源卡片。發布前程式化比對 `url`。
- **帳號上固定有兩個 Chrome 連線**，`name` 不反映使用者命名、`isLocal` 兩台都是 true。直接用寫死的 HOME deviceId（brief 第 6 節）。
- **`connectedAt` 不能用來分辨 HOME 與 WORK。** 實測 WORK 的 `connectedAt` 比 HOME 大，舊版 fallback「選 connectedAt 最大的那一台」會穩定選到已停用的辦公室機器，而且不會報錯。fallback 一律用排除法（排除 WORK 的 deviceId）。
- **報價口徑不可混用。** 美股收盤價與亞洲盤中報價、近月與連續合約、現貨與期貨，全部要標時間戳。
- **24 小時窗口的起點不能用「產出時刻往前推 24 小時」。** 本站在台北上午產出，前一晚美股收盤（美東前一日 16:00 ＝ 台北當日 04:00）的報導多半掛前一日日期；浮動起點會把當天最重要的素材整批切掉。起點一律固定為**前一日台北 07:00**。
- **`ts` 一律換算成台北時間（+08:00）再寫入。** 混用來源當地時區會讓窗口比對出錯，而且錯得很安靜——比對照樣跑得過，只是收了不該收的或丟了不該丟的。
- **驗證上線要帶 cache-buster**，否則會拿到 CDN 舊快取而誤判推送失敗。
- **每一次大改動當天都會留下新的不同步，沒有例外。** 第 2 次修訂漏了 brief、第 4 次修訂漏了三處（JS 讀法、檢查腳本、E 組用語）。改完當下**一定要再比對一次同步清單**，不要等隔天體檢才發現。最容易漏的是**兩段程式碼**（發布前檢查腳本、`javascript_tool` 讀法），因為它們藏在文件中段、不像散文那樣一眼看得出差異。
- **排程 prompt 是整份取代，不是局部編輯。** `update_scheduled_task` 送出的 `prompt` 會完全覆蓋舊的，漏帶的段落等於被刪除。改之前先 Read 一次現有全文。
- **本 repo 與 `~/podcast-knowledge-digest` 有 7 個同名檔案**：`AGENT_BRIEF.md`、`MAINTENANCE.md`、`README.md`、`index.html`、`data/index.json`、`data/2026-07-30.json`、`data/2026-08-02.json`。**任何腳本一律用絕對路徑**（brief 第 5 節的檢查腳本已改用 `REPO` 常數）。
- **維護作業若為了改另一條產線而連了 podcast 資料夾，做完要記得移除。** 排程任務的工作資料夾會保留這次連線——2026-08-03 就發生過：在排程執行的工作階段裡連了 podcast repo，結果 `advisory-dashboard-daily` 的 Working folders 多出一個它根本用不到、卻有寫入權的 Public repo。**目前沒有工具可以程式化移除，只能在 App 的 Working folders 面板手動拿掉。**

---

## 4. 新增一家來源的完整步驟

1. `AGENT_BRIEF.md` 第 1 節：加進付費／免費／官方的對應清單、徽章 class 列表、「各來源擅長」一句話、免費白名單。
2. `index.html`：加一條 `.b-<code>{...}` CSS、`BADGE` 物件加一筆、`SRCBAR` 陣列加一個代碼。三處都要，缺一個徽章會沒有樣式。
3. `AGENT_BRIEF.md` 第 5 節：把它放進某個 subagent 分組，並評估時間預算。
4. 排程 prompt 同步以上。
5. 第 8 節加變更紀錄。

---

## 5. 目前已知待辦與觀察中的事項

**（2026-08-04 更新：窗口制首次實測已完成，下列前五條「尚未驗證」已改寫為實測結果。）**

### 8/4 首次實測的結論

- **24 小時窗口制可行，但下限比時間更吃緊。** 8/4 產出 91 則、八組全部 ≥10 則、五項歸零指標（缺/壞 `ts`、逾期、未來 `ts`、`date`/`ts` 不一致、與前一版重複）**全數為 0**，09:17 寫檔完成、比 11:30 目標早約兩小時（6 組平行採集約 50 分鐘、撰寫約 25 分鐘）。**時間不是瓶頸，湊足 10 則才是。**
- **⚠ 三組毫無緩衝，這是目前最該處理的風險。** 「金融、併購與企業」「能源與原物料」「地緣政治（中東與戰事）」8/4 都**剛好卡在 10 則**——而那還是素材充足、且 Reuters 整天缺席的一天。若遇週末或清淡日又同時掉一家主力來源，這三組很可能湊不齊。**建議下次體檢時把這三組的下限由 10 調降為 8**（其餘五組維持 10），而不是放寬窗口。新增 SemiAnalysis 幫不上忙——它只補「AI 與半導體」，而那一組 8/4 有 14 則、本來就最寬裕。
- **`ts` 取得率不是問題。** 8/4 因抓不到發布時間而放棄的篇數極少，各組回報的放棄原因幾乎都是「逾期」而非「無 `ts`」；唯一的大宗是 Reuters 那 11 則，但那是頁面根本載不進來、不是選擇器不夠。brief 第 3.5 節現有的兩種通用寫法夠用，暫不需要為個別來源補選擇器。
- **F 組的最低產出要求有效。** 8/4 交回 9 則（鉅亨 5、MoneyDJ 4），超過 8 則下限，「台股與亞太」12 則中有 4 則來自台灣媒體。8/3 那次 0 則的狀況沒有重演。
- **台股官方源部分可用，已寫進 brief。** `bfi82u`（三大法人）、`mi-margn`（融資融券）、`mi-index`（大盤統計）**三頁均可正常取得**；**MOPS 的 `t21sc03_ifrs`（月營收）與 `t100sb02_1`（法說會）會被重導至新版 SPA 首頁而失敗**，已確認為結構性問題、不是偶發，往後直接走媒體轉引即可。櫃買（TPEx）官方頁連兩次 45 秒逾時，尚未找到可靠路徑。
- **一次性指示已於 8/4 移除。** 排程 prompt 第 5 步結尾那段「8/4 是窗口制第一次實測，請額外回報…」已刪除，改為在第 4 步與降級段落中保留實測數據作為參考基準。

### 仍在觀察 / 待辦

- **Reuters 的 DataDome 攔截是間歇性的，不要誤判為永久失效。** 8/4 早上整站回傳 CAPTCHA 挑戰頁（`geo.captcha-delivery.com`）、約 10 次重試皆失敗，導致當日整版沒有任何 Reuters 卡片；**同日稍晚以同一台瀏覽器重測即完全恢復正常**（列表頁 51 條連結、單篇 17 段／3,329 字、`article:published_time` 正常）。brief 第 1.1 節已補上處置規則與 D 組的補位辦法。若未來連續多日被擋，才需要重新評估這家的定位。
- **TPEx 櫃買指數尚無可靠抓取路徑。** 官方頁逾時、媒體端當日盤後彙整也未必寫出收盤點位。目前是「有就寫、沒有就略過」，尚未影響到任何硬性檢查項。
- **候選的第二批來源**（時間撐得住再加）：TrendForce／集邦（目前 DRAM 價格都是二手轉引）、DIGITIMES（台廠訂單）、Punchbowl News（國會票數）。**SemiAnalysis 已於 2026-08-04 正式納入（第 20 家，`src`＝`semi`，歸 D 組）**，不再列為候選。
- **SemiAnalysis 是每週 1～2 篇、不是日更**，brief 第 1.2 節已寫死「窗口內沒有新文是正常狀態、不記為降級、不得收錄窗口外舊文」。**這是本次擴充最容易被後續執行者破壞的地方**——某天為了湊「AI 與半導體」而回頭撈它上週的長文，檢查腳本的「逾期」那一項會抓到，但前提是執行者真的跑了腳本。
- **HOME 的 deviceId 若因重裝 Chrome 或換設定檔而改變**，brief 第 6 節寫死的那一行會失效，需要更新。（2026-08-04 實測：`list_connected_browsers` 只剩 HOME 一台；另注意回傳的 `name` 在同一場對話中曾先後顯示為 Browser 1 與 Browser 2，**`name` 完全不可作為判斷依據，只認 deviceId**。）
- **subagent 偶發「Multiple Chrome browsers are connected」並流失分頁。** 8/4 的 C 組因此中斷、只交回 1 則新聞（市場數據已完成）；重新 `select_browser` 後派 C2 組補齊 22 則，最終無影響。排程 prompt 第 1.5 步已加入「subagent 自行重選瀏覽器後重試、不要中止也不要問使用者」的指示。
- **WebFetch 抓 GitHub Pages 會拿到 CDN 快取的舊內容。** 8/4 發布後 5 分鐘用 WebFetch 仍回傳前一天的 `index.json`，改用 Chrome `fetch(..., {cache:'no-store'})` 並加 cache-buster 立即拿到新版。排程 prompt 第 4 步已寫入。
- **`notifyOnCompletion` 尚未開啟，而且踩到的坑比原本以為的更細。** 2026-08-03 與 2026-08-04 兩次嘗試都被擋，回應相同：「Can't subscribe a scheduled-task run session to completion notifications — it ends when the run does.」
  - **關鍵在於「工作階段的身分是開場時決定的，不會因為使用者中途加入而改變。」** 8/4 那次是使用者在排程跑完後、直接在同一個對話裡接著交代事情，感覺上已經是一般對話，但系統仍把它認定為 scheduled-task run session，所以照樣被擋。訂閱動作是綁在「當前工作階段」上的，而這個工作階段會隨著排程執行結束而消失。
  - **正確做法：另外開一個全新的對話**（不要在排程產出的那串後面接），對 Claude 說「幫我把 `advisory-dashboard-daily` 的 `notifyOnCompletion` 打開」，它會呼叫 `update_scheduled_task` 帶 `notifyOnCompletion: true`。
  - 開了之後每天跑完會主動通知，不必自己去看網站。另兩條線（`podcast-digest-daily`、`convergence-weekly`）同理，要開就一起開。

---

## 6. 執行環境：機器與電源（2026-08-03 確立）

**這套系統實質上是把一台舊 MacBook Pro 當常時開機的伺服器用。** 決策是：放在家裡、全天開機、插著電、不裝任何第三方電源管理軟體。

### 每天需要醒著的時間窗口

| 時間（台北） | 事件 | 需要什麼 |
|---|---|---|
| 01:00 | `com.kenny.podfetch`（另一條線） | Mac 醒著，約 30–45 分鐘 |
| 03:00 | `podcast-digest-daily` | Mac 醒著、Claude 桌面版開著 |
| **07:35** | **`advisory-dashboard-daily`** | Mac 醒著、Claude 開著、**Chrome 開著且各站維持登入** |
| 至 11:30 | 本線跑完 | 同上，持續 |

**是連續七小時，不是「時間到醒一下」。** 排定喚醒只解決起點，之後閒置會再睡回去，03:00 與 07:35 都會接不到。

### 已套用的設定

```bash
sudo pmset -c sleep 0          # 插電時永不睡眠（螢幕仍可關）
sudo pmset -c disksleep 0
sudo pmset -c womp 1           # 允許網路喚醒
sudo pmset repeat wakeorpoweron MTWRFSU 00:55:00   # 保險：萬一仍睡著
```

另加一項（2026-08-03）：

```bash
sudo pmset -b sleep 30    # 電池模式改 30 分鐘
```

電池模式原為 `sleep 1`——電源瞬斷（插頭鬆脫、跳電數十秒）切到電池後一分鐘就睡，正在跑的任務會直接中斷。30 分鐘可撐過短暫停電，又不至於把電池放到全空。

**2026-08-03 實測驗證通過**：AC Power 為 `sleep 0`、`disksleep 0`、`womp 1`、`displaysleep 10`；Battery Power 為 `sleep 30`；`pmset -g ps` 顯示 `AC Power`；`pmset -g sched` 顯示 `wakepoweron at 0:55AM every day`。

全天開機之後 `repeat wakeorpoweron` 理論上用不到，**但務必保留**——它是唯一能救「意外睡著或斷電」的機制，且不衝突。

**`autorestart` 無法驗證，不要當成保障。** `sudo pmset -c autorestart 1` 執行未報錯，但 `pmset -g custom` 的 AC Power 清單**不會列出這個鍵**，無從確認是否生效。Apple Silicon 機種已移除此鍵（預設即復電自動開機），Intel 機種應會列出。要確認機型跑 `uname -m`（`arm64` ＝ Apple Silicon、`x86_64` ＝ Intel）。**工作假設一律採保守版：停電當天需人工介入，該日產出視為會缺。**

### 為什麼不用 AlDente（或任何充電管理軟體）

AlDente 有三個功能會讓 Mac **在插著電時改用電池供電**：Discharge（官方描述即「即使插著電也完全靠電池運行」）、Sailing Mode（靠放電讓電量下滑到區間下緣）、Calibration Mode（自動跑 15%→100% 完整循環）。一旦電源來源變成電池，macOS 改套用 `pmset -b` 那組設定並積極睡眠，上面的 `-c sleep 0` **完全不生效**。

真正的否決理由不是「它會出錯」，而是**它的失效方式是安靜的**——某次更新重新啟用 Discharge、或手滑點到，結果是排程沒跑、網站停在昨天，現場看不出任何異常。這與本專案已知的 `auto-push.sh` 靜默失效是同一種模式。移除它換來的是少一個看不見的變數。

代價是電池會長期停在 100%。這台是舊機且定位為固定式伺服器，判斷為可接受；macOS 內建的「最佳化電池充電」可以保持開啟（它只延後充電、不放電，無害）。

### 其他前提

- **蓋子必須打開**，除非接了外接螢幕。闔蓋且無外接螢幕時一定會睡，`pmset` 擋不住。
- **Chrome 與 Claude 桌面版都要加進「系統設定 → 一般 → 登入項目」**，且 Chrome 視窗不要退出（付費來源的登入狀態綁在它身上）。
- **避免半夜自動重開機。** 自動更新若在凌晨重啟，Chrome 與 Claude 不會自己回來。建議設成「僅下載、手動安裝」。
- **若啟用 FileVault，任何重開機都需要人工輸入密碼才會進到桌面**，`autorestart` 也救不回無人值守的情境。這是目前已知、尚未解決的單點。
- 全天開機的機器要注意散熱，不要塞在密閉空間。

### 驗證

```bash
pmset -g custom     # 看 AC Power 段的 sleep 應為 0
pmset -g sched      # 應有 repeat wakeorpoweron 00:55:00
pmset -g ps         # 應顯示 "AC Power"，若顯示 Battery Power 代表有東西在放電
```

---

## 7. 不要做的事

- 不要刪除或改寫既有的 `data/YYYY-MM-DD.json`。每天只新增一個檔案。
- 不要為了湊版面放舊聞或編造內容。清淡日改用「前瞻／最新一次」框架，並在心得中誠實說明。
- 不要用任何繞過付費牆、反爬蟲、archive 鏡像站或快取的手段。
- 不要用 WebFetch／curl／Python 抓新聞網頁，只用 Chrome 工具。
- 不要跑 git 指令。
