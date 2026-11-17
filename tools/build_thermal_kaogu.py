"""熱學「考古題（第 1、2 章範圍）」章：把第 1、2 章裡考過的題目卡，依考卷與題號重新排成一章。
題目（英文原卷＋翻譯）、考試書寫版、符號表從 ch01／ch02 原樣複製；解題部分改用
tools/sources/thermal-kaogu.md 的精簡步驟版（「① 步驟名：」＋公式框＋計算，同應數考古章），
每張卡一段，以「## 卡片 id」開頭。改題目請改原章節，改解題請改 md，再重跑本腳本：
    python tools/build_thermal_kaogu.py
"""
import json
import re
from pathlib import Path

from build_extra_md import to_html

ROOT = Path(__file__).resolve().parents[1]
TH = ROOT / "subjects" / "thermal"
OUT = TH / "kaogu"
SOLUTIONS = ROOT / "tools" / "sources" / "thermal-kaogu.md"

# 考卷 → [(題號, 卡片 id, 附註)]；附註是放在卡片前的一句說明（沒有就留空）
PAPERS = [
    ("s01", "01-115-mid.html", "115 級上學期期中", "範圍第 1–2 章，7 題 100 分", [
        ("第 1 題", "tk1-115-1", ""),
        ("第 2 題", "sc-1-8", "考卷第 2 題就是課本 Problem 1.8，只考 (a)(c)；下面題目是課本原題，解題只寫考過的 (a)(c)。"),
        ("第 3 題", "tk-115-3", ""),
        ("第 4 題", "tk-115-4", ""),
        ("第 5 題", "tk-115-5", ""),
        ("第 6 題", "tk-115-6", ""),
        ("第 7 題", "tk-115-7", ""),
    ]),
    ("s02", "02-114-mid.html", "114 級上學期期中", "7 題（只有手機照片，封面沒拍到）", [
        ("第 1 題", None, "第 1 題（熱膨脹）與 115 級期中第 2 題相同，見 <a href=\"#sc-1-8\">115 級第 2 題</a>。"),
        ("第 2 題", "tk1-114-2", ""),
        ("第 3 題", "tk-114-3", ""),
        ("第 4 題", "tk-114-4", ""),
        ("第 5 題", "tk-114-5", ""),
        ("第 6 題", "tk-114-6", ""),
        ("第 7 題", "tk1-114-7", ""),
    ]),
    ("s03", "03-x-mid.html", "某級上學期期中", "範圍第 1–4.1 章，4 大題 110 分；第 1 題 (f)–(h) 是第 4 章熱機，不在本章範圍", [
        ("第 1 題 (a)", "tk1x-1a", ""),
        ("第 1 題 (b)", "tk1x-1b", ""),
        ("第 1 題 (c)(d)", "tk1x-1cd", ""),
        ("第 1 題 (e)", "tk1x-1e", ""),
        ("第 1 題 (f)–(h)", None, "第 1 題 (f)–(h)（雙原子氣體熱機循環、效率、Carnot 效率）屬第 4 章，不在第 1、2 章範圍，未收。"),
        ("第 1 題 (i)", "sc-1-17", "考卷第 1 題 (i) 就是課本 Problem 1.17 (c)（凡得瓦方程式的維里係數）；下面題目是課本原題，解題只寫考過的 (c)。"),
        ("第 1 題 (j)", "tkx-1j", ""),
        ("第 2 題", "tkx-2", ""),
        ("第 3 題", "tkx-3", ""),
        ("第 4 題", "tk1x-4", ""),
    ]),
]


def grab_div(text, start):
    """從 start（'<div' 開頭）抓出完整、成對的 div。"""
    depth, i = 0, start
    for m in re.compile(r"<(/?)div\b[^>]*>").finditer(text, start):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return text[start:m.end()]
    raise ValueError("div 不成對")


def find_card(cid):
    for ch in ("ch01", "ch02"):
        for f in sorted((TH / ch / "sections").glob("*.html")):
            t = f.read_text(encoding="utf-8")
            m = re.search(r'<div class="problem"[^>]*\sid="%s"' % re.escape(cid), t)
            if m:
                sec = json.loads((TH / ch / "chapter.json").read_text(encoding="utf-8"))
                title = next((s["title"] for s in sec["sections"] if s["file"] == f.name), f.name)
                return grab_div(t, m.start()), ch, title
    raise KeyError(cid)


def load_solutions():
    """thermal-kaogu.md → {卡片 id: 解題 Markdown}。"""
    sols, cur = {}, None
    for ln in SOLUTIONS.read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^## (\S+)\s*$", ln)
        if m:
            cur = m.group(1)
            sols[cur] = []
        elif cur:
            sols[cur].append(ln)
    return {k: "\n".join(v).strip() for k, v in sols.items()}


def concise_card(card, md):
    """保留卡片標頭與題目（英文原卷＋翻譯），其餘（條件表、為什麼、詳解、答案、檢查、詳細說明）換成精簡解題。"""
    head = card[:card.index('<div class="pbody">') + len('<div class="pbody">')]
    statement = grab_div(card, card.index('<div class="part statement"'))
    sol = to_html(md, "x", False)
    return (f'{head}\n    {statement}\n    <div class="part solution concise"><span class="part-label">解題</span>\n'
            f'{sol}\n    </div>\n  </div>\n</div>')


def find_exam(cid):
    for ch in ("ch01", "ch02"):
        t = (TH / ch / "exam.html").read_text(encoding="utf-8")
        m = re.search(r'<article class="exam-item"[^>]*data-exam-id="%s"' % re.escape(cid), t)
        if m:
            return t[m.start():t.index("</article>", m.start()) + len("</article>")]
    return None


def main():
    (OUT / "sections").mkdir(parents=True, exist_ok=True)
    for old in (OUT / "sections").iterdir():
        if old.is_file():
            old.unlink()
    sections = [{"id": "s00", "file": "00-intro.html", "title": "本章總覽：考卷與題目一覽", "pages": ""}]
    exams, rows, n_cards, pages = [], [], 0, {}
    sols = load_solutions()
    for sid, fname, paper, note, items in PAPERS:
        body = [f'<h2>{paper} <span class="pg">{note.split("，")[0]}</span></h2>',
                f'<p class="lead">{paper}：{note}。題目依考卷題號排列；英文原卷、翻譯與考試書寫版和第 1、2 章裡的同一題相同，解題改成精簡步驟版。</p>']
        for qno, cid, remark in items:
            hid = f"{sid}-q{len([b for b in body if b.startswith('<h3')]) + 1}"
            if cid is None:
                body.append(f'<h3 id="{hid}">{qno}</h3>\n<div class="box pitfall"><p>{remark}</p></div>')
                rows.append((paper, qno, "—", remark.split("，")[0] if "未收" in remark else "同 115 級第 2 題"))
                continue
            card, ch, sec_title = find_card(cid)
            h4 = re.search(r"<h4>(.*?)</h4>", card, re.S).group(1)
            card = concise_card(card, sols[cid])
            body.append(f'<h3 id="{hid}">{qno}｜{h4}</h3>')
            link = f'<p class="note-src">原本收在 <a data-chapter="thermal/{ch}" href="#{cid}">第 {ch[-1]} 章 · {sec_title}</a>。</p>'
            if remark:
                body.append(f'<div class="box idea"><p>{remark}</p></div>')
            body.append(link)
            body.append(card)
            n_cards += 1
            ex = find_exam(cid)
            if ex:
                ex = re.sub(r'data-group="[^"]*"', f'data-group="{paper}"', ex, count=1)
                exams.append(ex)
            rows.append((paper, qno, h4, f"第 {ch[-1]} 章 · {sec_title}"))
        pages[fname] = "\n\n".join(body) + "\n"
        sections.append({"id": sid, "file": fname, "title": paper, "pages": "",
                         "desc": f"{note}。"})

    # 卡片裡原本連到同章錨點的 <a href="#x">：本章沒有 x 時，補上 x 所在的原章節
    here = set(re.findall(r'\sid="([^"]+)"', "".join(pages.values())))
    src_ids = {ch: set(re.findall(r'\sid="([^"]+)"', "".join(f.read_text(encoding="utf-8") for f in (TH / ch / "sections").glob("*.html"))))
               for ch in ("ch01", "ch02")}

    def relink(html):
        def fix(m):
            x = m.group(1)
            if x in here:
                return m.group(0)
            ch = next((c for c in ("ch01", "ch02") if x in src_ids[c]), None)
            return f'<a data-chapter="thermal/{ch}" href="#{x}"' if ch else m.group(0)
        return re.sub(r'<a href="#([^"]+)"', fix, html)

    for fname, html in pages.items():
        (OUT / "sections" / fname).write_text(relink(html), encoding="utf-8")
    exams = [relink(e) for e in exams]

    table = "\n".join(f"<tr><td>{p}</td><td>{q}</td><td>{t}</td><td>{w}</td></tr>" for p, q, t, w in rows)
    intro = f"""<h2>本章總覽：考卷與題目一覽</h2>
<p class="lead">這一章只收考卷上考過、且在第 1、2 章範圍內的題目，依考卷與題號排列，共 {n_cards} 張題目卡。每張卡附英文原卷與翻譯，解題用精簡步驟（每步先說在做什麼、再列用到的公式與計算），也可以直接用考試模式練習。</p>
<div class="box idea"><p><b>收錄範圍：</b>趙松柏老師熱物理學（上學期）的 115 級期中、114 級期中、某級期中。期末考（第 3–5 章）與下學期統計熱力學（第 6–7 章）不在網站目前的第 1、2 章範圍，沒有收。</p></div>
<div class="symbol-table-wrap"><table><thead><tr><th>考卷</th><th>題號</th><th>題目</th><th>原本所在</th></tr></thead><tbody>
{table}
</tbody></table></div>
<div data-section-list></div>
"""
    (OUT / "sections" / "00-intro.html").write_text(intro, encoding="utf-8")
    (OUT / "exam.html").write_text("<!-- 由 tools/build_thermal_kaogu.py 從 ch01／ch02 的 exam.html 複製 -->\n\n" + "\n\n".join(exams) + "\n", encoding="utf-8")

    syms = {"symbols": {}, "groups": [], "steps": {}}
    for ch in ("ch02", "ch01"):
        s = json.loads((TH / ch / "step_symbols.json").read_text(encoding="utf-8"))
        for k in ("symbols", "groups", "steps"):
            v = s.get(k)
            if isinstance(v, list):
                syms[k] = syms[k] + [x for x in v if x not in syms[k]]
            else:
                for kk, vv in (v or {}).items():
                    syms[k].setdefault(kk, vv)
    (OUT / "step_symbols.json").write_text(json.dumps(syms, ensure_ascii=False, indent=1), encoding="utf-8")

    c2 = json.loads((TH / "ch02" / "chapter.json").read_text(encoding="utf-8"))
    chapter = {
        "title": "考古題（第 1、2 章範圍）",
        "shortTitle": "熱學 考古題",
        "range": "115 級、114 級、某級上學期期中考裡屬於第 1、2 章的題目，依考卷與題號排列",
        "pageLabel": "考古",
        "tutorIntro": "你是「讀懂物理」讀書網站裡的 AI 助教。對象是台灣的大學物理系學生，正在準備熱物理學（趙松柏老師）考試，課本 Schroeder《An Introduction to Thermal Physics》。這一章只收上學期期中考考過、屬於第 1 章（理想氣體、均分定理、熱與功、壓縮功、熱容量與潛熱、熱膨脹）與第 2 章（兩態系統、愛因斯坦固體、交互作用的系統、Stirling 近似、多重度的峰、理想氣體多重度、熵）的題目，依考卷排列；考試要求寫出完整推導。",
        "overview": "s00",
        "sections": sections,
        "sources": c2.get("sources", []),
        "stepSymbols": "step_symbols.json",
        "exam": "exam.html",
        "scripts": [],
    }
    (OUT / "chapter.json").write_text(json.dumps(chapter, ensure_ascii=False, indent=2), encoding="utf-8")

    reg_p = ROOT / "subjects" / "registry.json"
    reg = json.loads(reg_p.read_text(encoding="utf-8"))
    subj = next(s for s in reg["subjects"] if s["id"] == "thermal")
    ent = next((c for c in subj["chapters"] if c["id"] == "kaogu"), None)
    if ent is None:
        ent = {"id": "kaogu"}
        subj["chapters"].append(ent)
    ent.update({"title": chapter["title"], "range": chapter["range"], "status": "ready"})
    reg_p.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")
    print("卡片", n_cards, "張；考試書寫版", len(exams), "份；節", len(sections))


if __name__ == "__main__":
    main()
