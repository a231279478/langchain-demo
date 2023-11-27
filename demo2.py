from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from Tool.mail_tool import SendMailTool,EmailAddressTool
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate,SystemMessagePromptTemplate,MessagesPlaceholder,HumanMessagePromptTemplate,PromptTemplate
from langchain.chains import LLMChain,MultiPromptChain
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from MyCustomChain import MyCustomChain


import os
os.environ["SERPAPI_API_KEY"] = '9333902da63642ef782fd41fb732587cbb22abf913554dbc7f4f2273345a50f9'




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

llm = ChatOpenAI(openai_api_base="http://region-9.seetacloud.com:25540/v1",openai_api_key="none")
tools = load_tools(["serpapi", "llm-math"], llm=llm)
# 工具加载后都需要初始化，verbose 参数为 True，会打印全部的执行详情
agent = initialize_agent(tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)


prompt_infos = [
    {
        "name": "mail",
        "description": "擅长处理邮件问题",
    },
]

destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]

destinations_str = "\n".join(destinations)
print('============================================================')
from multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE


router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations_str)

print(router_template)

print('============================================================')
from langchain.chains.router.llm_router import RouterOutputParser

router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    output_parser=RouterOutputParser(),
)

candadite_chains = {}

candadite_chains['mail'] = MyCustomChain()

from langchain.chains.router.llm_router import LLMRouterChain
router_chain = LLMRouterChain.from_llm(llm, router_prompt,verbose=True)

# chain = MultiPromptChain(
#     router_chain=router_chain,
#     destination_chains=candadite_chains,
#     default_chain=agent,
#     verbose=True,
#     silent_errors=True
# )

params = {"model":"chatglm3-6b","messages":[{"role":"user","content":"明天是周几？"}],"stream":True}

messages = params['messages']

chain_messages = build_chain_messages(messages)
chain_messages.pop()

current_message = messages[-1]
# prompt = ChatPromptTemplate.from_messages([
#     MessagesPlaceholder(variable_name="history")
# ])
#print(prompt_template.format_messages())


# print(chain.run(input="你是谁",history=prompt.format(history=messages)))

router_result = router_chain.invoke({"input":current_message['content'],"history":ChatPromptTemplate.from_messages(chain_messages).format()},return_only_outputs=True)

print(router_result)


router = router_result['destination']


if router:
    chain = candadite_chains.get(router)
    if chain is not None:
        print(chain.invoke(params,return_only_outputs=True))
else:
    print(agent.run(router_result['next_inputs']))






