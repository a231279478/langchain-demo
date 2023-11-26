from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from Tool.mail_tool import SendMailTool,EmailAddressTool
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate,SystemMessagePromptTemplate,MessagesPlaceholder,HumanMessagePromptTemplate
from langchain.chains import LLMChain
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import os
os.environ["SERPAPI_API_KEY"] = '9333902da63642ef782fd41fb732587cbb22abf913554dbc7f4f2273345a50f9'


llm = ChatOpenAI(openai_api_base="http://region-9.seetacloud.com:25540/v1",openai_api_key="none")

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("{system}"),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])
#print(prompt_template.format_messages())
messages = [
        HumanMessage(content="我是周俊辰，你呢？"),
        AIMessage(content="我是通义千问"),
    ]
chain = LLMChain(llm=llm ,prompt = prompt,verbose=True)
print(chain.run(input="我是谁？", system="你是邮件助手",history=messages))
