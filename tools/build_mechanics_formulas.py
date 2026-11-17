"""把 tools/sources/mechanics-formulas.md 轉成力學的「公式表」章（subjects/mechanics/formulas）。

來源格式（自訂，比 HTML 好寫）：
- `# s01 | 01-vectors.html | 一、標題 | Lecture 1 §1–5 | 節的簡介`：開新的一節（一頁）；
- `## 1.1 小標 {#fx-xxx}`：節裡的小標（h3，進目錄）；
- `### 公式名稱 | ch01#錨點`：一張公式卡，右上角連到講義那一段（可寫 `ch02#c2-ex26=例題 2.6` 自訂標籤）；
- 卡片內容：`$$…$$` 是公式；「符號：」開頭的段落是符號說明（小字灰底）；其他段落是說明；`**粗體**` 照用。
第一節之前的文字是總覽頁（s00）的內容，原樣當 HTML 放進去。
連結標籤（例如「L1 §4.1」）由錨點所在的講義小標自動算出，講義改了小標編號重跑一次即可。
用法：python tools/build_mechanics_formulas.py
"""
import html
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "tools" / "sources" / "mechanics-formulas.md"
OUT = ROOT / "subjects" / "mechanics" / "formulas"
LECT = {"ch01": "L1", "ch02": "L2"}

TITLE = "公式表（Lecture 1、2）"
RANGE = "Lecture 1、2 全部公式依主題整理：每條附一兩句說明、符號與使用條件，右上角連回講義那一段"


def anchor_index():
    """每個 id → (章, 節 id, 小標編號, 小標文字)，用來產生「L1 §4.1」這種連結標籤。"""
    idx = {}
    for ch in LECT:
        meta = json.loads((ROOT / "subjects" / "mechanics" / ch / "chapter.json").read_text(encoding="utf-8"))
        for s in meta["sections"]:
            t = (ROOT / "subjects" / "mechanics" / ch / "sections" / s["file"]).read_text(encoding="utf-8")
            heads = [(m.start(), m.group(1), re.sub(r"<[^>]+>", "", m.group(2))) for m in re.finditer(r'<h3 id="([^"]+)"[^>]*>(.*?)</h3>', t, re.S)]
            for m in re.finditer(r'id="([^"]+)"', t):
                prev = [h for h in heads if h[0] <= m.start()]
                if prev:
                    _, hid, text = prev[-1]
                    num = re.match(r"\s*(\d+\.\d+)", text)
                    idx[m.group(1)] = (ch, s["id"], num.group(1) if num else "", text.split(" p.")[0].strip())
                else:  # 沒有小標的節（例如只有一題的節）：用節標題，連結標籤要在來源裡自己寫
                    idx[m.group(1)] = (ch, s["id"], "", s["title"])
    return idx


def inline(s):
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)


def card(name, refs, body, idx):
    links = []
    for ref in refs:
        ref = ref.strip()
        ref, _, label = ref.partition("=")
        ch, anc = ref.split("#")
        if anc not in idx or idx[anc][0] != ch:
            raise SystemExit(f"找不到錨點 {ref}（公式卡「{name}」）")
        _, _, num, text = idx[anc]
        tip = text.split("$")[0].rstrip("：")  # 提示文字不放公式（title 不會渲染 LaTeX）
        label = label or f"{LECT[ch]} §{num}"
        links.append(f'<a class="fx-src" data-chapter="mechanics/{ch}" href="#{anc}" title="{html.escape(tip)}">{html.escape(label)}</a>')
    out, para = [], []
    text = "\n".join(body).strip()
    for blk in re.split(r"\n\s*\n", text):
        blk = blk.strip()
        if not blk:
            continue
        if blk.startswith("$$"):
            out.append(f'  <div class="math-block">{blk}</div>')
        elif blk.startswith("符號："):
            out.append(f'  <p class="symnote">{inline(blk)}</p>')
        else:
            out.append(f"  <p>{inline(blk)}</p>")
    head = f'  <div class="fx-head"><span class="fx-name">{inline(name)}</span><span class="fx-links">{"".join(links)}</span></div>'
    return '<div class="fx">\n' + head + "\n" + "\n".join(out) + "\n</div>"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    idx = anchor_index()
    lines = SRC.read_text(encoding="utf-8").split("\n")
    intro, sections, cur, fx = [], [], None, None

    def flush():
        nonlocal fx
        if fx:
            cur["html"].append(card(fx[0], fx[1], fx[2], idx))
            fx = None

    for ln in lines:
        if ln.startswith("# "):
            flush()
            sid, fname, title, pages, desc = [x.strip() for x in ln[2:].split("|")]
            cur = {"id": sid, "file": fname, "title": title, "pages": pages, "desc": desc, "html": []}
            sections.append(cur)
        elif cur is None:
            intro.append(ln)
        elif ln.startswith("## "):
            flush()
            m = re.match(r"## (.+?)\s*\{#([\w-]+)\}\s*$", ln)
            cur["html"].append(f'<h3 id="{m.group(2)}">{inline(m.group(1))}</h3>')
        elif ln.startswith("### "):
            flush()
            name, _, refs = ln[4:].partition("|")
            fx = (name.strip(), [r for r in refs.split(",") if r.strip()], [])
        elif fx is not None:
            fx[2].append(ln)
        elif ln.strip():
            cur["html"].append(inline(ln))
    flush()

    (OUT / "sections").mkdir(parents=True, exist_ok=True)
    for old in (OUT / "sections").glob("*.html"):
        old.unlink()
    intro_html = "\n".join(intro).strip()
    intro_html = re.sub(r"^<!--.*?-->\s*", "", intro_html, flags=re.S)
    (OUT / "sections" / "00-intro.html").write_text(intro_html + "\n", encoding="utf-8")
    meta_secs = [{"id": "s00", "file": "00-intro.html", "title": "總覽與使用方式", "pages": ""}]
    nums = "一二三四五六七八九十"
    for i, s in enumerate(sections):
        h2 = f'<h2>{nums[i]}、{s["title"]} <span class="pg">{s["pages"]}</span></h2>'
        (OUT / "sections" / s["file"]).write_text(h2 + "\n\n" + "\n\n".join(s["html"]) + "\n", encoding="utf-8")
        meta_secs.append({"id": s["id"], "file": s["file"], "title": s["title"], "pages": s["pages"], "pageLabel": "", "desc": s["desc"]})
    meta = {"title": TITLE, "shortTitle": "力學 公式表", "range": RANGE, "pageLabel": "",
            "overview": "s00", "sections": meta_secs}
    (OUT / "chapter.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    n = sum(len([h for h in s["html"] if h.startswith('<div class="fx"')]) for s in sections)
    print(f"公式表：{len(sections)} 節、{n} 張公式卡 → {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
