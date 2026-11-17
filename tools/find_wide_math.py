"""列出手機寬度下被縮小（<85%）或仍然溢出的獨立公式原始碼，方便拆行。

用法：python tools/find_wide_math.py s11 s12 ...   （需先啟動伺服器）
"""
import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from cdp import Browser  # noqa: E402

BASE = "http://127.0.0.1:8642/chapter.html?s=mechanics&c=ch01&p="
READY = "!!document.querySelector('.page-head h1') && document.fonts.status==='loaded'"
JS = """(async function(){
  await new Promise(function(r){setTimeout(r,1200)});
  document.querySelectorAll('details').forEach(function(d){d.open=true});
  await new Promise(function(r){setTimeout(r,300)});
  return [].filter.call(document.querySelectorAll('#reading .katex-display'),function(e){
    return (e.style.fontSize&&parseFloat(e.style.fontSize)<0.85)||e.scrollWidth>e.clientWidth+2;
  }).map(function(e){var a=e.querySelector('annotation');return (e.style.fontSize||'1')+' | '+(a?a.textContent:'').slice(0,160);});
})()"""


async def main():
    sys.stdout.reconfigure(encoding="utf-8")
    async with Browser(390, 844, port=9440) as b:
        for p in sys.argv[1:]:
            await b.goto(BASE + p, ready_js=READY)
            for line in await b.eval(JS):
                print(p, line)


asyncio.run(main())
