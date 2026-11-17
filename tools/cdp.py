"""極簡的 Chrome DevTools Protocol 控制器：開無頭 Chrome、載入頁面、執行 JS、截圖。

只依賴 aiohttp（若系統沒有，會嘗試使用 Website 2 的 .local/video-tools 中的 aiohttp）。
"""
from __future__ import annotations

import asyncio
import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

try:
    import aiohttp  # noqa: F401
except ImportError:  # 使用之前做影片時已安裝的套件
    sys.path.insert(0, str(Path.home() / "Documents/Codex/2026-09-05/https-drive-google-com-drive-u/work/physics-site2/.local/video-tools"))
    import aiohttp  # noqa: E402,F401

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def find_chrome() -> str:
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    found = shutil.which("chrome") or shutil.which("msedge")
    if not found:
        raise RuntimeError("找不到 Chrome 或 Edge")
    return found


class Browser:
    def __init__(self, width=1280, height=720, port=9333):
        # CDP_PORT_OFFSET：同時跑多個檢查時錯開連接埠（例如 100、200）
        self.width, self.height, self.port = width, height, port + int(os.environ.get("CDP_PORT_OFFSET", "0"))
        self.proc = None
        self.ws = None
        self.session = None
        self._id = 0
        self.profile = tempfile.mkdtemp(prefix="cdp-profile-")

    async def __aenter__(self):
        self.proc = subprocess.Popen([
            find_chrome(), "--headless=new", f"--remote-debugging-port={self.port}",
            f"--user-data-dir={self.profile}", "--no-first-run", "--no-default-browser-check",
            "--hide-scrollbars", "--force-device-scale-factor=1", "--disable-gpu",
            f"--window-size={self.width},{self.height}", "about:blank",
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.session = aiohttp.ClientSession()
        url = None
        for _ in range(100):
            try:
                async with self.session.get(f"http://127.0.0.1:{self.port}/json") as r:
                    pages = [p for p in await r.json() if p.get("type") == "page"]
                    if pages:
                        url = pages[0]["webSocketDebuggerUrl"]
                        break
            except Exception:
                pass
            await asyncio.sleep(0.1)
        if not url:
            raise RuntimeError("無法連上無頭 Chrome")
        self.ws = await self.session.ws_connect(url, max_msg_size=0)
        await self.send("Page.enable")
        await self.send("Runtime.enable")
        await self.send("Emulation.setDeviceMetricsOverride", width=self.width, height=self.height, deviceScaleFactor=1, mobile=False)
        return self

    async def __aexit__(self, *exc):
        try:
            if self.ws is not None:
                await self.ws.close()
            if self.session is not None:
                await self.session.close()
        finally:
            if self.proc:
                self.proc.terminate()
                try:
                    self.proc.wait(5)
                except Exception:
                    self.proc.kill()
            shutil.rmtree(self.profile, ignore_errors=True)

    async def send(self, method, **params):
        self._id += 1
        mid = self._id
        await self.ws.send_str(json.dumps({"id": mid, "method": method, "params": params}))
        while True:
            msg = await self.ws.receive()
            if msg.type != aiohttp.WSMsgType.TEXT:
                raise RuntimeError(f"CDP 連線中斷：{msg.type}")
            data = json.loads(msg.data)
            if data.get("id") == mid:
                if "error" in data:
                    raise RuntimeError(f"{method}: {data['error']}")
                return data.get("result", {})

    async def goto(self, url, ready_js="document.body && document.body.getAttribute('data-ready')==='1'", timeout=30):
        await self.send("Page.navigate", url=url)
        t0 = time.time()
        while time.time() - t0 < timeout:
            if await self.eval(ready_js):
                return
            await asyncio.sleep(0.1)
        raise TimeoutError(f"頁面沒有在 {timeout}s 內就緒：{url}")

    async def eval(self, expr, await_promise=True):
        r = await self.send("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=await_promise)
        if "exceptionDetails" in r:
            raise RuntimeError(json.dumps(r["exceptionDetails"], ensure_ascii=False)[:2000])
        return r.get("result", {}).get("value")

    async def screenshot(self, fmt="jpeg", quality=92, clip=None, full=False) -> bytes:
        params = {"format": fmt}
        if fmt == "jpeg":
            params["quality"] = quality
        if full:
            size = await self.eval("[document.documentElement.scrollWidth, document.documentElement.scrollHeight]")
            params["clip"] = {"x": 0, "y": 0, "width": size[0], "height": size[1], "scale": 1}
            params["captureBeyondViewport"] = True
        elif clip:
            params["clip"] = dict(clip, scale=1)
        r = await self.send("Page.captureScreenshot", **params)
        return base64.b64decode(r["data"])


async def _shot(url, out, width, height, full):
    async with Browser(width, height) as b:
        await b.goto(url)
        await asyncio.sleep(0.5)
        Path(out).write_bytes(await b.screenshot(fmt="png", full=full))


if __name__ == "__main__":
    # 用法：python cdp.py URL 輸出.png [寬] [高] [full]
    u, o = sys.argv[1], sys.argv[2]
    w = int(sys.argv[3]) if len(sys.argv) > 3 else 1280
    h = int(sys.argv[4]) if len(sys.argv) > 4 else 720
    asyncio.run(_shot(u, o, w, h, len(sys.argv) > 5))
    print("saved", o)
