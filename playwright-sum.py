# playwright-sum.py
import asyncio
from playwright.async_api import async_playwright

URLS = [
    f"https://roe.dev/data-seed-{seed}" for seed in range(76, 86)
]

async def extract_and_sum(page, url):
    await page.goto(url)
    total = 0.0
    tables = await page.query_selector_all("table")
    for table in tables:
        rows = await table.query_selector_all("tr")
        for row in rows:
            cells = await row.query_selector_all("td")
            for cell in cells:
                text = await cell.inner_text()
                try:
                    total += float(text.replace(",", "").strip())
                except ValueError:
                    continue
    return total

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        grand_total = 0.0
        for url in URLS:
            subtotal = await extract_and_sum(page, url)
            print(f"{url} subtotal: {subtotal}")
            grand_total += subtotal
        print("✅ Grand Total:", grand_total)
        await browser.close()

asyncio.run(main())
