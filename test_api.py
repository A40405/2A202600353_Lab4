import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
model_name = os.getenv("DEFAULT_MODEL")
llm = ChatOpenAI(base_url="https://models.inference.ai.azure.com/", model= model_name)
print(llm.invoke("xin chào?").content)