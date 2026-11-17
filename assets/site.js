/* 讀懂物理｜共用程式：首頁科目清單、章節（總覽 + 每節一頁）、KaTeX、本步符號、考試書寫版側欄、影片、目錄。
   新增科目只需在 subjects/registry.json 登記，並依 subjects/_template 建立章節資料夾。 */
(function () {
  "use strict";

  var store = {
    get: function (k, d) { try { var v = localStorage.getItem("study:" + k); return v === null ? d : v; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem("study:" + k, v); } catch (e) { /* 無法儲存時仍可閱讀 */ } }
  };

  var KATEX_MACROS = {
    "\\uvec": "\\hat{\\mathbf{#1}}",
    "\\dd": "\\mathrm{d}",
    "\\T": "^{\\mathsf T}"
  };

  function renderMath(el) {
    if (!window.renderMathInElement) return;
    window.renderMathInElement(el, {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "\\[", right: "\\]", display: true },
        { left: "$", right: "$", display: false },
        { left: "\\(", right: "\\)", display: false }
      ],
      ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code", "option"],
      ignoredClasses: ["no-math"],
      throwOnError: false,
      errorColor: "#c0392b",
      macros: KATEX_MACROS,
      strict: "ignore"
    });
  }
  /* 窄畫面時，把仍然超出容器的獨立公式等比例縮小（最多縮到 72%），避免公式凸出版面 */
  function fitMath(root) {
    (root || document).querySelectorAll(".katex-display").forEach(function (el) {
      el.style.fontSize = "";
      var cw = el.clientWidth, sw = el.scrollWidth;
      if (cw > 0 && sw > cw + 1) el.style.fontSize = Math.max(0.72, (cw - 2) / sw).toFixed(3) + "em";
    });
  }
  document.addEventListener("toggle", function (e) { if (e.target.open) fitMath(e.target); }, true);
  var fitTimer;
  window.addEventListener("resize", function () { clearTimeout(fitTimer); fitTimer = setTimeout(function () { fitMath(document); }, 150); });

  function tex(str, display) {
    try { return window.katex.renderToString(str, { throwOnError: false, displayMode: !!display, macros: KATEX_MACROS, strict: "ignore" }); }
    catch (e) { return '<span class="math-err">' + str + "</span>"; }
  }

  /* 有伺服器時讀最新的檔案；直接雙擊 HTML（file://）或讀取失敗時，改用 assets/bundle.js 打包好的內容 */
  function fetchText(url) {
    var packed = window.STUDY_FILES && window.STUDY_FILES[url];
    if (APP && packed != null) return Promise.resolve(packed);  // 線上版：章節內容都打包在 bundle.js，不另外放檔案
    if (location.protocol === "file:") {
      return packed != null ? Promise.resolve(packed) : Promise.reject(new Error(url + "（未打包）"));
    }
    return fetch(url, { cache: "no-cache" }).then(function (r) {
      if (!r.ok) throw new Error(url + "（" + r.status + "）");
      return r.text();
    }).catch(function (e) {
      if (packed != null) return packed;
      throw e;
    });
  }
  function fetchJSON(url) { return fetchText(url).then(JSON.parse); }

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function fileProtocolHelp(err) {
    var local = location.protocol === "file:";
    return '<div class="error-box"><strong>內容載入失敗。</strong><br>' +
      (local ? "找不到打包好的內容（assets/bundle.js）。請在資料夾內執行 <code>python tools/build_bundle.py</code>，或改用 <code>Start.cmd</code> 開啟。"
             : "請確認檔案路徑存在：" + esc(err && err.message)) + "</div>";
  }

  /* ---------- 介面偏好：深淺色、字級 ---------- */
  function initPrefs() {
    var theme = store.get("theme", "");
    if (theme) document.documentElement.setAttribute("data-theme", theme);
    if (store.get("large", "0") === "1") document.body.classList.add("large");
    var tbtn = document.getElementById("btn-theme");
    if (tbtn) tbtn.addEventListener("click", function () {
      var cur = document.documentElement.getAttribute("data-theme");
      var dark = cur ? cur === "dark" : window.matchMedia("(prefers-color-scheme: dark)").matches;
      var next = dark ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      store.set("theme", next);
      document.dispatchEvent(new CustomEvent("themechange"));
    });
    var fbtn = document.getElementById("btn-font");
    if (fbtn) {
      fbtn.setAttribute("aria-pressed", document.body.classList.contains("large"));
      fbtn.addEventListener("click", function () {
        var on = document.body.classList.toggle("large");
        fbtn.setAttribute("aria-pressed", on);
        store.set("large", on ? "1" : "0");
      });
    }
  }

  /* ---------- 單頁版（放在 claude.ai 上的 app.html）：不換頁，用 #~科目~章~節~錨點 切換 ---------- */
  var APP = false;
  function chapterHref(sid, cid) { return APP ? "#~" + sid + "~" + cid : "chapter.html?s=" + encodeURIComponent(sid) + "&c=" + encodeURIComponent(cid); }
  function homeHref() { return APP ? "#home" : "index.html"; }
  function showView(name) {
    var home = document.getElementById("home-view"), chap = document.getElementById("chapter-view");
    if (home) home.hidden = name !== "home";
    if (chap) chap.hidden = name !== "chapter";
  }
  /* 解析路由：""／home → 首頁；~科目~章[~節[~錨點]]；單獨的錨點 → 目前章節（或預設章節）裡找 */
  function route(token) {
    token = token || "";
    if (!token || token === "home") {
      showView("home"); document.title = "讀懂物理"; initHome(); window.scrollTo(0, 0);
      document.dispatchEvent(new CustomEvent("study:page", { detail: { home: true } }));
      return;
    }
    var sid, cid, p, anchor;
    if (token.charAt(0) === "~") {
      var t = token.slice(1).split("~");
      sid = t[0]; cid = t[1]; p = t[2]; anchor = t[3];
    } else {
      sid = Chapter.sid || "mechanics"; cid = Chapter.cid || "ch01"; anchor = token;
    }
    showView("chapter");
    if (Chapter.sid === sid && Chapter.cid === cid && Chapter.ch) {
      if (!p && anchor) p = sectionOf(anchor);
      if (!p || !Chapter.html[p]) p = Chapter.overview;
      if (p === Chapter.page && anchor) { goTo(anchor); return; }
      Chapter.page = p;
      renderPage(p, anchor);
    } else initChapter(sid, cid, p, anchor);
  }
  function navigate(token) {
    try { history.pushState(null, "", "#" + token); } catch (e) { /* 無法改網址時仍可切換 */ }
    route(token);
  }

  /* ---------- 首頁 ---------- */
  function initHome() {
    var host = document.getElementById("subjects");
    fetchJSON("subjects/registry.json").then(function (reg) {
      host.innerHTML = reg.subjects.map(function (s) {
        var chapters = (s.chapters || []).map(function (c) {
          var ready = c.status === "ready";
          var link = ready ? '<a href="' + chapterHref(s.id, c.id) + '">' + esc(c.title) + "</a>" : "<span>" + esc(c.title) + "</span>";
          return "<li>" + link + '<span class="badge' + (ready ? " ready" : "") + '">' + (ready ? "可閱讀" : "待加入") + "</span>" +
            (c.range ? '<div class="small muted">' + esc(c.range) + "</div>" : "") + "</li>";
        }).join("");
        return '<article class="subject-card"><h2>' + esc(s.name) + "</h2>" +
          '<div class="meta">' + (s.teacher ? "授課：" + esc(s.teacher) + "<br>" : "") + (s.textbook ? "課本：" + esc(s.textbook) : "") + "</div>" +
          (chapters ? '<ul class="chapter-list">' + chapters + "</ul>" : '<p class="small muted">尚未加入章節。</p>') + "</article>";
      }).join("");
    }).catch(function (e) { host.innerHTML = fileProtocolHelp(e); });
  }

  /* ---------- 章節：總覽頁 + 每一節一頁（?p=節的 id） ---------- */
  var Chapter = { base: "", symbols: {}, steps: {}, exams: null, sections: [], html: {}, page: null };

  function pageURL(sec, hash) {
    if (APP) return "#~" + Chapter.sid + "~" + Chapter.cid + "~" + (sec || Chapter.overview) + (hash ? "~" + hash : "");
    var q = new URLSearchParams(location.search);
    if (sec && sec !== Chapter.overview) q.set("p", sec); else q.delete("p");
    return location.pathname + "?" + q.toString() + (hash ? "#" + hash : "");
  }
  /* 某個錨點在哪一節（連到別頁的題目、補充時用） */
  function sectionOf(id) {
    if (!id) return null;
    var needle = 'id="' + id + '"';
    for (var i = 0; i < Chapter.sections.length; i++) {
      var s = Chapter.sections[i];
      if (s.id === id || (Chapter.html[s.id] || "").indexOf(needle) >= 0) return s.id;
    }
    return null;
  }
  function lessons() { return Chapter.sections.filter(function (s) { return s.id !== Chapter.overview; }); }

  function initChapterFromURL() {
    var q = new URLSearchParams(location.search);
    var h = decodeURIComponent(location.hash.slice(1));
    initChapter(q.get("s"), q.get("c"), q.get("p"), h || null);
  }

  function initChapter(sid, cid, pIn, anchorIn) {
    var main = document.getElementById("reading");
    if (!sid || !cid || !/^[\w-]+$/.test(sid) || !/^[\w-]+$/.test(cid)) { main.innerHTML = '<div class="error-box">網址缺少科目或章節。<a href="' + homeHref() + '">回首頁</a></div>'; return; }
    main.innerHTML = '<p class="loading">載入章節中…</p>';
    Chapter.sid = sid; Chapter.cid = cid; Chapter.ch = null; Chapter.html = {}; Chapter.page = null;
    Chapter.base = "subjects/" + sid + "/" + cid + "/";
    Chapter.key = sid + ":" + cid;

    Promise.all([fetchJSON("subjects/registry.json"), fetchJSON(Chapter.base + "chapter.json")]).then(function (res) {
      var reg = res[0], ch = res[1];
      var subj = reg.subjects.filter(function (s) { return s.id === sid; })[0] || { name: sid };
      Chapter.ch = ch; Chapter.subj = subj; Chapter.sections = ch.sections;
      Chapter.overview = ch.overview || ch.sections[0].id;
      var crumbs = document.getElementById("crumbs");
      if (crumbs) crumbs.innerHTML = '<a href="' + homeHref() + '">科目</a> ／ ' + esc(subj.name) + ' ／ <a href="' + pageURL(Chapter.overview) + '">' + esc(ch.shortTitle) + "</a>";

      var parts = ch.sections.map(function (s) { return fetchText(Chapter.base + "sections/" + s.file); });
      parts.push(ch.stepSymbols ? fetchJSON(Chapter.base + ch.stepSymbols) : Promise.resolve({ symbols: {}, steps: {} }));
      parts.push(ch.exam ? fetchText(Chapter.base + ch.exam) : Promise.resolve(""));
      return Promise.all(parts).then(function (arr) {
        var examHTML = arr.pop(), sym = arr.pop();
        Chapter.symbols = sym.symbols || {}; Chapter.steps = sym.steps || {}; Chapter.symbolGroups = sym.groups || [];
        ch.sections.forEach(function (s, i) { Chapter.html[s.id] = arr[i]; });
        var holder = document.createElement("div");
        holder.innerHTML = examHTML;
        Chapter.exams = holder;

        // 只有 #錨點（舊網址）：自動換到該錨點所在的那一頁
        var p = pIn, h = anchorIn || "";
        if (!p && h && h.indexOf("exam=") !== 0) {
          var found = sectionOf(h);
          if (found && found !== Chapter.overview) {
            if (!APP) { location.replace(pageURL(found, h)); return; }
            p = found;
          }
        }
        if (!p || !Chapter.html[p]) p = Chapter.overview;
        Chapter.page = p;
        renderPage(p, h || null);
      });
    }).catch(function (e) { main.innerHTML = fileProtocolHelp(e); console.error(e); });
  }

  function renderPage(p, anchor) {
    var ch = Chapter.ch, main = document.getElementById("reading"), list = lessons();
    if (window.Study && Study.Exam) Study.Exam.close();
    if (p === Chapter.overview) {
      document.title = ch.shortTitle + "｜" + Chapter.subj.name + "｜讀懂物理";
      main.innerHTML = '<header class="page-head"><span class="eyebrow">' + esc(Chapter.subj.name) + " · " + esc(ch.range || "") + "</span><h1>" + esc(ch.title) + "</h1></header>" +
        '<section class="lesson overview" id="' + esc(p) + '">' + Chapter.html[p] + "</section>";
      buildSectionList(main, list);
      buildSymbolTable(main);
      var last = store.get("page:" + Chapter.key, "");
      var lastSec = list.filter(function (s) { return s.id === last; })[0];
      var lead = main.querySelector(".lead");
      if (lastSec && lead) lead.insertAdjacentHTML("afterend", '<p class="continue"><a href="' + pageURL(lastSec.id) + '">繼續上次讀到的：第 ' + (list.indexOf(lastSec) + 1) + " 節　" + esc(lastSec.title) + " →</a></p>");
    } else {
      var sec = list.filter(function (s) { return s.id === p; })[0], n = list.indexOf(sec);
      var tmp = document.createElement("div");
      tmp.innerHTML = Chapter.html[p];
      var h2 = tmp.querySelector("h2"), title = esc(sec.title);
      if (h2) {
        var pg = h2.querySelector(".pg"); if (pg) pg.remove();
        title = h2.innerHTML.trim().replace(/^[一二三四五六七八九十]+、/, "");
        h2.remove();
      }
      document.title = sec.title + "｜" + ch.shortTitle + "｜讀懂物理";
      var prev = n > 0 ? list[n - 1] : null, next = n < list.length - 1 ? list[n + 1] : null;
      var nav = '<nav class="lesson-nav" aria-label="上一節與下一節">' +
        (prev ? '<a class="prev" href="' + pageURL(prev.id) + '"><span class="dir">← 上一節</span>' + (n) + ". " + esc(prev.title) + "</a>"
              : '<a class="prev" href="' + pageURL(Chapter.overview) + '"><span class="dir">← 回到</span>本章總覽</a>') +
        (next ? '<a class="next" href="' + pageURL(next.id) + '"><span class="dir">下一節 →</span>' + (n + 2) + ". " + esc(next.title) + "</a>"
              : '<a class="next" href="' + pageURL(Chapter.overview) + '"><span class="dir">讀完了 →</span>回到本章總覽</a>') + "</nav>";
      main.innerHTML = '<header class="page-head"><span class="eyebrow">第 ' + (n + 1) + " 節 / 共 " + list.length + " 節 · " + pageTag(sec) + "</span><h1>" + title + "</h1></header>" +
        '<section class="lesson" id="' + esc(p) + '"></section>' + nav;
      var host = main.querySelector("section.lesson");
      while (tmp.firstChild) host.appendChild(tmp.firstChild);
      store.set("page:" + Chapter.key, p);
    }
    decorateProblems(main);
    // 跨章連結：<a data-chapter="科目/章" href="#卡片id">，依本機版或線上版換成正確網址；href 有錨點時保留（載入後自動找到所在的節）
    main.querySelectorAll("a[data-chapter]").forEach(function (l) {
      var sc = l.getAttribute("data-chapter").split("/"), h = l.getAttribute("href") || "";
      var anc = /^#[^~]/.test(h) ? h.slice(1) : "";
      l.setAttribute("href", chapterHref(sc[0], sc[1]) + (anc ? (APP ? "~~" + anc : "#" + anc) : ""));
    });
    sizeOriginals(main);
    pinStatements(main);
    initExamMode(main, p !== Chapter.overview);
    injectStepSymbols(main, true);
    buildVideos(main);
    renderMath(main);
    fitMath(main);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { fitMath(main); });
    buildTOC(p);
    initExamLinks(main);
    loadScripts((ch.scripts || []).map(function (s) { return Chapter.base + s; })).then(function () {
      if (window.Anim) window.Anim.mountAll(main);
    });
    restorePosition(anchor);
    document.dispatchEvent(new CustomEvent("study:page", { detail: { page: p } }));
  }

  /* ---------- 捲動時題目固定在上方：題目（含原題）跟著往下，直到這張題目卡結束；📌 可關閉，記在瀏覽器 ---------- */
  var pinState = { bound: false, list: [] };
  function pinStatements(root) {
    var on = store.get("pinq") !== "off";
    document.body.classList.toggle("pin-q", on);
    var hdr = document.querySelector(".site-header");
    function setHdr() { document.documentElement.style.setProperty("--hdr", (hdr ? hdr.offsetHeight : 0) + "px"); }
    setHdr();
    pinState.list = Array.prototype.slice.call(root.querySelectorAll(".problem>.pbody>.part.statement"));
    pinState.list.forEach(function (st) {
      if (st.querySelector(":scope>.pin-toggle")) return;
      var b = document.createElement("button");
      b.type = "button"; b.className = "pin-toggle";
      b.addEventListener("click", function () {
        var now = !document.body.classList.contains("pin-q");
        document.body.classList.toggle("pin-q", now);
        store.set("pinq", now ? "on" : "off");
        pinState.list.forEach(function (s) { s.classList.remove("stuck"); });
        st.scrollIntoView({ block: "nearest" });
      });
      st.insertBefore(b, st.firstChild);
      // 底部拖曳條：上下拖改固定區的高度（全站共用、記在瀏覽器），雙擊還原
      var g = document.createElement("div");
      g.className = "pin-grip"; g.title = "上下拖曳調整固定題目的高度；雙擊還原";
      g.addEventListener("pointerdown", function (e) {
        e.preventDefault();
        var y0 = e.clientY, h0 = st.getBoundingClientRect().height;
        g.setPointerCapture(e.pointerId);
        function move(ev) {
          var h = Math.max(70, Math.min(window.innerHeight * 0.85, h0 + ev.clientY - y0));
          document.documentElement.style.setProperty("--pinh", Math.round(h) + "px");
        }
        function up() {
          g.removeEventListener("pointermove", move); g.removeEventListener("pointerup", up); g.removeEventListener("pointercancel", up);
          store.set("pinh", document.documentElement.style.getPropertyValue("--pinh"));
        }
        g.addEventListener("pointermove", move); g.addEventListener("pointerup", up); g.addEventListener("pointercancel", up);
      });
      g.addEventListener("dblclick", function () { document.documentElement.style.removeProperty("--pinh"); store.set("pinh", ""); });
      st.appendChild(g);
    });
    var ph = store.get("pinh", "");
    if (ph) document.documentElement.style.setProperty("--pinh", ph);
    function mark() {  // 真的貼在上方時加陰影，看得出它蓋在詳解上面
      var top = (hdr ? hdr.offsetHeight : 0) + 6, pinned = document.body.classList.contains("pin-q");
      pinState.list.forEach(function (st) {
        var r = st.getBoundingClientRect(), card = st.parentNode.getBoundingClientRect();
        st.classList.toggle("stuck", pinned && Math.abs(r.top - top) < 2 && card.top < top - 4);
      });
    }
    if (!pinState.bound) {
      pinState.bound = true;
      var raf = 0;
      window.addEventListener("scroll", function () { if (!raf) raf = requestAnimationFrame(function () { raf = 0; mark(); }); }, { passive: true });
      window.addEventListener("resize", function () { setHdr(); mark(); });
    }
    mark();
  }

  /* ---------- 原題截圖：預設寬度（data-w）＋拖曳右下角自己調大小，記在瀏覽器，雙擊還原 ---------- */
  function sizeOriginals(root) {
    root.querySelectorAll(".original-image-link").forEach(function (a) {
      if (a.querySelector(".orig-grip")) return;
      var img = a.querySelector("img"), key = "origw:" + img.getAttribute("src");
      var base = +(a.getAttribute("data-w") || 0);
      function setW(w) { a.style.width = (w || base) ? Math.round(w || base) + "px" : ""; }
      setW(+store.get(key, 0));
      var g = document.createElement("span");
      g.className = "orig-grip";
      g.title = "拖曳調整大小，雙擊還原";
      a.appendChild(g);
      g.addEventListener("click", function (e) { e.preventDefault(); e.stopPropagation(); });
      g.addEventListener("dblclick", function (e) { e.preventDefault(); e.stopPropagation(); store.set(key, ""); setW(0); });
      g.addEventListener("pointerdown", function (e) {
        e.preventDefault(); e.stopPropagation();
        var x0 = e.clientX, w0 = a.getBoundingClientRect().width, max = a.parentNode.getBoundingClientRect().width;
        g.setPointerCapture(e.pointerId);
        a.classList.add("resizing");
        function move(ev) { setW(Math.max(80, Math.min(max, w0 + ev.clientX - x0))); }
        function up() {
          g.removeEventListener("pointermove", move); g.removeEventListener("pointerup", up); g.removeEventListener("pointercancel", up);
          a.classList.remove("resizing");
          store.set(key, String(Math.round(a.getBoundingClientRect().width)));
        }
        g.addEventListener("pointermove", move); g.addEventListener("pointerup", up); g.addEventListener("pointercancel", up);
      });
    });
  }

  var loadedScripts = {};
  function loadScripts(list) {
    return list.reduce(function (p, src) {
      return p.then(function () {
        if (loadedScripts[src]) return;  // 單頁版換節時不重複載入圖解
        loadedScripts[src] = true;
        return new Promise(function (ok) { var s = document.createElement("script"); s.src = src; s.onload = ok; s.onerror = ok; document.body.appendChild(s); });
      });
    }, Promise.resolve());
  }

  /* 題目的簡短標籤：例題 1.5、課本 1-12、練習 */
  /* 頁碼標籤：「講義 p.5–9」；節可用自己的 pageLabel 覆蓋全章設定（例如自編節設成空字串） */
  function pageTag(sec) {
    var label = sec.pageLabel != null ? sec.pageLabel : (Chapter.ch.pageLabel || "講義");
    return (label ? esc(label) + " " : "") + esc(sec.pages || "");
  }
  function problemLabel(p) {
    var kind = p.getAttribute("data-kind") || "example";
    var src = (p.querySelector("header .src") || {}).textContent || "";
    var chip = ((p.querySelector("header .chip") || {}).textContent || "").trim();
    if (kind === "self") return chip || "練習";  // 自編難題、自編綜合題、老師指定必考…照卡片上的標籤
    if (chip === "作業") { var hw = src.match(/(\d+\/\d+)\s*作業\s*第\s*(\d+)\s*題/); return "作業 " + (hw ? hw[1] + "-" + hw[2] : ""); }
    if (chip === "板書例題") { var bd = src.match(/(\d+\/\d+)/); return "板書例題" + (bd ? " " + bd[1] : ""); }
    if (kind === "textbook") { var m = src.match(/(\d+-\d+)/); return "課本 " + (m ? m[1] : ""); }
    if (kind === "exam") {
      var sem = src.match(/（(\d{2,3}[上下])）/), qn = src.match(/第\s*(\d+)\s*題/);
      if (sem && qn) return "考古 " + sem[1] + "-" + qn[1];
      var y = src.match(/(\d{3})\s*(?:學年|級)[^第]*第\s*(\d+)\s*題/); if (y) return "考古 " + y[1] + "-" + y[2];
      return qn ? "考古 " + (src.indexOf("某級") >= 0 ? "某級" : "") + "-" + qn[1] : "考古題";
    }
    if (kind === "tbexample") { var e = src.match(/Example\s*([\d.]+)/), sc = src.match(/§\s*([\d.]+)/); return e ? "課本例題 " + e[1] : "課本 §" + (sc ? sc[1] : ""); }
    var ex = src.match(/Example\s*([\d.]+)/), pg = src.match(/p\.(\d+)/);
    return "例題 " + (ex ? ex[1] : pg ? "p." + pg[1] : "");
  }

  /* 總覽頁：各節清單（標題、頁碼、一句話說明、本節題目） */
  function buildSectionList(root, list) {
    var host = root.querySelector("[data-section-list]");
    if (!host) return;
    host.outerHTML = '<ol class="section-list">' + list.map(function (s, i) {
      var tmp = document.createElement("div");
      tmp.innerHTML = Chapter.html[s.id];
      var probs = [].slice.call(tmp.querySelectorAll(".problem[id]")).map(function (p) {
        var h = p.querySelector("header h4, header h3");
        var tb = /^(textbook|tbexample|exam)$/.test(p.getAttribute("data-kind"));
        var vid = p.querySelector(".video[data-video]") ? '<span class="vid" title="有影片講解">▶影片</span>' : "";
        // 清單裡用小號的分式，避免某一題特別高
        var t = h ? h.innerHTML.replace(/\\displaystyle\s*/g, "").replace(/\\dfrac/g, "\\tfrac") : "";
        return '<a href="' + pageURL(s.id, p.id) + '"><span class="lab' + (tb ? " tb" : "") + '">' + esc(problemLabel(p)) + "</span>" + t + vid + "</a>";
      }).join("");
      return '<li><span class="n">' + (i + 1) + "</span><div>" +
        '<a class="t" href="' + pageURL(s.id) + '">' + esc(s.title) + '</a><span class="pages">' + pageTag(s) + "</span>" +
        (s.desc ? '<p class="d">' + s.desc + "</p>" : "") +
        (probs ? '<div class="probs">' + probs + "</div>" : "") + "</div></li>";
    }).join("") + "</ol>";
  }

  /* 題目卡：把考試寫法按鈕放進右上角的 actions */
  function decorateProblems(root) {
    root.querySelectorAll(".problem > header").forEach(function (hd) {
      if (hd.querySelector(".actions")) return;
      var act = document.createElement("div");
      act.className = "actions";
      var btn = hd.querySelector(".exam-btn");
      if (btn) { btn.textContent = "考試寫法"; act.appendChild(btn); }
      hd.appendChild(act);
      addSourceLink(hd.querySelector(".meta .src"));
    });
  }

  /* 側欄的課本題也附原文連結（來源文字取自正文題目卡；考古題在 exam.html 裡已寫好原卷連結） */
  var srcCache = {};
  function addExamSource(node, id) {
    if (node.querySelector(".src-link, a[href^='http']")) return;
    var k = Chapter.key + ":" + id;   // 不同章的題號可能相同
    if (!(k in srcCache)) {
      srcCache[k] = null;
      Object.keys(Chapter.html).some(function (sec) {
        if (Chapter.html[sec].indexOf('id="' + id + '"') < 0) return false;
        var d = document.createElement("div"); d.innerHTML = Chapter.html[sec];
        var sp = d.querySelector('[id="' + id + '"] header .src');
        if (sp) srcCache[k] = sp.textContent;
        return true;
      });
    }
    if (!srcCache[k]) return;
    var p = document.createElement("p"); p.className = "small src";
    p.textContent = "出處：" + srcCache[k];
    addSourceLink(p);
    if (p.querySelector(".src-link")) { var o = node.querySelector(".orig"); (o || node.firstChild).insertAdjacentElement("afterend", p); }
  }

  /* 原文連結：chapter.json 的 sources 依來源文字比對（先列的優先），連到自己雲端硬碟裡的原檔 */
  function addSourceLink(src) {
    var list = (Chapter.ch && Chapter.ch.sources) || [];
    if (!src || src.querySelector(".src-link")) return;
    var t = src.textContent;
    for (var i = 0; i < list.length; i++) {
      if (t.indexOf(list[i].match) >= 0) {
        var a = document.createElement("a");
        a.className = "src-link"; a.href = list[i].url; a.target = "_blank"; a.rel = "noopener";
        var pg = t.match(/p\.(\d+)/);   // 印刷頁碼 + pageOffset = PDF 頁碼
        var hasOff = typeof list[i].pageOffset === "number";
        var pdfPage = hasOff && pg ? +pg[1] + list[i].pageOffset : 0;
        // 雲端硬碟的檢視器不支援跳頁；本機雙擊版改開電腦上的 PDF，瀏覽器的 PDF 檢視器會直接跳到 #page=N
        if (location.protocol === "file:" && list[i].local) {
          a.href = "file:///" + encodeURI(list[i].local.replace(/\\/g, "/")) + (pdfPage ? "#page=" + pdfPage : "");
        }
        a.textContent = list[i].label + (pdfPage ? "（PDF 第 " + pdfPage + " 頁）" : "");
        src.appendChild(document.createTextNode(" · ")); src.appendChild(a);
        return;
      }
    }
  }

  /* 從 exam.html 取出某題的考試寫法（看到框、步驟、答案），給考試模式放在題目卡裡 */
  function examWriteup(id) {
    var src = id && Chapter.exams && Chapter.exams.querySelector('[data-exam-id="' + id + '"]');
    if (!src) return null;
    var box = document.createElement("div");
    box.className = "part exam-inline";
    box.innerHTML = '<span class="part-label">考試寫法</span>';
    Array.prototype.forEach.call(src.children, function (c) {
      if (c.matches(".rote, .write-q, ol.write, .final")) box.appendChild(c.cloneNode(true));
    });
    if (box.children.length < 2) return null;
    box.querySelectorAll("[id]").forEach(function (n) { n.setAttribute("data-id", n.id); n.removeAttribute("id"); });
    return box;
  }
  /* 考試寫法側欄：在英文原題下面放題目卡上的中文翻譯；原題本來就是中文的就不重複 */
  function examTranslation(id) {
    var html = null;
    Object.keys(Chapter.html).some(function (sec) {
      if (Chapter.html[sec].indexOf('id="' + id + '"') < 0) return false;
      var d = document.createElement("div"); d.innerHTML = Chapter.html[sec];
      var st = d.querySelector('[id="' + id + '"] .part.statement');
      if (!st) return true;
      var orig = st.querySelector(".original-text"), t = orig ? orig.textContent : "";
      var cjk = (t.match(/[一-鿿]/g) || []).length, lat = (t.match(/[A-Za-z]/g) || []).length;
      if (orig && cjk > lat) return true;   // 原題已經是中文
      st.querySelectorAll(".original-source, .part-label, .pin-toggle, .pin-grip").forEach(function (n) { n.remove(); });
      st.querySelectorAll("[id]").forEach(function (n) { n.removeAttribute("id"); });
      if (st.textContent.trim()) html = st.innerHTML;
      return true;
    });
    if (!html) return null;
    var box = document.createElement("div");
    box.className = "exam-trans";
    box.innerHTML = '<span class="part-label">中文翻譯</span>' + html;
    return box;
  }

  /* 考試模式：收起解說和圖，重點整理移到最上面，題目卡改顯示考試寫法，按了才顯示完整詳解 */
  function initExamMode(root, lesson) {
    var body = document.body;
    body.classList.remove("exam-mode");
    var probs = root.querySelectorAll(".problem");
    var head = root.querySelector(".page-head");
    if (!lesson || !probs.length || !head) return;
    var bar = document.createElement("div");
    bar.className = "mode-bar";
    bar.innerHTML = '<button type="button" class="mode-btn" aria-pressed="false">考試模式</button><span>只留原文公式、推導標題和題目；題目下面直接換成考試寫法，完整詳解按了才展開</span>';
    head.appendChild(bar);
    var key = root.querySelector("section.lesson > .box.key"), lead = root.querySelector("section.lesson > .lead");
    if (key) {
      var top = key.cloneNode(true);
      top.classList.add("key-top");
      if (lead) lead.insertAdjacentElement("afterend", top); else root.querySelector("section.lesson").prepend(top);
    }
    probs.forEach(function (pr) {
      // 考試模式時，題目下面直接放這題的考試寫法（看到／步驟／答案），原本的完整詳解收起來
      var wr = examWriteup(pr.id), st = pr.querySelector(".part.statement");
      if (wr && st) { st.insertAdjacentElement("afterend", wr); pr.classList.add("has-writeup"); }
      var after = wr || pr.querySelector(".part.plan") || st;
      if (!after) return;
      var label = wr ? ["顯示完整詳解", "收起完整詳解"] : ["顯示解法", "收起解法"];
      var b = document.createElement("button");
      b.type = "button"; b.className = "reveal-btn"; b.textContent = label[0];
      b.addEventListener("click", function () {
        var open = pr.classList.toggle("revealed");
        b.textContent = open ? label[1] : label[0];
        if (open) fitMath(pr);
      });
      after.insertAdjacentElement("afterend", b);
    });
    // 考試模式下，正文的推導只顯示標題，點標題才展開
    root.querySelectorAll("section.lesson > .step > .step-title").forEach(function (t) {
      t.addEventListener("click", function () {
        if (!body.classList.contains("exam-mode")) return;
        var st = t.parentNode;
        st.classList.toggle("open");
        if (st.classList.contains("open")) fitMath(st);
      });
    });
    var btn = bar.querySelector(".mode-btn");
    function apply(on) {
      body.classList.toggle("exam-mode", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
      fitMath(root);
    }
    btn.addEventListener("click", function () {
      var on = !body.classList.contains("exam-mode");
      store.set("examMode", on ? "1" : "0");
      apply(on);
    });
    apply(store.get("examMode", "0") === "1");
  }

  /* 影片：題目卡右上角一顆「▶ 影片講解」按鈕，按了才展開播放器 */
  function fmtTime(t) { t = Math.max(0, Math.floor(t)); return Math.floor(t / 60) + ":" + ("0" + t % 60).slice(-2); }
  function buildVideos(root) {
    root.querySelectorAll(".video[data-video]").forEach(function (host) {
      var id = host.getAttribute("data-video"), base = Chapter.base + "videos/" + id;
      var card = host.closest(".problem"), hd = card && card.querySelector(":scope > header");
      host.className = "video-block";
      host.hidden = true;
      if (hd) hd.insertAdjacentElement("afterend", host);
      fetchJSON(base + ".timeline.json").then(function (tl) {
        var btn = document.createElement("button");
        btn.type = "button"; btn.className = "video-btn";
        btn.setAttribute("aria-expanded", "false");
        btn.innerHTML = "▶ 影片講解 <span>" + fmtTime(tl.duration) + "</span>";
        var act = hd && hd.querySelector(".actions");
        if (act) act.insertBefore(btn, act.firstChild);
        btn.addEventListener("click", function () {
          var open = host.hidden;
          host.hidden = !open;
          btn.setAttribute("aria-expanded", open ? "true" : "false");
          btn.innerHTML = (open ? "✕ 收起影片 " : "▶ 影片講解 ") + "<span>" + fmtTime(tl.duration) + "</span>";
          var v = host.querySelector("video");
          if (open && !v) {
            var lines = tl.scenes.map(function (s) {
              return '<li><button type="button" class="t" data-seek="' + s.start + '">' + fmtTime(s.start) + "</button>" + s.sub + "</li>";
            }).join("");
            host.innerHTML = '<video controls preload="metadata" playsinline poster="' + base + '.jpg" src="' + base + '.mp4"></video>' +
              '<details><summary>逐字稿（點時間可跳轉）</summary><ol class="transcript">' + lines + "</ol></details>";
            renderMath(host);
            v = host.querySelector("video");
            host.addEventListener("click", function (e) {
              var b = e.target.closest("[data-seek]"); if (!b) return;
              v.currentTime = parseFloat(b.getAttribute("data-seek")); v.play();
            });
          }
          if (open && v) { var pr = v.play(); if (pr && pr.catch) pr.catch(function () {}); }
          if (!open && v) v.pause();
        });
      }).catch(function () { host.remove(); });
    });
  }

  function symbolLine(key) {
    var s = Chapter.symbols[key];
    if (!s) return "";
    return "<span>" + tex(s.tex) + "：" + esc(s.zh) + (s.unit ? "（" + esc(s.unit) + "）" : "") + "</span>";
  }

  function buildSymbolTable(root) {
    root.querySelectorAll("[data-symbol-table]").forEach(function (host) {
      var groups = Chapter.symbolGroups.length ? Chapter.symbolGroups : [{ title: "", keys: Object.keys(Chapter.symbols) }];
      host.innerHTML = groups.map(function (g) {
        var rows = g.keys.map(function (k) {
          var s = Chapter.symbols[k]; if (!s) return "";
          return "<tr><td>" + tex(s.tex) + "</td><td>" + esc(s.zh) + (s.en ? '<br><span class="muted small">' + esc(s.en) + "</span>" : "") + "</td><td>" + esc(s.unit || "—") + "</td><td>" + (s.note || "") + "</td></tr>";
        }).join("");
        return (g.title ? "<h4>" + esc(g.title) + "</h4>" : "") +
          '<div class="symbol-table-wrap"><table><thead><tr><th>符號</th><th>名稱</th><th>單位</th><th>注意</th></tr></thead><tbody>' + rows + "</tbody></table></div>";
      }).join("");
    });
  }

  /* 本步符號：同一頁中每個符號只在第一次用到的步驟提醒一次 */
  function injectStepSymbols(root, dedupe) {
    var seen = {};
    root.querySelectorAll("[data-step]").forEach(function (el) {
      var keys = el.getAttribute("data-sym");
      keys = keys ? keys.split(",") : (Chapter.steps[el.getAttribute("data-step")] || []);
      keys = keys.map(function (k) { return k.trim(); }).filter(function (k) {
        if (!dedupe) return true;
        if (seen[k]) return false;
        seen[k] = true; return true;
      });
      if (!keys.length) return;
      var line = document.createElement("div");
      line.className = "step-symbols";
      line.innerHTML = keys.map(symbolLine).join("");
      var title = el.querySelector(".step-title");
      if (title && title.parentNode === el) title.insertAdjacentElement("afterend", line); else el.insertBefore(line, el.firstChild);
    });
  }

  /* 目錄：各節（連到各頁）＋ 目前這一頁的小節 */
  function buildTOC(p) {
    var list = lessons(), subs = "";
    var h3s = [].slice.call(document.querySelectorAll("#reading section.lesson > h3[id]"));
    if (p !== Chapter.overview && h3s.length) {
      subs = '<ol class="sub">' + h3s.map(function (h) {
        var c = h.cloneNode(true); var t = c.querySelector(".pg-tag"); if (t) t.remove();
        return '<li><a href="#' + h.id + '" data-h="' + h.id + '">' + c.innerHTML.trim() + "</a></li>";
      }).join("") + "</ol>";
    }
    var items = list.map(function (s, i) {
      var cur = s.id === p;
      return '<li><a href="' + pageURL(s.id) + '"' + (cur ? ' class="active" aria-current="page"' : "") + '><span class="num">' + (i + 1) + "</span>" + esc(s.title) + "</a>" + (cur ? subs : "") + "</li>";
    }).join("");
    var side = document.getElementById("toc");
    if (side) {
      side.innerHTML = '<a class="toc-title" href="' + pageURL(Chapter.overview) + '">' + esc(Chapter.ch.shortTitle) + "</a><ol>" + items + "</ol>" +
        '<div class="toc-tools"><button type="button" id="btn-exam-index">✎ 全部考試寫法</button><a class="small" href="' + pageURL(Chapter.overview, "symbols") + '">符號總表</a></div>';
      renderMath(side);
    }
    var mob = document.getElementById("toc-mobile");
    if (mob) {
      var cur = list.filter(function (s) { return s.id === p; })[0];
      mob.innerHTML = "<details><summary>" + (cur ? "第 " + (list.indexOf(cur) + 1) + " 節：" + esc(cur.title) : "本章目錄") + "　▾</summary><ol>" +
        '<li><a href="' + pageURL(Chapter.overview) + '">本章總覽</a></li>' +
        list.map(function (s, i) { return '<li><a href="' + pageURL(s.id) + '"' + (s.id === p ? ' class="active"' : "") + ">" + (i + 1) + ". " + esc(s.title) + "</a></li>"; }).join("") + "</ol></details>";
    }
    var idx = document.getElementById("btn-exam-index");
    if (idx) idx.addEventListener("click", function () { Exam.index(); });

    if (!subs || !("IntersectionObserver" in window)) return;
    var links = {};
    document.querySelectorAll("#toc a[data-h]").forEach(function (a) { links[a.getAttribute("data-h")] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        Object.keys(links).forEach(function (k) { links[k].classList.toggle("here", k === en.target.id); });
      });
    }, { rootMargin: "-15% 0px -75% 0px" });
    h3s.forEach(function (h) { io.observe(h); });
  }

  function restorePosition(anchor) {
    var h = anchor != null ? anchor : (APP ? "" : decodeURIComponent(location.hash.slice(1)));
    if (h.indexOf("exam=") === 0) { Exam.open(h.slice(5)); return; }
    var target = h ? document.getElementById(h) : null;
    if (target) {
      openAncestors(target);
      setTimeout(function () { target.scrollIntoView(); flash(target); }, 80);
    } else if (APP) window.scrollTo(0, 0);
  }
  function openAncestors(el) {
    for (var p = el; p; p = p.parentElement) {
      if (p.tagName === "DETAILS") p.open = true;
      if (p.classList && p.classList.contains("step")) p.classList.add("open");  // 考試模式下收起的推導
      if (p !== el && p.classList && p.classList.contains("problem")) p.classList.add("revealed");  // 連到解法裡的某一步
    }
  }
  function flash(el) { el.classList.remove("flash"); void el.offsetWidth; el.classList.add("flash"); }

  /* 跳到某個錨點：在這一頁就捲過去；在別頁就換頁 */
  function goTo(id) {
    var t = document.getElementById(id);
    if (t) {
      openAncestors(t);
      t.scrollIntoView({ behavior: "smooth", block: "start" });
      if (!APP) history.replaceState(null, "", "#" + id);
      flash(t);
      return true;
    }
    var sec = sectionOf(id);
    if (sec) {
      if (APP) navigate(pageURL(sec, id).slice(1)); else location.href = pageURL(sec, id);
      return true;
    }
    return false;
  }
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest && ev.target.closest('a[href^="#"]');
    if (!a) return;
    var id = decodeURIComponent(a.getAttribute("href").slice(1));
    if (APP && (id === "home" || id.charAt(0) === "~")) { ev.preventDefault(); if (window.Study) Study.Exam.close(); navigate(id); return; }
    if (a.closest(".exam-sidebar")) return;
    if (id.indexOf("exam=") === 0) { ev.preventDefault(); Exam.open(id.slice(5)); return; }
    if (goTo(id)) ev.preventDefault();
  });

  /* ---------- 考試書寫版側欄 ---------- */
  var Exam = {
    stack: [],
    el: null,
    ensure: function () {
      if (this.el) return;
      var side = document.createElement("aside");
      side.className = "exam-sidebar";
      side.setAttribute("aria-label", "考試寫法");
      side.innerHTML = '<header><button type="button" class="back" hidden>← 返回</button><strong>考試寫法</strong><button type="button" class="list">目錄</button><button type="button" class="close" aria-label="關閉">✕ 關閉</button></header><div class="exam-body" tabindex="-1"></div>';
      document.body.appendChild(side);
      var scrim = document.createElement("div"); scrim.className = "scrim"; document.body.appendChild(scrim);
      this.el = side; this.scrim = scrim; this.body = side.querySelector(".exam-body");
      var self = this;
      side.querySelector(".close").addEventListener("click", function () { self.close(); });
      side.querySelector(".list").addEventListener("click", function () { self.index(); });
      side.querySelector(".back").addEventListener("click", function () { self.stack.pop(); var prev = self.stack.pop(); if (prev) self.open(prev.id, prev.anchor); });
      scrim.addEventListener("click", function () { self.close(); });
      document.addEventListener("keydown", function (e) { if (e.key === "Escape" && side.classList.contains("open")) self.close(); });
      this.body.addEventListener("click", function (ev) {
        var b = ev.target.closest("[data-exam]");
        if (b) { ev.preventDefault(); self.open(b.getAttribute("data-exam"), b.getAttribute("data-anchor")); return; }
        var a = ev.target.closest('a[href^="#"]');
        if (!a) return;
        var id = a.getAttribute("href").slice(1);
        var inside = self.body.querySelector('[data-id="' + id + '"]');
        ev.preventDefault();
        if (inside) { inside.scrollIntoView({ behavior: "smooth", block: "center" }); flash(inside); return; }
        self.close();
        goTo(id);
      });
    },
    show: function () {
      this.el.classList.add("open");
      if (window.matchMedia("(max-width:980px)").matches) this.scrim.classList.add("show");
      this.body.focus({ preventScroll: true });
    },
    open: function (id, anchor) {
      this.ensure();
      var src = Chapter.exams && Chapter.exams.querySelector('[data-exam-id="' + id + '"]');
      if (!src) { this.body.innerHTML = '<p class="muted">找不到這份考試寫法（' + esc(id) + "）。</p>"; this.show(); return; }
      var node = src.cloneNode(true);
      // 在側欄內改用 data-id，避免與正文錨點重複
      node.querySelectorAll("[id]").forEach(function (n) { n.setAttribute("data-id", n.id); n.removeAttribute("id"); });
      this.body.innerHTML = "";
      this.body.appendChild(node);
      var tr = examTranslation(id), os = node.querySelector(".orig .original-source");
      if (tr) { if (os) os.insertAdjacentElement("afterend", tr); else (node.querySelector(".orig") || node.firstChild).insertAdjacentElement("beforebegin", tr); }
      addExamSource(node, id);
      sizeOriginals(this.body);
      injectStepSymbols(this.body, true);
      renderMath(this.body);
      this.stack.push({ id: id, anchor: anchor });
      this.el.querySelector(".back").hidden = this.stack.length < 2;
      this.show();
      fitMath(this.body);
      var body = this.body;
      if (anchor) {
        var t = body.querySelector('[data-id="' + anchor + '"]');
        if (t) setTimeout(function () { t.scrollIntoView({ block: "center" }); flash(t); }, 80);
      } else body.scrollTop = 0;
      if (!APP) history.replaceState(null, "", "#exam=" + id);
      document.dispatchEvent(new CustomEvent("study:exam-open"));
    },
    index: function () {
      this.ensure();
      var items = Chapter.exams ? Chapter.exams.querySelectorAll("[data-exam-id]") : [];
      var html = '<h3>本章全部考試寫法</h3><p class="small muted">每份都先列完整題目，再列可直接寫在考卷上的作答。</p><ul class="exam-index">';
      var lastGroup = "";
      items.forEach(function (it) {
        var g = it.getAttribute("data-group") || "";
        if (g && g !== lastGroup) { html += '<li class="grp">' + esc(g) + "</li>"; lastGroup = g; }
        html += '<li><button type="button" data-exam="' + it.getAttribute("data-exam-id") + '">' + (it.getAttribute("data-title") || it.getAttribute("data-exam-id")) + "</button></li>";
      });
      this.body.innerHTML = html + "</ul>";
      renderMath(this.body);
      this.stack = [];
      this.el.querySelector(".back").hidden = true;
      this.show();
      document.dispatchEvent(new CustomEvent("study:exam-open"));
    },
    close: function () {
      if (!this.el) return;
      this.el.classList.remove("open"); this.scrim.classList.remove("show");
      this.stack = [];
      if (!APP && location.hash.indexOf("#exam=") === 0) history.replaceState(null, "", location.pathname + location.search);
    }
  };

  function initExamLinks(root) {
    if (root._examLinks) return;  // 單頁版裡 #reading 一直存在，只綁一次
    root._examLinks = true;
    root.addEventListener("click", function (ev) {
      var b = ev.target.closest("[data-exam]");
      if (!b) return;
      ev.preventDefault();
      Exam.stack = [];
      Exam.open(b.getAttribute("data-exam"), b.getAttribute("data-anchor"));
    });
  }

  window.Study = {
    renderMath: renderMath, fitMath: fitMath, tex: tex, esc: esc, store: store, Exam: Exam,
    Chapter: Chapter, lessons: lessons, problemLabel: problemLabel, navigate: function (t) { navigate(t); },
    isApp: function () { return APP; }
  };

  function start() {
    initPrefs();
    var root = document.getElementById("app-root");
    if (root) {
      APP = true;
      document.documentElement.lang = "zh-Hant";
      window.addEventListener("popstate", function () { route(decodeURIComponent(location.hash.slice(1))); });
      route(decodeURIComponent(location.hash.slice(1)));
      return;
    }
    var page = document.body.getAttribute("data-page");
    if (page === "home") initHome();
    if (page === "chapter") initChapterFromURL();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
