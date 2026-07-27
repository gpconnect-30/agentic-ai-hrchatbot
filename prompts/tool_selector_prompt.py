class ToolPlannerPrompt:

    def create(self, query, tools_registry,history):
        tool_lines = []
        for tool_name, tool_obj in tools_registry.items():
            desc = tool_obj['description']
            params = tool_obj.get('parameters', None)
            tool_lines.append(f"- {tool_name}: {desc} | Args: {params}")
        allowed_tools_with_desc = "\n".join(tool_lines)
        #print(allowed_tools_with_desc)
        prompt = f"""/no_think
You are a tool selector. Your ONLY job is to pick the ONLY correct tools.

USER QUERY: "{query}"

 Use the chat history to understand follow-up questions. If the user says 'it', 'that', or 'those', resolve them using the previous conversation.
    {history}
Current authenticated employee:
employee_id = 104
    
AVAILABLE TOOLS:
{allowed_tools_with_desc}

Instructions:
1. If the query requires multiple tools, respond with a JSON array:
   [
     {{
       "source": "tools",
       "tool": "tool_name_1",
       "args": {{"arg_name": "value"}}
     }},
     {{
       "source": "tools",
       "tool": "tool_name_2",
       "args": {{"arg_name": "value"}}
     }}
   ]
2. Respond ONLY with a valid JSON array matching this structure:
[
   {{
     "source": "tools",
     "tool": "tool_name",
     "args": {{"arg_name": "value"}}
   }}
]
3. If a tool matches, set "source" to "tools".

4. If a tool requires no parameters, use an empty dict for args:
[
   {{
     "source": "tools",
     "tool": "tool_name",
     "args": {{}}
   }}
]
5. If NO tool matches, set "source" to "rag", "tool" to "NONE", and "args" to {{}}:
   [{{
     "source": "rag",
     "tool": "NONE",
     "args": {{}}
   }}]

6. Return ONLY raw JSON with no markdown block fences or extra text.

"""
        return prompt