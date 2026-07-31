from langchain_ollama import OllamaLLM
import config,json
from tools.registry import tools_registry
from prompts import tool_selector_prompt
from prompts.checker_prompt import CheckerPrompt
from agentstate import AgentState

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

    def _planner(self, query, execution_history):
        prompt = tool_selector_prompt.ToolPlannerPrompt().create(query, execution_history ,tools_registry, self.memory)
        raw_answer = self.llm.invoke(prompt)
        #print(f"planner out : {raw_answer}")
        answer = json.loads(raw_answer)
        return answer

    def _execute_action(self, tool_data):
        if tool_data.get("action") == "tool":
            tool_name = tool_data.get("tool")
            tool_params = tool_data.get("args", {})
            if tool_name in tools_registry:
                tool_function = tools_registry[tool_name]["function"]
                results = tool_function(**tool_params)
                return results
            else:
                return {"action": "tool", "success": False, "data": f"Tool {tool_name} is not found"}
        elif tool_data.get("action") == "rag":
            rag_params = tool_data.get("args", {})
            rag_result = self._retrive_documents(**rag_params)
            return rag_result

    def agent_run(self, query, history):
        state = AgentState(query, history)
        state.enhanced_query = self.query_enhancer.enhance(query, history)
        while state.iteration <= 5:
            state.latest_action = self._planner(state.enhanced_query, state.execution_history)
            if state.latest_action["action"] == "NONE":
                break
            else:    
                state.latest_observation = self._execute_action(state.latest_action)
            entry = {
                "action": state.latest_action,
                "observation": state.latest_observation
            }
            state.execution_history.append(entry)
            checker_prompt = CheckerPrompt.create(self, state.user_query, state.enhanced_query, state.execution_history)
            raw_answer = self.llm.invoke(checker_prompt)
            checker_answer = json.loads(raw_answer)
            entry["checker"] = checker_answer
            #print(state.iteration)
            last_entry = state.execution_history[-1]
            if last_entry.get("checker", {}).get("status") == "COMPLETE":
                state.finished = True
                break
            #print(f"execution history : {state.execution_history}")
            state.iteration += 1
        return state

    def ask(self, query):
        history = self.memory.get_history()
        agent = self.agent_run(query, history)
        genPrompt = self.prompt_builder.create(query, agent.execution_history, history)
        answers = self._ask_llm(genPrompt)
        self.memory.add("user", query)
        self.memory.add("Assistant", answers)
        return answers

if __name__ == "__main__": 
    bot = HRChatbot() # Prints: Bot created! 
    answer = bot.chat(query="what is my sick leave policy ?") 
    print(answer)