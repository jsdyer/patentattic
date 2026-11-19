"""Exercise the shipped application against its built distribution in Chromium."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
with ThreadingHTTPServer(("127.0.0.1",0), partial(SimpleHTTPRequestHandler,directory=root / "dist")) as server:
    Thread(target=server.serve_forever,daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH"))
        page = browser.new_page(viewport={"width":390,"height":844})
        errors = []
        page.on('pageerror',lambda error: errors.append(str(error)))
        page.goto(base + '/')
        page.locator('#filters:not([hidden])').wait_for()
        assert 'pre-grant applications' in page.locator('#coverage').inner_text()
        page.fill('#query','G01S')
        assert 'matches' in page.locator('#status').inner_text()
        page.locator('#records article button').first.click()
        assert 'Final fee received' in page.locator('#detail-fields').inner_text()
        page.get_by_role('button',name='Close details').click()
        page.select_option('#collection','catalog')
        page.get_by_text('22 selected Canadian publications').wait_for()
        page.fill('#query','autofocus')
        assert page.locator('#records article').count() > 0
        assert not errors, errors
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
        browser.close()
    server.shutdown()
