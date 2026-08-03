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
- **報價口徑不可混用。** 美股收盤價與亞洲盤中報價、近月與連續合約、現貨與期貨，全部要標時間戳。
- **驗證上線要帶 cache-buster**，否則會拿到 CDN 舊快取而誤判推送失敗。

---

## 4. 新增一家來源的完整步驟

1. `AGENT_BRIEF.md` 第 1 節：加進付費／免費／官方的對應清單、徽章 class 列表、「各來源擅長」一句話、免費白名單。
2. `index.html`：加一條 `.b-<code>{...}` CSS、`BADGE` 物件加一筆、`SRCBAR` 陣列加一個代碼。三處都要，缺一個徽章會沒有樣式。
3. `AGENT_BRIEF.md` 第 5 節：把它放進某個 subagent 分組，並評估時間預算。
4. 排程 prompt 同步以上。
5. 第 8 節加變更紀錄。

---

## 5. 目前已知待辦與觀察中的事項

- **台股官方數據（TWSE／公開資訊觀測站）的抓取穩定度尚未驗證。** 三大法人買賣超與融資餘額是 2026-08-03 才加入的需求，頁面結構對自動化不友善，第一次實測在 8/4。抓不到就要換方法。
- **19 家的時間預算尚未實測。** 15 家那一輪從 07:40 跑到 13:10。目標是 11:30 前完成，落後時的降級順序見 brief 第 5 節。
- **候選的第二批來源**（時間撐得住再加）：TrendForce／集邦（目前 DRAM 價格都是二手轉引）、DIGITIMES（台廠訂單）、SemiAnalysis（HBM 與資料中心深度）、Punchbowl News（國會票數）。
- **HOME 的 deviceId 若因重裝 Chrome 或換設定檔而改變**，brief 第 6 節寫死的那一行會失效，需要更新。

---

## 6. 不要做的事

- 不要刪除或改寫既有的 `data/YYYY-MM-DD.json`。每天只新增一個檔案。
- 不要為了湊版面放舊聞或編造內容。清淡日改用「前瞻／最新一次」框架，並在心得中誠實說明。
- 不要用任何繞過付費牆、反爬蟲、archive 鏡像站或快取的手段。
- 不要用 WebFetch／curl／Python 抓新聞網頁，只用 Chrome 工具。
- 不要跑 git 指令。
