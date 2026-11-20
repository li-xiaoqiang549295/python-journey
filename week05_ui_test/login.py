import re

from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://www.saucedemo.com")

    # 1. 填
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")

    # 2. 点
    page.get_by_role("button", name="Login").click()

    # 3. 断言
    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(page.get_by_text("Products")).to_be_visible()

    page.screenshot(path="login_ok.png")
    print("登录成功，截图已保存")

    browser.close()