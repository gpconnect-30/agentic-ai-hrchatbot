from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
import config
from chatbot import HRChatbot
from prompts import hr_prompt_builder
from query_enhancer import QueryEnhancer
from conversation_memory import ConversationMemory

llm = OllamaLLM(model=config.OLLAMA_MODEL)

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
answer = bot.ask("my leave balance?")
print(answer)
#print("----------------------------------------------------")
# print("\n\nFollowup question 1")
# print(bot.ask("How many days is that?"))
# print("\n\n question 2")
# print(bot.ask("Tell me about maternity leave."))
# print("\n\nFollowup question 2")
# print(bot.ask("What is the duration?"))
# print("\n\n question 3")
# print(bot.ask("Can I take leave during probation?"))
# print("\n\nFollowup question 3")
# print(bot.ask("How much annual leave can I use?"))
