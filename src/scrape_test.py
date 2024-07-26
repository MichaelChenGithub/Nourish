import os
from dotenv import load_dotenv
from scrapegraphai.graphs import SmartScraperGraph
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

graph_config = {
    "llm": {
        "api_key": OPENAI_API_KEY,
        "model": "gpt-3.5-turbo",
    },
}

smart_scraper_graph = SmartScraperGraph(
    prompt="List me all the foods and nutritions of them. report as a table and contain Brand name",
    # also accepts a string with the already downloaded HTML code
    source="https://www.fatsecret.cn/%E7%83%AD%E9%87%8F%E8%90%A5%E5%85%BB/search?q=%E9%BA%A5%E7%95%B6%E5%8B%9E",
    config=graph_config
)

result = smart_scraper_graph.run()
print(result)