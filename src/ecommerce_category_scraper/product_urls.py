import logging
from typing import List

from oxylabs_ai_studio.apps.ai_scraper import AiScraper
from tenacity import retry, stop_after_attempt

from ecommerce_category_scraper.common import normalize_url

logger = logging.getLogger(__name__)


PRODUCT_URLS_DESCRIPTION = """
A list of product URL links in category pagination page:
- Only include URL links that are in this category listing;
- Usually there are from 20 to 30. Could be more or less. Last pagination page sometimes have less;
- Do not include other product URLs, or category URLs, or related product URLs, which are not part of category pagination page listing;
- Don't invent any product URLs or modify existing ones;
- Return only URL links that you find in category pagination page.
"""


@retry(
    stop=stop_after_attempt(3),
    reraise=True,
)
async def extract_product_urls_from_page(
    scraper: AiScraper,
    page_url: str,
    geo_location: str | None = None,
    render_javascript: bool = False,
) -> List[str]:
    try:
        result = await scraper.scrape_async(
            url=page_url,
            output_format="json",
            schema={
                "type": "object",
                "properties": {
                    "product_url_links": {
                        "type": "array",
                        "description": PRODUCT_URLS_DESCRIPTION,
                        "items": {"type": "string"},
                    }
                },
                "required": ["product_url_links"],
            },
            render_javascript=render_javascript,
            geo_location=geo_location,
        )

        if result.data and isinstance(result.data, dict):
            urls = result.data.get("product_url_links", [])
            return [normalize_url(page_url, url) for url in urls]
        return []
    except Exception as e:
        raise e
