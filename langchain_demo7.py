from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain,LLMChain
from qwen_llm import QwenLLM

llm = QwenLLM()
default_chain = ConversationChain(llm=llm, output_key="text")

while True:
    text  = input("请输入内容")
    result = default_chain.run(text)
    print(result)