from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()


api_key = os.getenv('API_KEY')
base_url = "https://apim-pllum-tst-pcn.azure-api.net/vllm/v1"
model_name = "CYFRAGOVPL/pllum-12b-nc-chat-250715"


llm = ChatOpenAI(
    model=model_name,
    openai_api_key="EMPTY",
    openai_api_base=base_url,
    temperature=0.7,
    max_tokens=300,
    default_headers={
    'Ocp-Apim-Subscription-Key': api_key
     }
)

response = llm.invoke("Witaj!")
print(response.model_dump()['content'])