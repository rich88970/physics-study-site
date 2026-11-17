"""把 subjects/ 裡網頁要讀的文字檔（JSON、章節 HTML、考試寫法、影片時間軸）打包成 assets/bundle.js。

這樣直接雙擊 index.html（file:// 開啟、沒有伺服器）也能閱讀。
用法：python tools/build_bundle.py      （每次改完內容後執行一次；check_pages.py 會自動先執行）
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def wanted(rel):
    if "/_template/" in rel or "/.local/" in rel:
        return False
    if rel.endswith(".timeline.json") or rel.endswith("registry.json") or rel.endswith("chapter.json") or rel.endswith("step_symbols.json"):
        return True
    return rel.endswith(".html") and ("/sections/" in rel or rel.endswith("/exam.html"))


def build():
    files = {}
    for dirpath, _dirs, names in os.walk(os.path.join(ROOT, "subjects")):
        for n in names:
            rel = os.path.relpath(os.path.join(dirpath, n), ROOT).replace(os.sep, "/")
            if wanted(rel):
                files[rel] = io.open(os.path.join(ROOT, rel), encoding="utf-8").read()
    body = json.dumps(dict(sorted(files.items())), ensure_ascii=False, separators=(",", ":"))
    body = body.replace("</", "<\\/")  # 避免字串裡的 </script> 之類被誤判
    out = os.path.join(ROOT, "assets", "bundle.js")
    io.open(out, "w", encoding="utf-8").write(
        "/* 自動產生，請勿手動修改：python tools/build_bundle.py */\nwindow.STUDY_FILES=" + body + ";\n")
    return len(files), os.path.getsize(out)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    n, size = build()
    print(f"bundle.js：{n} 個檔案，{size / 1024:.0f} KB")
