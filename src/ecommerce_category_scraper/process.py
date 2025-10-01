import asyncio
import json
import logging
import sys

from oxylabs_ai_studio.apps.ai_scraper import AiScraper
from oxylabs_ai_studio.apps.browser_agent import BrowserAgent

from ecommerce_category_scraper.category import (
    get_category_pagination_urls_from_category,
    get_category_pagination_urls_from_domain,
)
from ecommerce_category_scraper.product_urls import extract_product_urls_from_page
from ecommerce_category_scraper.products import scrape_product_details

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logging.getLogger("oxylabs_ai_studio").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class CategoryScrapingError(Exception): ...


async def scrape_category(
    api_key: str,
    ecommerce_domain_url: str | None = None,
    category_url: str | None = None,
    category_description_prompt: str | None = None,
    geo_location: str | None = None,
    render_javascript: bool = False,
    json_schema: dict | None = None,
    parsing_prompt: str | None = None,
    json_filepath: str | None = None,
    max_pages: int | None = None,
    max_products: int | None = None,
) -> list[dict] | None:
    if not ecommerce_domain_url and not category_url:
        raise CategoryScrapingError(
            "Either ecommerce_domain_url or category_url must be provided."
        )

    if ecommerce_domain_url and category_url:
        raise CategoryScrapingError(
            "Either ecommerce_domain_url or category_url must be provided, not both."
        )

    if ecommerce_domain_url and not category_description_prompt:
        raise CategoryScrapingError(
            "category_description_prompt must be provided if ecommerce_domain_url is provided."
        )

    if not json_schema and not parsing_prompt:
        raise CategoryScrapingError(
            "Either json_schema or parsing_prompt must be provided."
        )

    if json_schema and parsing_prompt:
        raise CategoryScrapingError(
            "Either json_schema or parsing_prompt must be provided, not both."
        )

    browser_agent = BrowserAgent(api_key=api_key)
    scraper = AiScraper(api_key=api_key)

    try:
        if ecommerce_domain_url:
            logger.info(
                f"Starting to look for ecommerce category and its pagination URLs from domain: {ecommerce_domain_url}."
            )
            pagination_urls = await get_category_pagination_urls_from_domain(
                browser_agent,
                ecommerce_domain_url,
                category_description_prompt,
                geo_location,
            )
            
        else:
            logger.info(
                f"Starting to look for ecommerce category pagination URLs from category: {category_url}."
            )
            pagination_urls = await get_category_pagination_urls_from_category(
                browser_agent,
                category_url,
                geo_location,
            )
            pagination_urls = list(dict.fromkeys([category_url] + pagination_urls))   
    except Exception as e:
        logger.error(f"Error finding pagination URLs in provided website: {e!r}.")
        raise CategoryScrapingError(e)

    if not pagination_urls:
        logger.info(
            f"No pagination URLs found for {ecommerce_domain_url or category_url}."
        )
        return None
    logger.info(f"Found {len(pagination_urls)} pagination URLs.")

    max_pages = (
        min(max_pages, len(pagination_urls)) if max_pages else len(pagination_urls)
    )
    logger.info(f"Starting to extract product URLs from {max_pages} pagination URLs.")

    product_urls = []
    empty_results_count = 0
    exceptions = []

    for pagination_url in pagination_urls[:max_pages]:
        try:
            page_product_urls = await extract_product_urls_from_page(
                scraper,
                pagination_url,
                geo_location,
                render_javascript,
            )
            if not page_product_urls:
                empty_results_count += 1
                logger.info(
                    f"No product URLs found in pagination URL: {pagination_url}."
                )
            else:
                logger.info(
                    f"Found {len(page_product_urls)} product URLs in pagination URL: {pagination_url}."
                )
                page_product_urls = list(dict.fromkeys(page_product_urls))
                product_urls.extend(
                    [(pagination_url, product_url) for product_url in page_product_urls]
                )
        except Exception as e:
            exceptions.append((pagination_url, e))
            logger.error(
                f"Error extracting product URLs from pagination URL {pagination_url}: {e!r}."
            )

    if len(exceptions) == max_pages:
        logger.error(f"All {max_pages} pagination URLs failed to extract product URLs.")
        raise CategoryScrapingError(
            f"Failed to extract product URLs from all {max_pages} pagination URLs."
        )

    if product_urls:
        product_urls = list(dict.fromkeys(product_urls))
        logger.info(f"Found {len(product_urls)} product URLs in total.")
    else:
        logger.info(f"No product URLs found in any pagination URL.")
        return None

    if not json_schema:
        logger.info(f"Starting to generate JSON schema for product details.")
        try:
            json_schema = await scraper.generate_schema_async(parsing_prompt)
            if not json_schema:
                logger.info(f"JSON schema is not available.")
                return None
        except Exception as e:
            logger.error(f"Error generating JSON schema: {e!r}.")
            raise CategoryScrapingError(e)

    tasks = []
    max_products = (
        min(max_products, len(product_urls)) if max_products else len(product_urls)
    )
    logger.info(f"Starting to scrape product details from {max_products} product URLs.")
    for pagination_url, product_url in product_urls[:max_products]:
        logger.info(f"Starting to scrape product details from {product_url}.")
        tasks.append(
            asyncio.ensure_future(
                scrape_product_details(
                    api_key,
                    product_url,
                    pagination_url,
                    json_schema,
                    geo_location,
                    render_javascript,
                )
            )
        )
        await asyncio.sleep(1)

    # Gather results with return_exceptions=True to handle errors gracefully
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Separate successful results from exceptions
    product_details = []
    exceptions_count = 0
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            exceptions_count += 1
            pagination_url, product_url = product_urls[i]
            logger.error(
                f"Error scraping product details from {product_url}: {result!r}."
            )
        else:
            product_details.append(result)

    # If all scraping attempts failed, raise CategoryScrapingError
    if exceptions_count == max_products:
        logger.error(
            f"All {max_products} product URLs failed to scrape product details."
        )
        raise CategoryScrapingError(
            f"Failed to scrape product details from all {max_products} product URLs."
        )

    if not product_details:
        logger.info(f"No product details found.")
        return None

    logger.info(
        f"Successfully scraped {len(product_details)} out of {max_products} product details."
    )

    if json_filepath:
        logger.info(
            f"Saving {len(product_details)} product details to {json_filepath}."
        )
        with open(json_filepath, "w") as f:
            f.write(json.dumps(product_details, ensure_ascii=False))
        return None

    return product_details
