import logging
from typing import List

from oxylabs_ai_studio.apps.browser_agent import BrowserAgent
from tenacity import retry, stop_after_attempt

from ecommerce_category_scraper.common import normalize_url

logger = logging.getLogger(__name__)


CATEGORY_NAVIGATION_PROMPT = "Navigate to {category_prompt} and scroll down to see category pagination information."
PAGINATION_NAVIGATION_PROMPT = """
Visit ecommerce category listing page and scroll down to see pagination information. 
Only visit provided website, do not navigate to other pages, don't click on any links. 
If provided website is not a category listing page, don't look for pagination information. 
"""
PAGINATION_FIELD_DESCRIPTION = """
Return pagination ecommerce category listing URLs from one you are currently in to current + 99 pages, but no more than 
100 URLs. It is okey to return less if no more pages are available. If you noticed there are missing URLs because webpage 
does not list them all, create them to match existing ones."""
PAGINATION_SCHEMA = {
    "type": "object",
    "properties": {
        "paginationUrls": {
            "type": "array",
            "maxItems": 100,
            "description": PAGINATION_FIELD_DESCRIPTION,
            "items": {"type": "string"},
        }
    },
    "required": [],
}


@retry(stop=stop_after_attempt(3), reraise=True)
async def _find_pagination_urls(
    browser_agent: BrowserAgent,
    website: str,
    user_prompt: str,
    geo_location: str | None = None,
) -> List[str]:
    try:
        result = await browser_agent.run_async(
            url=website,
            user_prompt=user_prompt,
            output_format="json",
            schema=PAGINATION_SCHEMA,
            geo_location=geo_location,
        )
        return [
            normalize_url(website, url)
            for url in result.data.content.get("paginationUrls", [])
        ]
    except Exception as e:
        raise e


async def get_category_pagination_urls_from_domain(
    browser_agent: BrowserAgent,
    ecommerce_domain_url: str,
    user_prompt: str,
    geo_location: str | None = None,
) -> List[str]:
    """Navigate to a category from the domain URL and get pagination URLs."""
    prompt = CATEGORY_NAVIGATION_PROMPT.format(category_prompt=user_prompt)
    return await _find_pagination_urls(
        browser_agent, ecommerce_domain_url, prompt, geo_location
    )


async def get_category_pagination_urls_from_category(
    browser_agent: BrowserAgent,
    category_url: str,
    geo_location: str | None = None,
) -> List[str]:
    """Get pagination URLs directly from a category URL."""
    prompt = PAGINATION_NAVIGATION_PROMPT
    return await _find_pagination_urls(
        browser_agent, category_url, prompt, geo_location
    )
