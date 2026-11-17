"""靜態檢查章節 HTML 與原題 manifest（不需伺服器）。

抓 KaTeX 不會報錯、但畫面會壞掉的情況：
1. 控制字元：Python 字串裡的 "\t"、"\f"、"\b"、"\v"、"\a" 把 \theta、\frac、\beta、\vec、\alpha 吃掉
   （例如顯示成「 heta」）。
2. 數學式裡裸露的 `<` 被瀏覽器當成 HTML 標籤，後面的文字消失（應寫 \lt）。

用法：python tools/lint_static.py   有問題時結束碼為 1。
"""
import glob
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
KNOWN = set("""a abbr article aside b blockquote br button caption code col colgroup dd details div dl dt em
figcaption figure footer h1 h2 h3 h4 h5 h6 header hr i img li main mark nav ol p pre q s section small span
strong sub summary sup table tbody td th thead tr u ul video source svg path g line circle rect text polyline
polygon defs marker tspan ellipse use script style kbd var del ins wbr label input select option canvas""".split())


class TagScan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.bad = []

    def handle_starttag(self, tag, attrs):
        if tag not in KNOWN:
            self.bad.append((tag[:30], self.getpos()[0]))


def main():
    problems = []
    files = [f for f in glob.glob(os.path.join(ROOT, "subjects", "*", "*", "**", "*.html"), recursive=True) if "_template" not in f]
    for f in sorted(files):
        rel = os.path.relpath(f, ROOT)
        s = open(f, encoding="utf-8").read()
        for n, line in enumerate(s.splitlines(), 1):
            # 行內的 Tab 只有夾在文字中間才算（縮排用的 Tab 不算）
            body = line.lstrip("\t ")
            if CTRL.search(body) or "\t" in body:
                problems.append(f"{rel}:{n} 控制字元或 Tab：{body.strip()[:80]!r}")
        p = TagScan()
        p.feed(s)
        for tag, n in p.bad:
            problems.append(f"{rel}:{n} 不明標籤 <{tag}>（數學式裡的 < 要寫 \\lt）")
    for f in sorted(glob.glob(os.path.join(ROOT, "assets", "originals", "manifest", "*.json"))):
        for k, v in json.load(open(f, encoding="utf-8")).items():
            for field in ("text", "note", "label", "source"):
                t = v.get(field) or ""
                if CTRL.search(t) or "\t" in t:
                    problems.append(f"{os.path.basename(f)} {k}.{field} 控制字元或 Tab：{t[:80]!r}")
    for line in problems:
        print(line)
    print(f"lint_static：{len(files)} 個 HTML，問題 {len(problems)} 個")
    return 1 if problems else 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
