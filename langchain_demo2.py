from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field, validator
from langchain.chains import LLMChain

from qwen_llm import QwenLLM
from langchain.schema.messages import HumanMessage, SystemMessage,AIMessage
from langchain.llms import OpenAI


import os
os.environ["SERPAPI_API_KEY"] = '9333902da63642ef782fd41fb732587cbb22abf913554dbc7f4f2273345a50f9'

# prompt = """
#     能做的事情['发送邮件','查询天气','搜索资料']
#     帮我分析用户的语义具体需要做什么事情，请直接返回对应的内容，如果不在其中，请你自己发挥
#
# """
#
#
#
# messages = [
#     SystemMessage(content=prompt),
#     HumanMessage(content="给张念驰发送一封邮件"),
# ]
#
#
# llm = QwenLLM()
#
# print(llm.invoke(messages))

prompt = """
    发送邮件：
    需要你引导用户填写 收件人、主题、内容。当信息收集完毕时，请输出json格式模板如下:
    ```
    {"recipient":"收件人","subject":"主题","content":"内容"}
    ```
"""
messages = [
    SystemMessage(content=prompt),
    HumanMessage(content="给张念驰发送一封邮件"),
    # AIMessage(content="好的，请问您需要在邮件中添加什么内容吗？"),
    # HumanMessage(content="明天早上10点来办公室开会"),
]

llm = QwenLLM()
LLMChain(llm=llm)


print(llm.invoke(messages))


