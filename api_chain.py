from langchain.chat_models import ChatOpenAI
from langchain.chains.api.prompt import API_RESPONSE_PROMPT

from langchain.chains import APIChain
from langchain.prompts.prompt import PromptTemplate

import podcast_docs

llm = ChatOpenAI(openai_api_base="http://region-9.seetacloud.com:25540/v1",openai_api_key="none")

from langchain.chains.api import open_meteo_docs
chain_new = APIChain.from_llm_and_api_docs(llm,
                                           podcast_docs.PODCAST_DOCS,
                                           headers={'X-Access-Token':'beee151f-c928-4854-a7a8-f92a1d908f7a'},
                                           limit_to_domains=None,
                                           verbose=True)

chain_new.run("查询周俊辰o")