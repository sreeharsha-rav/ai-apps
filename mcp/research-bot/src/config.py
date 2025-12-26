import os
import logging
from dotenv import load_dotenv

# logging config
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('research_bot_logger')

# storage config
papers_dir = 'data'
papers_path = os.path.join(papers_dir, 'papers_info.json')
os.makedirs(papers_dir, exist_ok=True)

# llm config
load_dotenv(dotenv_path=".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
logger.info(f"===(main)=== Loaded OPENAI_API_KEY: { '*' * 8 if OPENAI_API_KEY else None }")
