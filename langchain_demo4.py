from qwen_llm import QwenLLM
from langchain.schema.messages import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate , PromptTemplate
from langchain.chains import LLMChain

import os
os.environ["SERPAPI_API_KEY"] = '9333902da63642ef782fd41fb732587cbb22abf913554dbc7f4f2273345a50f9'

messages = [
    SystemMessage(content="You're a helpful assistant"),
    HumanMessage(content="What is the purpose of model regularization?"),
]
template = "你现在是一位美食博主，需要根据用户输入的城市：{city}，给出对应的美食推荐"
prompt_template = PromptTemplate(template=template, input_variables=['city'])
llm = QwenLLM()
llmChain = LLMChain(llm=llm,prompt=prompt_template)
llmChain.run("我想要听听深圳的")



