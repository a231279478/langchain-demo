#!/usr/bin/env python
from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatAnthropic, ChatOpenAI
from langserve import add_routes
import os
os.environ['OPENAI_API_KEY'] = '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'
os.environ["OPENAI_API_KEY"] = 'none'
os.environ["OPENAI_API_BASE"] = 'http://region-9.seetacloud.com:25540/v1'

app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple api server using Langchain's Runnable interfaces",
)

add_routes(
    app,
    ChatOpenAI(),
    path="/openai",
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)