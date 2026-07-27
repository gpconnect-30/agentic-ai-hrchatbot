from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
import config
from chatbot import HRChatbot
from prompts import hr_prompt_builder
from query_enhancer import QueryEnhancer
from conversation_memory import ConversationMemory

llm = OllamaLLM(model=config.OLLAMA_MODEL, temperature=0.4, num_ctx=2048)

embed = OllamaEmbeddings(model=config.EMBEDDING_MODEL)
vector_store = Chroma(
        embedding_function=embed,
        persist_directory=config.VECTORSTORE_PATH
    )
retriever = vector_store.as_retriever()

query_enhancer = QueryEnhancer(llm)

prompt_builder = hr_prompt_builder.HRPromptTemplate()

memory = ConversationMemory()

bot = HRChatbot(llm, query_enhancer, retriever, prompt_builder, memory)
while True:
    query = input("You: ")
    if query.lower() in ["exit", "quit"]:
        break
    bot.ask(query)
    print()
