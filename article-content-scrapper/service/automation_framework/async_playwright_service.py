import asyncio
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

# Define a semaphore to limit the number of concurrent tasks
semaphore = asyncio.Semaphore(5)  # Limit to 5 concurrent tabs


async def extract_info_from_webpage(page, url):
    await page.goto(url)

    elements = await page.query_selector_all('//h1[@data-cy="article-title"]')
    texts = []
    if elements:
        for ele in elements:
            text = await ele.inner_text()
            texts.append(text)
    return {
        "header": ' '.join(texts)
    }


def crawl_from_article(selectors, page):
    texts = []
    for s in selectors:
        selector_query = s.get('name', '')
        elements = await page.query_selector_all(selector_query)
        if elements:
            for ele in elements:
                text = await ele.inner_text()
                texts.append(text)
            return ' '.join(texts)
        else:
            continue
    return ' '


def extract_articles_batch():
    print('')


def fetch_articles_from_urls(article_metadata_list: list):
    articles = []
    print()


async def start_async():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Launch a single browser instance
        async with semaphore:
            page = await browser.new_page()  # open a new tab
            try:
                value = await extract_info_from_webpage(page,
                                                        'https://fortune.com/2025/02/27/openai-gpt-4-5-orion-launch-sam-altman-benchmarks/')
                print(value)
            except Exception as e:
                print(e)


# asyncio.run(start_async())
def start_sync():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Launch a single browser instance
        page = browser.new_page()  # open a new tab
        try:
            value = await extract_info_from_webpage(page,
                                                    'https://fortune.com/2025/02/27/openai-gpt-4-5-orion-launch-sam-altman-benchmarks/')
            print(value)
        except Exception as e:
            print(e)
            