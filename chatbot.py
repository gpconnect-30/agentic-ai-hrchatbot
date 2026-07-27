from langchain_ollama import OllamaLLM
import config,json
from tools.registry import tools_registry
from prompts import tool_selector_prompt
class HRChatbot:
    def __init__(self, llm, query_enhancer, retriever, prompt, memory):
        self.retriever = retriever
        self.prompt_builder = prompt
        self.memory = memory
        self.llm = llm
        self.query_enhancer = query_enhancer
            
    def _retrive_documents(self, query):
        results = self.retriever.invoke(query)
        return results

    def _ask_llm(self, prompt):
        answer = self.llm.stream(prompt)
        full_response = ""
        for chunk in answer:
            full_response += chunk
            print(chunk, end="", flush=True)
        return full_response

    def _select_tool(self, query):
        prompt = tool_selector_prompt.ToolPlannerPrompt().create(query, tools_registry, self.memory)
        raw_answer = self.llm.invoke(prompt)
        answer = json.loads(raw_answer)
        return answer

    def _execute_plan(self, plan):
        results = []
        for action in plan:
            tool_output = self._execute_tool(action)
            results.append(tool_output)
        return results

    def _execute_tool(self, tool_data):
        tool_name = tool_data.get("tool")
        tool_params = tool_data.get("args", {})
        if tool_name in tools_registry:
            tool_function = tools_registry[tool_name]["function"]
            results = tool_function(**tool_params)
            return results
        else:
            return {"source": "tools", "success": False, "data": f"Tool {tool_name} is not found"}

    def ask(self, query):
        history = self.memory.get_history()
        query_enhanced = self.query_enhancer.enhance(query, history)
        #print(query_enhanced)
        tool_data = self._select_tool(query_enhanced)
        #print(tool_data)
        tool_result = self._execute_plan(tool_data)
        genPrompt = self.prompt_builder.create(query, tool_result, history)
        answers = self._ask_llm(genPrompt)
        self.memory.add("user", query)
        self.memory.add("Assistant", answers)
        return answers

if __name__ == "__main__": 
    bot = HRChatbot() # Prints: Bot created! 
    answer = bot.chat(query="what is my sick leave policy ?") 
    print(answer)