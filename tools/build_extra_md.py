"""把使用者提供的整理講義 Markdown 轉成網站的「額外章」（不改內容，只改排版）。
目前用在：光學「考古題同類題完整詳解」（optics/kaogu）、應用數學「考古題與作業完整解題」（applied-math/kaogu）。
- 依最上層標題（# …）切成一節一頁，## 變 h3（目錄）、### 變 h4、#### 變 h5；
- 公式（$…$、$$…$$、\\(…\\)、\\[…\\]）先抽出來保護，轉完 Markdown 再原樣放回（只把 < > & 換成 HTML 實體，顯示不變）；
- 表格包在可左右捲動的框裡、引言變成提示框、外部連結另開分頁；
- 以「符號：」開頭的段落（公式下面的符號說明）用小字灰色顯示；
- 以「公式（名稱）：」開頭的段落（該步用到的一般公式）用框起來的提示顯示。
用法：python tools/build_extra_md.py optics|applied-math
"""
import html
import json
import re

import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]

CONFIGS = {
    "optics": {
        "src": "tools/sources/optics-kaogu.md",
        "out": "subjects/optics/kaogu",
        "intro_title": "總覽：老師逐字稿與考古題對照",
        "lead": "這一章是另外整理的考古題同類題教學，相同題型放在一起、逐年比較；內容照原文件，只改成網站排版，並在公式下補上符號說明。",
        "title": "考古題同類題完整詳解（112、114、115 級）",
        "short": "光學 考古題詳解",
        "range": "李孟恩近代光學 112、114、115 級下學期期中考：波的疊加、平面電磁波、干涉逐年比較，另加 2018、2020 舊考古與課本補強題（球面波、圓柱波、對比度、楊氏干涉、群速度、能量密度）",
        "tutor": "你是「讀懂物理」讀書網站裡的 AI 助教。對象是台灣的大學物理系學生，正在準備「光學」（李孟恩老師，範圍講義第八～十章）的考試。這一頁是 112、114、115 級下學期近代光學期中考的同類題完整詳解：第 1 題同頻率波的疊加（合成振幅與相位、象限判斷）、第 2 題平面電磁波完整表示（$\\vec E$、$\\vec B$、瞬時 Poynting 向量、照度）、第 3 題干涉（菲涅耳雙稜鏡、牛頓環），以及補強題：2020 期中球面電磁波、課本 4-18／4-19（照度與場振幅、圓柱波 $1/\\sqrt r$）、2018 期中對比度與楊氏干涉加薄片、課本 7-1／7-6、2020 期中群速度、電磁波能量密度與都卜勒效應。",
        "desc": {
            "A 組": "四個同頻率波合成振幅與相位；112、114、115 級逐題展開。",
            "B 組": "$\\vec E$、$\\vec B$、瞬時 Poynting 向量與照度；三年份逐題。",
            "C 組": "112 級雙稜鏡、114 級雙波長牛頓環、115 級亮暗牛頓環。",
            "E 組": "核對用的答案總表與三份電磁波題的相位、方向。",
            "F 組": "作答骨架與三年數值代入重點。",
            "G 組": "老師提到但這三份沒考的範圍、最後的複習順序。",
            "H 組": "舊考古（2018、2020）與課本補強題的來源、優先順序與符號表。",
        },
        "h_anchor": True,
    },
    "applied-math": {
        "src": "tools/sources/applied-math-kaogu.md",
        "out": "subjects/applied-math/kaogu",
        "intro_title": "總覽與主題目錄",
        "lead": "這一章是另外整理的 2021–2025 期中考古題與歷次作業完整解題，依主題重新排列；內容照原文件，只改成網站排版，並驗算、在公式下補上符號說明。",
        "title": "考古題與作業完整解題（依主題）",
        "short": "應數 考古與作業詳解",
        "range": "2021–2025 期中考古題與作業一～五的完整解題，依主題排列：一階（可分離、線性、恰當）、二階齊次、降階法、未定係數法、冪級數、Frobenius、Fourier 級數",
        "tutor": "你是「讀懂物理」讀書網站裡的 AI 助教。對象是台灣的大學物理系學生，正在準備「應用數學」的期中考。這一頁是 2021–2025 年期中考古題與作業一～五的完整解題，依主題排列：一階 ODE（可分離變數、線性方程與積分因子、恰當方程與積分因子）、二階齊次常係數、降階法、二階非齊次（未定係數法的 sum／multiplication／modification rule、初值問題）、冪級數解、Frobenius 法、Fourier 級數（實數、複數 Fourier、功率頻譜）。",
        "desc": {},
        "h_anchor": False,
    },
}


def protect_math(text):
    store = []

    def keep(m):
        store.append(m.group(0))
        return f"MATHPH{len(store) - 1}X"

    text = re.sub(r"\$\$.+?\$\$", keep, text, flags=re.S)
    text = re.sub(r"\\\[.+?\\\]", keep, text, flags=re.S)
    text = re.sub(r"\\\(.+?\\\)", keep, text)
    text = re.sub(r"(?<!\\)\$[^\n$]+?(?<!\\)\$", keep, text)
    return text, store


def restore_math(h, store):
    def back(m):
        tex = store[int(m.group(1))]
        return tex.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    h = re.sub(r"<p>\s*(MATHPH\d+X)\s*</p>", lambda m: '<div class="math-block">' + m.group(1) + "</div>", h)
    return re.sub(r"MATHPH(\d+)X", back, h)


def to_html(md_text, prefix, h_anchor):
    text, store = protect_math(md_text)
    h = markdown.markdown(text, extensions=["tables", "sane_lists"])
    n = [0]

    def h2(m):
        n[0] += 1
        return f'<h3 id="{prefix}-{n[0]}">{m.group(1)}</h3>'
    h = re.sub(r"<h4>(.*?)</h4>", r"<h5>\1</h5>", h)
    h = re.sub(r"<h3>(.*?)</h3>", r"<h4>\1</h4>", h)
    h = re.sub(r"<h2>(.*?)</h2>", h2, h)
    h = re.sub(r"<table>", '<div class="symbol-table-wrap"><table>', h).replace("</table>", "</table></div>")
    h = re.sub(r"<blockquote>\s*", '<div class="box idea">', h).replace("</blockquote>", "</div>")
    h = re.sub(r'<a href="(https?://[^"]+)">', r'<a href="\1" target="_blank" rel="noopener">', h)
    if h_anchor:
        h = re.sub(r'<a href="#h-[^"]*">', '<a href="#kp-h">', h)   # 光學文件裡連到「H 組」標題的錨點
    h = h.replace("<p>符號：", '<p class="symnote">符號：')
    h = re.sub(r"<p>(公式（[^）]*）：)", r'<p class="fnote"><b>\1</b>', h)   # 補上的「用到的公式」
    h = h.replace("<hr />", "")
    return restore_math(h, store)


def split_top(md):
    parts, cur, in_math = [], [], False
    for ln in md.split("\n"):
        s = ln.strip()
        if s in ("$$", "\\[", "\\]") or (s.startswith("$$") and s.count("$$") == 1) or (s.endswith("$$") and s.count("$$") == 1 and not s.startswith("$$")):
            in_math = not in_math
        if not in_math and re.match(r"^# ", ln):
            parts.append(cur)
            cur = [ln]
        else:
            cur.append(ln)
    parts.append(cur)
    return parts


def build(key):
    cfg = CONFIGS[key]
    out = ROOT / cfg["out"]
    md = (ROOT / cfg["src"]).read_text(encoding="utf-8")
    parts = split_top(md)
    title_line, intro = parts[1][0], parts[1][1:]
    groups = parts[2:]
    out.joinpath("sections").mkdir(parents=True, exist_ok=True)
    for old in out.joinpath("sections").iterdir():   # 這一章的頁面全部由本腳本產生（只清檔案，資料夾被占用也不會失敗）
        if old.is_file():
            old.unlink()

    sections = [{"id": "s00", "file": "00-intro.html", "title": cfg["intro_title"], "pages": ""}]
    doc_title = title_line[2:].strip()
    out.joinpath("sections", "00-intro.html").write_text(
        f'<h2>{cfg["intro_title"]}</h2>\n<p class="lead">{html.escape(doc_title)}。{cfg["lead"]}</p>\n'
        + to_html("\n".join(intro), "k0", cfg["h_anchor"]) + '\n<div data-section-list></div>\n', encoding="utf-8")
    for i, g in enumerate(groups, 1):
        heading = g[0][2:].strip()
        sid, fname = f"s{i:02d}", f"{i:02d}-part.html"
        hid = ' id="kp-h"' if cfg["h_anchor"] and heading.startswith("H 組") else f' id="kp-{i:02d}"'
        text, store = protect_math(heading)
        page = f"<h2{hid}>{restore_math(html.escape(text), store)}</h2>\n" + to_html("\n".join(g[1:]), f"k{i:02d}", cfg["h_anchor"])
        out.joinpath("sections", fname).write_text(page, encoding="utf-8")
        entry = {"id": sid, "file": fname, "title": re.sub(r"（[^）]*分）$", "", heading), "pages": ""}
        for k, v in cfg["desc"].items():
            if heading.startswith(k):
                entry["desc"] = v
        sections.append(entry)

    chapter = {
        "title": cfg["title"], "shortTitle": cfg["short"], "range": cfg["range"], "pageLabel": "考古",
        "tutorIntro": cfg["tutor"], "overview": "s00", "sections": sections, "sources": [], "scripts": [],
    }
    out.joinpath("chapter.json").write_text(json.dumps(chapter, ensure_ascii=False, indent=2), encoding="utf-8")

    reg_p = ROOT / "subjects" / "registry.json"
    reg = json.loads(reg_p.read_text(encoding="utf-8"))
    subj = next(s for s in reg["subjects"] if s["id"] == key)
    ent = next((c for c in subj["chapters"] if c["id"] == "kaogu"), None)
    if ent is None:
        ent = {"id": "kaogu"}
        subj["chapters"].append(ent)
    ent.update({"title": cfg["title"], "range": cfg["range"], "status": "ready"})
    reg_p.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")
    print("完成：", out, "；節數", len(sections))
    for s in sections:
        print(" ", s["id"], s["title"])


if __name__ == "__main__":
    build(sys.argv[1])
