import chainlit as cl
from langchain_community.llms import Ollama

model = Ollama(model="codellama", base_url="http://ollama:11434")


@cl.on_chat_start
async def on_chat_start():
    pass


@cl.on_message
async def on_message(msg: cl.Message):
    if cl.context.session.client_type == "copilot":
        fn = cl.CopilotFunction(name="test", args={"msg": msg.content})
        res = await fn.acall()
        await cl.Message(content=res).send()
