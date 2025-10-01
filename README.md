# Ecommerce Category Scraper

[![AI-Studio Python (1)](https://github.com/oxylabs/ecommerce-category-scraper/blob/main/Ai-Studio2.png)](https://aistudio.oxylabs.io/?utm_source=877&utm_medium=affiliate&utm_campaign=ai_studio&groupid=877&utm_content=ai-studio-js-github&transaction_id=102f49063ab94276ae8f116d224b67) 


[![](https://dcbadge.limes.pink/api/server/Pds3gBmKMH?style=for-the-badge&theme=discord)](https://discord.gg/Pds3gBmKMH) [![YouTube](https://img.shields.io/badge/YouTube-Oxylabs-red?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@oxylabs)

## 🛒 E-commerce Category Scraper

AI-Powered E-commerce Category Scraper with AI Studio

The E-commerce Category Scraper is an AI-powered, open-source tool built using Oxylabs AI Studio. It automates and streamlines data extraction from e-commerce websites, making it accessible to developers of all skill levels. This solution can also be adapted as a scalable price comparison tool, perfect for analyzing competitor pricing and market trends.

What problems does this tool solve?
- Scraping all products from ecommerce categories without writing custom code;
- Automatically locating ecommerce categories and scraping their products;

## 🚀 Key features

- **Cost optimization**: AI Studio ensures task-based scalability.
- **Pre-built solution**: A ready-to-use open-source tool for faster adoption and seamless integration.
- **Low-code automation**: Create automated workflows for web scraping and parsing without needing advanced coding skills.
- **AI-powered capabilities**: Extract structured web data with minimal effort using Oxylabs’ AI Studio apps.
- **Enterprise-ready infrastructure**: Handle CAPTCHAs, bypass IP blocks, and navigate dynamic content effortlessly.
- **Flexible scalability**: Perfect for small tasks using free AI Studio credits or scaling to enterprise-level projects.

## 🤖 How it works

- **Browser Agent**: Collects all product URLs, handling pagination and location-specific categories.
- **AI-Scraper**: Extracts all product URLs from category listing pages.
- **AI-Scraper**: Extracts structured product data like pricing, titles, and stock availability. Based on user prompt or JSON schema.
- **Final Output**: Clean, structured datasets ready for use in analytics, reporting, or pricing workflows. Which can be saved to JSONL file or returned to the user programatically.


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

## 📈 Practical use cases
- **Price comparison tool**: Automate workflows to compare competitor prices by category or region.
- **Price monitoring**: Regularly track competitor pricing trends and fluctuations.
- **Market intelligence**: Collect data for competitive and industry analysis.
- **E-commerce scraping**: Extract essential product details for AI applications or business intelligence.
- **Product detail extraction**: Automate the retrieval of pricing, inventory, and product descriptions.

## 📝 FAQ

- **Can I scrape any website using this tool?**

  This tool can scrape most websites, but scraping capabilities depend on adhering to the website's legal and technical restrictions.
- **Is this tool free?**
  Yes, the E-commerce Category Scraper is open-source and free to use. Smaller tasks are powered by AI Studio’s free credits, while flexible plans allow scaling for larger workflows.
- **Do I need advanced coding skills to use this tool?**
  Advanced coding skills are not required. AI-powered code editor simplifies integration, making it accessible for engineers with basic coding experience.
- **Can I customize this scraper for my needs?**
  Yes, the open-source solution can be fully customized to meet specific workflow or business requirements.
- **What are AI Studio free credits?**
  AI Studio offers free credits for smaller tasks. For scaling beyond free credits, users can subscribe to flexible plans.


## 🎥 Showcased at Oxycon 2025
This E-commerce Category Scraper was featured live at Oxycon 2025. The presentation demonstrated how AI Studio can be used to easily build real-time price comparison tool while showcasing how developers can create scalable scraping workflows for various e-commerce tasks.

## 📚 Learn more
For a deeper dive into features, integrations, and examples, and documentation, visit the [AI Studio](https://aistudio.oxylabs.io/) website.

## 💬 Contact us
If you have questions or need support, reach out to us at hello@oxylabs.io, through [live chat](https://oxylabs.drift.click/oxybot), or join our [Discord community](https://discord.com/invite/Pds3gBmKMH).
