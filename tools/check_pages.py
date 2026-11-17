"""逐頁檢查章節網站（需先啟動伺服器）：公式錯誤、橫向溢出、圖解每一步、舊網址轉頁、側欄跨頁連結、影片按鈕。

用法：python tools/check_pages.py [mechanics/ch01]
"""
import asyncio
import json
import sys

sys.path.insert(0, __import__("os").path.dirname(__file__))
from cdp import Browser  # noqa: E402
from build_bundle import build  # noqa: E402

build()  # 先更新 assets/bundle.js，讓直接雙擊 HTML 時看到的內容也是最新的

CH = sys.argv[1] if len(sys.argv) > 1 else "mechanics/ch01"
S, C = CH.split("/")
BASE = f"http://127.0.0.1:8642/chapter.html?s={S}&c={C}"
# 各章用來測導覽的題目：(舊網址錨點, 它所在的節, 側欄測試題, 它所在的節, 有沒有影片)
NAV = {"mechanics/ch01": ("tm-1-12", "s05", "ex-p49", "s09", True),
       "modern/ch01": ("kg-107-3", "s09", "kg-107-4", "s11", False),
       "modern/ch02": ("kg-107-7", "s07", "kg-107-8", "s08", False),
       "thermal/ch02": ("tk-115-5", "s03", "tk-115-6", "s06", False),
       "mechanics/ch02": ("c2-tm-2-25", "s14", "c2-ex29", "s10", False)}
A1, P1, A2, P2, HAS_VIDEO = NAV.get(CH, (None, None, None, None, False))  # 不在表裡的章：跳過導覽測試
READY = "!!document.querySelector('.page-head h1') && document.fonts.status==='loaded'"

PAGE_CHECK = """(async function(){
  await new Promise(function(r){setTimeout(r,1200)});
  var out={};
  var cw=document.documentElement.clientWidth;
  out.hOverflow=document.documentElement.scrollWidth>cw+1;
  out.katexErr=[].map.call(document.querySelectorAll('.katex-error'),function(e){return e.title}).slice(0,3);
  document.querySelectorAll('details').forEach(function(d){d.open=true});
  await new Promise(function(r){setTimeout(r,300)});
  out.mathOverflow=[].filter.call(document.querySelectorAll('#reading .katex-display'),function(e){return e.scrollWidth>e.clientWidth+2}).length;
  out.mathTiny=[].filter.call(document.querySelectorAll('#reading .katex-display'),function(e){return e.style.fontSize&&parseFloat(e.style.fontSize)<0.85}).length;
  document.querySelectorAll('details').forEach(function(d){d.open=false});
  var anims=document.querySelectorAll('.anim'), bad=[];
  anims.forEach(function(h){var p=h._player; if(!p){bad.push(h.dataset.anim+':unmounted');return;}
    try{for(var i=0;i<p.def.steps.length;i++){p.jump(i);var f=h.querySelector('.fig-formula');
      if(f.scrollWidth>f.clientWidth+2) bad.push(h.dataset.anim+'#'+(i+1)+':formula overflow');
      if(h.querySelector('.katex-error')) bad.push(h.dataset.anim+'#'+(i+1)+':katex');}
      p.jump(0);}catch(e){bad.push(h.dataset.anim+':'+e.message)}});
  out.figures=anims.length; out.figureProblems=bad;
  out.problems=document.querySelectorAll('.problem').length;
  out.examButtons=document.querySelectorAll('.problem .exam-btn').length;
  out.videoButtons=document.querySelectorAll('.video-btn').length;
  out.nav=!!document.querySelector('.lesson-nav');
  return out;})()"""


async def check_pages(width):
    results = {}
    async with Browser(width, 900, port=9360 if width > 600 else 9361) as b:
        await b.goto(BASE, ready_js=READY)
        pages = await b.eval("Array.from(document.querySelectorAll('.section-list a.t')).map(function(a){return a.getAttribute('href')})")
        results["overview"] = await b.eval(PAGE_CHECK)
        for href in pages:
            await b.goto("http://127.0.0.1:8642" + href, ready_js=READY)
            await asyncio.sleep(0.8)
            await b.eval("new Promise(function(r){var n=0;(function w(){var a=document.querySelectorAll('.anim');if((a.length&&[].every.call(a,function(h){return h._player}))||n++>40)r();else setTimeout(w,100)})()})")
            results[href.split("p=")[-1]] = await b.eval(PAGE_CHECK)
    return results


async def check_navigation():
    out = {}
    if A1 is None:
        return out
    async with Browser(1280, 900, port=9362) as b:
        # 舊網址只有 #錨點 → 換到所在那一頁
        await b.goto(BASE + "#" + A1, ready_js=READY)
        await asyncio.sleep(1.0)
        out["oldLinkRedirect"] = await b.eval(f"location.search.indexOf('p={P1}')>=0 && location.hash==='#{A1}' && Math.abs(document.getElementById('{A1}').getBoundingClientRect().top)<200")
        # 影片按鈕：展開後出現播放器、讀得到片長
        if HAS_VIDEO: out["videoButton"] = await b.eval("""(async function(){var b=document.querySelector('#tm-1-12 .video-btn'); if(!b) return 'no button';
            b.click(); await new Promise(function(r){setTimeout(r,800)}); var v=document.querySelector('#tm-1-12 video'); if(!v) return 'no video';
            v.muted=true; await new Promise(function(r){if(v.readyState>=1)r();else{v.addEventListener('loadedmetadata',r,{once:true});setTimeout(r,4000)}});
            return {duration:v.duration, w:v.videoWidth, transcript:document.querySelectorAll('#tm-1-12 .transcript li').length, expanded:b.getAttribute('aria-expanded')};})()""")
        # 側欄「回到正文詳解」：從總覽頁開側欄，點連結應該換到該題所在的頁
        await b.goto(BASE + "#exam=" + A2, ready_js=READY)
        await asyncio.sleep(1.0)
        await b.eval("(function(){var a=document.querySelector('.exam-body a[href=\"#%s\"]'); if(a) a.click();})()" % A2)
        await asyncio.sleep(2.0)
        out["sidebarCrossPage"] = await b.eval(f"location.search.indexOf('p={P2}')>=0 && location.hash==='#{A2}'")
        # 總覽頁的「符號總表」錨點
        await b.goto(BASE + "&p=s03", ready_js=READY)
        await asyncio.sleep(0.6)
        await b.eval("(function(){var a=[].filter.call(document.querySelectorAll('#toc a'),function(x){return x.textContent==='符號總表'})[0]; if(a) a.click();})()")
        await asyncio.sleep(2.0)
        out["symbolsLink"] = await b.eval("!location.search.match(/p=/) && location.hash==='#symbols' && document.getElementById('symbols').open===true")
    return out


async def main():
    report = {"mobile390": await check_pages(390), "desktop1280": await check_pages(1280), "navigation": await check_navigation()}
    print(json.dumps(report, ensure_ascii=False, indent=1))
    print("手機寬度下被縮小到 85% 以下的公式數：",
          ", ".join(f"{p}={r['mathTiny']}" for p, r in report["mobile390"].items()))
    problems = []
    for mode in ("mobile390", "desktop1280"):
        for page, r in report[mode].items():
            if r["hOverflow"] or r["katexErr"] or r["mathOverflow"] or r["figureProblems"]:
                problems.append(f"{mode} {page}: {r}")
    for k, v in report["navigation"].items():
        if v is not True and not isinstance(v, dict):
            problems.append(f"navigation {k}: {v}")
    print("PROBLEMS:" if problems else "ALL PAGES OK", *problems, sep="\n")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(main())
