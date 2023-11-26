from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field, validator

from qwen_llm import QwenLLM
from langchain.schema.messages import HumanMessage, SystemMessage
from langchain.llms import OpenAI


import os
os.environ["SERPAPI_API_KEY"] = '9333902da63642ef782fd41fb732587cbb22abf913554dbc7f4f2273345a50f9'

messages = [
    SystemMessage(content="You're a helpful assistant"),
    HumanMessage(content="What is the purpose of model regularization?"),
]


llm = QwenLLM()





# Define your desired data structure.
class Email(BaseModel):
    recipient: str = Field(description="收件人")
    subject: str = Field(description="主题")
    content: str = Field(description="内容")


parser = PydanticOutputParser(pydantic_object=Email)

prompt = PromptTemplate(
    template="回答用户的询问。\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

_input =prompt.format_prompt(query="给张念驰发送一封邮件，明天10点过来开会")

output = llm.predict(_input.to_string())
email = parser.parse(output)
print(email)

