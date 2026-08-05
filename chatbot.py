from langchain_ollama import OllamaLLM
import config,json
from tools.registry import tools_registry
from prompts import tool_selector_prompt
from prompts.checker_prompt import CheckerPrompt
from agentstate import AgentState
from executionresult import ExecutionResult
from error_recovery import ErrorRecovery

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
        print(f"planner out : {raw_answer}")
        answer = json.loads(raw_answer)
        return answer

    def _execute_action(self, tool_data):
        action_type = tool_data.get("action")
        tool_name = tool_data.get("tool")
        args = tool_data.get("args", {})

        results = ExecutionResult(action=action_type)

        if action_type == "tool":
            if tool_name in tools_registry:
                results.source = tool_name
                tool_function = tools_registry[tool_name]["function"]
                data = tool_function(**args)

                if data is None:
                    results.status = "FAILED"
                    results.error = f"Employee ID {args.get('employee_id')} is not found"
                    results.data = None
                    results.recoverable = False
                else:
                    results.data = data
            else:
                results.status = "FAILED"
                results.error = f"Tool {tool_name} is not found"
                results.recoverable = True

        elif action_type == "rag":
            results.source = "rag"
            results.data = self._retrive_documents(**args)

        else:
            results.status = "FAILED"
            results.error = f"Unsupported action type: {action_type}"
            results.recoverable = True

        return results

    def _recover(self, latest_action, execution_result):
        if execution_result.status != "FAILED":
            return execution_result
        
        if execution_result.recoverable:
            for attempt in range(1, 4):
                print(f"Recovery Started.... Attempt {attempt}/3")
                retry_result = self._execute_action(latest_action)
                print(retry_result)

                if retry_result.status != "FAILED":
                    return retry_result

                execution_result = retry_result
        #self.error_recovery.record_result(execution_result)
        
        if not execution_result.recoverable:
            return execution_result

    def agent_run(self, query, history):
        state = AgentState(query, history)
        state.enhanced_query = self.query_enhancer.enhance(query, history)
        while state.iteration <= 5:
            state.latest_action = self._planner(state.enhanced_query, state.execution_history)
            #print(f"latest action : {state.latest_action}")
            if state.latest_action["action"] == "NONE":
                break
            else:    
                state.latest_observation = self._execute_action(state.latest_action)
            retry = self._recover(state.latest_action, state.latest_observation)
            #print(retry)
            state.latest_observation = retry
            state.execution_history.append(state.latest_observation)
            print(state.execution_history)
            if retry.status == "SUCCESS":
                checker_prompt = CheckerPrompt.create(self, state.user_query, state.enhanced_query, state.execution_history)
                raw_answer = self.llm.invoke(checker_prompt)
                checker_answer = json.loads(raw_answer)
                if state.execution_history:
                    state.execution_history[-1].checker = checker_answer
                last_entry = state.execution_history[-1]
                if last_entry.checker.get("status") == "COMPLETE":
                    state.finished = True
                    break
            state.iteration += 1
            print(state.iteration)
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