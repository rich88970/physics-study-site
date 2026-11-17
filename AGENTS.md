# AGENTS.md｜讀懂物理（物理系課程讀書網站）

這份文件寫給在這個專案裡新增或修改內容的 AI（Claude Code、Codex 等）。動手之前先讀完；沒寫到的情況，照「現有章節長怎樣」去做，不要自創新格式。

## 1. 專案目的

把大學物理系的課（力學、熱學、近代物理、光學、應用數學）整理成「讀得懂、考得出來」的讀書網站：
- 依老師講義的頁碼順序講解；沒有講義的科目照課本章節順序。
- 每一題都有完整解題，並附「考試書寫版」：考卷上實際該寫什麼。
- 讀者是要準備期中期末考的學生，所以內容以「解題步驟」為主軸，不寫空泛的觀念散文。

## 2. 網站結構

純靜態網站，不需要建置伺服器，GitHub Pages 直接提供。

```
index.html                  科目首頁（讀 subjects/registry.json 產生科目與章節清單）
chapter.html                通用章節頁：chapter.html?s=<科目id>&c=<章節id>&p=<節id>
assets/site.css             全站排版（深淺色、手機版、各種區塊樣式）
assets/site.js              載入章節、KaTeX 算式、考試書寫版側欄、目錄、考試模式、圖解
assets/anim.js              逐步圖解引擎（Anim.define）
assets/bundle.js            自動產生：subjects/ 的內容打包檔，讓雙擊 index.html 也能讀（不要手改）
assets/vendor/katex/        本機 KaTeX（不依賴外部 CDN）
subjects/registry.json      科目與章節清單（新增章節一定要登記）
subjects/<科目>/<章>/
    chapter.json            章名、範圍、小節順序（overview＋sections，每節一句 desc）
    sections/NN-名稱.html   各小節正文（一節一頁）
    exam.html               考試書寫版（側欄內容，每題一段）
    step_symbols.json       符號總表＋每一步要提醒的符號
    figures*.js             本章圖解
    videos/                 （只有力學第 1 章有）講解影片與時間軸
subjects/_template/ch01/    新章節範本
tools/                      建置、檢查、轉換工具（見第 6 節）
tools/sources/*.md          「考古題章」「公式表章」的 Markdown 來源（改這裡再轉換，不直接改產生的 HTML）
```

科目 id：`mechanics` 力學、`thermal` 熱學、`modern` 近代物理、`optics` 光學、`applied-math` 應用數學。
章節 id：一般章 `ch01`、`ch02`…；額外章固定用 `kaogu`（考古題）、`formulas`（公式表）。只用小寫英數與 `-`。
小節檔名：`NN-英文短名.html`（`00-intro.html` 是總覽、最後一節 `NN-exam.html` 是考前衝刺），順序跟 chapter.json 一致。

## 3. 版面與風格

- 語言：**台灣繁體中文**（用「影片、品質、資訊、程式」，不用「視頻、質量、信息、程序」），全形標點；題目原文保留英文。
- 數學一律用 LaTeX：行內 `$...$`、獨立 `$$...$$`，單位與下標也一樣（`$9.8\ \text{m/s}^2$`、`$W_{\text{on}}$`）。長式子用 `aligned`／`gathered` 拆行，避免手機版溢出。
- 只有三種東西有框：講義原文（淡棕底）、題目卡、圖解。觀念說明、注意事項都是一般段落，不要加彩色標籤或 emoji。
- 每節一頁，頁底有上一節／下一節；跨章連結寫 `<a data-chapter="科目/章" href="#卡片id">`。
- 每章最後一節是「考前衝刺」：必背公式（`.sheet`）、題型總表（`.drill`）、變化題（`details.reveal`）。

## 4. 內容格式（新增內容時照這些格式）

### 4.1 題目卡

```html
<div class="problem" data-kind="example|textbook|tbexample|self|exam" id="c2-tm-2-16">
  <header> .meta（.chip 標籤＋出處）、h4 題目標題、考試書寫版按鈕 </header>
  <div class="pbody">
    <div class="part statement">  英文原題（section.original-source，有文字才放）＋中文題目 </div>
    <div class="part solution concise"> 解題（格式見 4.2） </div>
  </div>
</div>
```

- `id` 規則：`<章縮寫>-<來源>-<題號>`，例如 `c2-tm-2-16`（Thornton & Marion 2-16）、`sc-1-8`（Schroeder 1.8）、`c2-self-11c`（自編）。全站唯一，連結和考試書寫版都靠它。
- `data-kind="self"` 是自編難題，chip 要寫「自編難題」，不能假裝是課本或考卷題。
- 每個講解節放 2 題自編難題（光學除外：光學只收作業與考古題）。
- 考古題保留原卷的小題、配分和用字；原卷筆誤不在英文原文裡改，在解題裡用 `**注意：**` 說明。

### 4.2 解題格式（精簡步驟版，全站統一）

```
<p class="symnote">符號：每個符號是什麼、已知數值、座標方向。</p>
<p><strong>① 步驟名稱：</strong> 一兩句說這步在做什麼、為什麼。</p>
<div class="math-block">$$ 計算 $$</div>
<p class="fnote"><b>公式（名稱）：</b>一般式，其中各符號意義；本題對應……</p>
<p><strong>② …</strong></p>
<div class="math-block">$$\boxed{ 最後答案 }$$</div>
```

- 以**解題過程**為主軸，一步一個編號（①②③），每步一兩句話＋公式＋計算。
- 第一次用到某個公式時寫一行 `p.fnote`「公式（名稱）：…」，同一題不重複，不同題要重寫。
- 數值代入要看得出每個數字從哪來。
- **不要寫驗算、代回檢查**，除非題目本身要求（例如 show that、證明線性獨立）。
- 答案用 `\boxed{}`，多個答案用 `gathered` 拆行。

### 4.3 考試書寫版（exam.html）

每題一段，對應卡片 id：只寫考卷上該寫的式子和一句必要的文字說明，不寫教學內容。

### 4.4 公式表章、考古題章

不要直接改 HTML，改 `tools/sources/` 的 Markdown 再轉換：
- 力學公式表：`tools/sources/mechanics-formulas.md` → `python tools/build_mechanics_formulas.py`。每條公式：`### 名稱 | 連回的章#錨點`、公式、一兩句說明（在說什麼、什麼條件能用、常見錯誤）。
- 應數、光學考古章：`tools/sources/applied-math-kaogu.md`、`optics-kaogu.md` → `python tools/build_extra_md.py applied-math|optics`。每題「原題／中文／① 步驟」格式，公式下補「符號：」說明。
- 熱學考古章：`tools/sources/thermal-kaogu.md` → `python tools/build_thermal_kaogu.py`（卡片標頭與題目從 ch01／ch02 原樣複製，要改題目就改原章再重跑）。

## 5. 新增一章的步驟

1. 複製 `subjects/_template/ch01` 到 `subjects/<科目>/<章>`。
2. 在 `subjects/registry.json` 登記章節（title、range、`"status": "ready"` 才會出現在首頁）。
3. 編 `chapter.json`：`sections` 每節一筆 `{ "id": "s01", "file": "01-xxx.html", "title": "…", "pages": "p.1–5", "desc": "一句話" }`，依講義頁碼排序；
   `overview` 填總覽節的 id（`"s00"`，檔案 `00-intro.html`，內含 `<div data-section-list></div>` 自動列出各節）。
4. 寫 `sections/*.html`（照第 3、4 節格式）、`exam.html`、`step_symbols.json`。
5. 執行第 6 節的建置與檢查，全部通過才算完成。

## 6. 建置與檢查（每次改完都要跑）

```bash
python tools/lint_static.py        # 靜態檢查：\theta 的 \t 被寫成 Tab、數學式裡裸露的 < 等 KaTeX 不報錯但畫面會壞的情況
python tools/build_bundle.py       # 重新產生 assets/bundle.js（改了 subjects/ 一定要跑）
python tools/check_pages.py 科目/章  # 用無頭 Chrome 逐頁檢查：公式錯誤、手機與桌機寬度溢出、圖解、跨頁連結（需要 Chrome）
```

本機預覽：直接雙擊 `index.html`，或在專案根目錄 `python -m http.server` 後開 `http://localhost:8000`。

## 7. AI 修改內容時的規則

- **不放有版權的原始圖片**：課本、講義、考卷的掃描或截圖不上這個公開網站。英文原題用文字放在 `section.original-source`，附出處（書名、題號、頁碼）。
- 老師上課的照片、私人檔案、個人資料不放上網站。
- 「網站補充」（講義沒有、網站自己補的內容）要標 `.added`；講義筆誤標「板書誤植」，不要默默改掉。
- 只改被要求的範圍；改格式時不能改到題目內容與答案。大量改寫前先列出會動到哪些檔案。
- 新的計算答案要用程式（Python、sympy）獨立算過一次再寫進網站。
- 不手改 `assets/bundle.js` 和 `tools/sources/` 轉出來的 HTML。
- `assets/site.css`、`site.js` 是全站共用：改樣式時要確認五個科目都沒有跑版。
- commit 訊息用繁體中文寫「改了什麼、為什麼」。
