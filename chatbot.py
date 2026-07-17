#from langchain_chroma import Chroma
#from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
import config

class HRChatbot:
    def __init__(self, llm, query_enhancer, retriever, prompt, memory):
        #self.vector_store = self._load_vector_store()
        self.retriever = retriever
        self.prompt_builder = prompt
        self.memory = memory
        self.llm = llm
        self.query_enhancer = query_enhancer
            
    def _retrive_documents(self, query):
        results = self.retriever.invoke(query)
        #print("User question: ", query)
        return results

    def _ask_llm(self, prompt):
        answer = self.llm.stream(prompt)
        full_response = ""
        for chunk in answer:
            full_response += chunk
            print(chunk, end="", flush=True)
        return full_response

    def ask(self, query):
        history = self.memory.get_history()
        #print(history)
        query_enhanced = self.query_enhancer.enhance(query, history)
        retrived_docs = self._retrive_documents(query_enhanced)
        genPrompt = self.prompt_builder.create(query, retrived_docs, history)
        answers = self._ask_llm(genPrompt)
        self.memory.add("user", query)
        self.memory.add("Assistant", answers)
        return answers

if __name__ == "__main__":
    bot = HRChatbot()  # Prints: Bot created!

    answer = bot.chat(query="what is my sick leave policy ?")
    print(answer)