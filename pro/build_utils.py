from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from mail_chain import MailChain
from langchain.chains.router.llm_router import RouterOutputParser
from multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.prompts import PromptTemplate
from langchain.chains.router.llm_router import LLMRouterChain
import os
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

def build_agent(llm,serpapi_api_key: str):
    os.environ["SERPAPI_API_KEY"] = serpapi_api_key
    tools = load_tools(["serpapi", "llm-math"], llm=llm)
    agent = initialize_agent(tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
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


