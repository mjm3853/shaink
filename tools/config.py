import os
from dotenv import load_dotenv
load_dotenv()

youtube_api_key = os.getenv("YOUTUBE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")