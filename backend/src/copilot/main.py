import os

import chainlit as cl
from langchain_community.llms import Ollama

OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL")

model = Ollama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)


@cl.on_chat_start
async def on_chat_start():
    pass


@cl.on_message
async def on_message(msg: cl.Message):
    if cl.context.session.client_type == "copilot":
        fn = cl.CopilotFunction(name="test", args={"msg": msg.content})
        res = await fn.acall()
        await cl.Message(content=res).send()
