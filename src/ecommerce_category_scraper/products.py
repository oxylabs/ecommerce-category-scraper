import logging
from typing import Dict

from oxylabs_ai_studio.apps.ai_scraper import AiScraper
from tenacity import retry, stop_after_attempt

logger = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(3),
    reraise=True,
)
async def scrape_product_details(
    api_key: str,
    product_url: str,
    pagination_url: str,
    product_schema: Dict,
    geo_location: str | None = None,
    render_javascript: bool = False,
) -> Dict:
    try:
        scraper = AiScraper(api_key=api_key)
        result = await scraper.scrape_async(
            url=product_url,
            output_format="json",
            schema=product_schema,
            render_javascript=render_javascript,
            geo_location=geo_location,
        )
        additional_data = {
            "pagination_url": pagination_url,
            "product_url": product_url,
        }
        if result.data:
            return {"extracted_data": result.data, "additional_data": additional_data}
        return {"extracted_data": {}, "additional_data": additional_data}

    except Exception as e:
        raise e
