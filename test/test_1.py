import argparse
import asyncio
from ecommerce_category_scraper.process import scrape_category

async def test_1(oxylabs_ai_studio_api_key: str):
    result = await scrape_category(
        api_key=oxylabs_ai_studio_api_key,
        category_url="https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html",
        parsing_prompt="Extract book name, price, UPC code, and availability",
        geo_location="US",
        render_javascript=False,
        max_pages=2,
        max_products=40,
        jsonl_filepath="test_1_results.jsonl",
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test ecommerce category scraper")
    parser.add_argument(
        "--oxylabs-ai-studio-api-key",
        required=True,
        help="Oxylabs AI Studio API key"
    )
    args = parser.parse_args()
    asyncio.run(test_1(args.oxylabs_ai_studio_api_key))
