# Load OPENAI_API_KEY from .env file
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

from langchain_core.messages import HumanMessage

msg = llm.invoke([HumanMessage(content="Hi! I'm Bob")])

print(msg)