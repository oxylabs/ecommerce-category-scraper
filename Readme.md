# Ecommerce Category Scraper

[![AI-Studio Python (1)](https://github.com/oxylabs/ecommerce-category-scraper/blob/main/Ai-Studio2.png)](https://aistudio.oxylabs.io/?utm_source=877&utm_medium=affiliate&utm_campaign=ai_studio&groupid=877&utm_content=ai-studio-js-github&transaction_id=102f49063ab94276ae8f116d224b67) 


[![](https://dcbadge.limes.pink/api/server/Pds3gBmKMH?style=for-the-badge&theme=discord)](https://discord.gg/Pds3gBmKMH) [![YouTube](https://img.shields.io/badge/YouTube-Oxylabs-red?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@oxylabs)

## ✅ Prerequisites

Before you begin, make sure you have Oxylabs AI studio API key. Obtain your API key from [Oxylabs AI Studio](https://aistudio.oxylabs.io/settings/api-key). (1000 credits free).

## 📦 Instalation 

- Open your terminal.
- Install the uv package manager:
  ```bash
  # macOS and Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

- Clone the repository:
  ```bash
  git clone https://github.com/oxylabs/ecommerce-category-scraper.git
  ```

- Navigate to the repository:
  ```bash
  cd ecommerce-category-scraper
  ```

- Install the dependencies:
  ```bash
  uv sync
  ```
- Enable the virtual environment:
  ```bash
  source .venv/bin/activate
  ```

## 🧪 Running Tests

Both tests scrape books from `books.toscrape.com` (Sequential art category), extracting book name, price, UPC code, and availability.

**Test 1:** Accepts a category URL directly and scrapes products from that specific category page.

```bash
python -m test.test_1 --oxylabs-ai-studio-api-key <your-api-key>
```

**Test 2:** Accepts an ecommerce domain URL and automatically searches for and identifies category pages before scraping.

```bash
python -m test.test_2 --oxylabs-ai-studio-api-key <your-api-key>
```

**Note:** Modify tests for different domains and settings.

## 🐍 Python Interface

Use `scrape_category` function to integrate the scraper into your code.

```python
from ecommerce_category_scraper.process import scrape_category

result = await scrape_category(
    api_key="your-api-key",
    category_url="https://example.com/category",  # OR use ecommerce_domain_url
    parsing_prompt="Extract product name, price, and rating",
    max_products=50
)
```

### Parameters

**Required:**
- `api_key` - Oxylabs AI Studio API key

**Category selection (choose one):**
- `category_url` - Direct category URL (starts gathering product URLs immediately)
- `ecommerce_domain_url` + `category_description_prompt` - Domain URL and description of category to search for

**Parsing (choose one):**
- `parsing_prompt` - Text description of data to extract
- `json_schema` - JSON schema for structured extraction (more reliable and deterministic)

**Optional:**
- `geo_location` - IP location in ISO2 format (e.g., `"US"`)
- `render_javascript` - Enable JavaScript rendering (default: `False`)
- `jsonl_filepath` - Save results to file (if not provided, returns list)
- `max_pages` - Maximum category pages to scrape (default: all)
- `max_products` - Maximum products to scrape (default: all)
