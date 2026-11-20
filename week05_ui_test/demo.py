from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.saucedemo.com")
    print("标题：", page.title())

    page.wait_for_timeout(5000)   # 停 5 秒

    browser.close()



