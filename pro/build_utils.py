from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from mail_chain import MailChain
from langchain.chains.router.llm_router import RouterOutputParser
from multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.prompts import PromptTemplate
from langchain.chains.router.llm_router import LLMRouterChain
from langchain.agents.structured_chat.base import StructuredChatAgent
from langchain.agents.structured_chat.output_parser import StructuredChatOutputParser
from langchain.agents import AgentExecutor

import tools
import os
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

def build_agent(llm):
    os.environ["SERPAPI_API_KEY"] = '9333902da63642ef782fd41fb732587cbb22abf913554dbc7f4f2273345a50f9'
    t = load_tools(["serpapi"],llm=llm)
    # 初始化工具
    t.extend([tools.SaveAddressBookTool(), tools.QueryAddressBookTool()])
    chat_agent = StructuredChatAgent.from_llm_and_tools(
        # prefix=SYSTEM_MESSAGE_PREFIX, # 指定提示词前缀
        llm=llm, tools=t,
        verbose=True,  # 是否打印调试日志，方便查看每个环节执行情况
        output_parser=StructuredChatOutputParser()  #
    )
    agent = AgentExecutor.from_agent_and_tools(
        agent=chat_agent, tools=t, verbose=True,
        max_iterations=3  # 设置大模型循环最大次数，防止无限循环
    )
    return agent

def build_mail_chain(base_url):
    return MailChain(base_url=base_url)


def build_router_chain(llm,infos):
    destinations = [f"{p['name']}: {p['description']}" for p in infos]

    destinations_str = "\n".join(destinations)
    router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations_str)


    router_prompt = PromptTemplate(
        template=router_template,
        input_variables=["input"],
        output_parser=RouterOutputParser(),
    )
    router_chain = LLMRouterChain.from_llm(llm, router_prompt, verbose=True)
    condition_chains = {p['name']:p['chain'] for p in infos}
    return condition_chains ,router_chain


def build_chain_messages(messages):
    chain_messages = []
    for item in messages:
        role = item['role']
        content = item['content']
        if 'system' == role:
            chain_messages.append(SystemMessage(content=content))
        elif 'assistant' == role:
            chain_messages.append(AIMessage(content=content))
        else:
            chain_messages.append(HumanMessage(content=content))
    return chain_messages


