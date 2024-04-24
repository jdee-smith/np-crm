import chainlit as cl
from langchain.schema import StrOutputParser
from langchain_community.llms import Ollama
from prompts import text_to_sql

model = Ollama(model="codellama", base_url="http://ollama:11434")
chain = text_to_sql.prompt | model | StrOutputParser()


@cl.on_chat_start
async def on_chat_start():
    pass


@cl.on_message
async def on_message(msg: cl.Message):
    if cl.context.session.client_type == "copilot":
        fn = cl.CopilotFunction(name="test", args={"msg": msg.content})
        res = await fn.acall()
        await cl.Message(content=res).send()
