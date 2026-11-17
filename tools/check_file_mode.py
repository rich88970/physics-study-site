"""確認不開伺服器、直接雙擊 HTML（file://）時每一頁都能載入：章節、圖解、考試寫法側欄、影片按鈕。

用法：python tools/check_file_mode.py [mechanics/ch01]
"""
import asyncio
import io
import json
import os
import sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(__file__))
from cdp import Browser  # noqa: E402
from build_bundle import ROOT, build  # noqa: E402

CH = sys.argv[1] if len(sys.argv) > 1 else "mechanics/ch01"
S, C = CH.split("/")
FILE = "file:///" + quote(ROOT.replace(os.sep, "/"), safe="/:")
READY = "!!document.querySelector('.page-head h1, .subject-card, .error-box')"
CHECK = """(async function(){
  await new Promise(function(r){setTimeout(r,1500)});
  var o={err:!!document.querySelector('.error-box'), title:(document.querySelector('.page-head h1')||{}).textContent||'',
    problems:document.querySelectorAll('.problem').length, figures:document.querySelectorAll('.anim.figure').length,
    katexErr:document.querySelectorAll('.katex-error').length, videos:document.querySelectorAll('.video-btn').length};
  var b=document.querySelector('.problem .exam-btn');
  if(b){b.click(); await new Promise(function(r){setTimeout(r,200)});
    var body=document.querySelector('.exam-sidebar .exam-body'); o.examOK=!!body && !/找不到/.test(body.textContent) && body.textContent.length>40;}
  return o;})()"""


async def main():
    sys.stdout.reconfigure(encoding="utf-8")
    n, _ = build()
    chapter = json.load(io.open(os.path.join(ROOT, "subjects", S, C, "chapter.json"), encoding="utf-8"))
    pages = [None] + [s["id"] for s in chapter["sections"] if s["id"] != chapter.get("overview")]
    out, ok = {}, True
    async with Browser(1280, 900, port=9420) as b:
        await b.goto(FILE + "/index.html", ready_js=READY)
        home = await b.eval("(async function(){await new Promise(function(r){setTimeout(r,800)});return {err:!!document.querySelector('.error-box'),cards:document.querySelectorAll('.subject-card').length}})()")
        out["home"] = home
        ok &= (not home["err"]) and home["cards"] > 0
        for p in pages:
            url = f"{FILE}/chapter.html?s={S}&c={C}" + (f"&p={p}" if p else "")
            await b.goto(url, ready_js=READY)
            r = await b.eval(CHECK)
            out[p or "overview"] = r
            ok &= (not r["err"]) and r["katexErr"] == 0 and r.get("examOK", True)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"打包 {n} 個檔案；" + ("FILE MODE OK" if ok else "FILE MODE FAILED"))


asyncio.run(main())
