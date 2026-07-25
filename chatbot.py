from langchain_ollama import OllamaLLM
import config
from tools.registry import tools_registry
from prompts import tool_selector_prompt
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

    def _select_tool(self, query):
        prompt = tool_selector_prompt.ToolSelectionPrompt().create(query, tools_registry)
        answer = self.llm.invoke(prompt)
        return answer

    def _execute_tool(self, tool_name, params):
        if tool_name in tools_registry:
            print(tool_name, params)
            tool_function = tools_registry[tool_name]["function"]
            if params:
                results = tool_function(params)
                results = {
                    "source": "tools",
                    "data": results
                }
                return results
            else:
                return "Employee ID not provided"
        return None

    def ask(self, query):
        history = self.memory.get_history()
        query_enhanced = self.query_enhancer.enhance(query, history)
        tool_name = self._select_tool(query_enhanced)
        if tool_name == "NONE":
            tool_result = self._retrive_documents(query_enhanced)
        else:
            employee_id = 102
            tool_result = self._execute_tool(tool_name, employee_id)
        #retrived_docs = self._retrive_documents(query_enhanced)
        genPrompt = self.prompt_builder.create(query, tool_result, history)
        answers = self._ask_llm(genPrompt)
        self.memory.add("user", query)
        self.memory.add("Assistant", answers)
        return answers

if __name__ == "__main__": 
    bot = HRChatbot() # Prints: Bot created! 
    answer = bot.chat(query="what is my sick leave policy ?") 
    print(answer)