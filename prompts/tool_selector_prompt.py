class ToolPlannerPrompt:

    def create(self, query, execution_history, tools_registry, history):
        tool_lines = []
        for tool_name, tool_obj in tools_registry.items():
            desc = tool_obj['description']
            params = tool_obj.get('parameters', None)
            tool_lines.append(f"- {tool_name}: {desc} | Args: {params}")
        allowed_tools_with_desc = "\n".join(tool_lines)
        prompt = f"""/no_think
You are a tool selector. Return ONLY the FIRST action needed for this query.
The system will loop to get the next action.

Query: {query}

 Use the chat history to understand follow-up questions. If the user says 'it', 'that', or 'those', resolve them using the previous conversation.
    {history}

Use RAG for company policies, documents, and knowledge-base questions.
    
Tools:
{allowed_tools_with_desc}

Current authenticated employee:
employee_id = 125


If the checker says something is missing,
choose the tool that can retrieve it.

Do NOT repeat a tool unless the previous execution failed.
Previous actions already done:
{execution_history if execution_history else "None"}

If the latest ExecutionResult is:
- FAILED
- recoverable=False
- Reason: {execution_history}

Do not retry the same action.
Return NONE and add the reason as well.

Return ONLY ONE JSON:
{{"action": "tool", "tool": "tool_name", "args": {{...}}}}
OR
{{"action": "rag", "args": {{"query": "..."}}}}
OR
{{"action": "NONE"}}


Return ONLY the JSON. Nothing else.

IMPORTANT:
Never write explanations.
Never use markdown.
Never write Python code.
Your entire response must start with {{ and end with }}.
"""
        return prompt