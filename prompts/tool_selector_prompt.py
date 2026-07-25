class ToolSelectionPrompt:

    def create(self, query, tools_registry):
        tool_lines = []
        for tool_name, tool_obj in tools_registry.items():
            tool_lines.append(f"- {tool_name}: {tool_obj['description']}")
        allowed_tools_with_desc = "\n".join(tool_lines)
        prompt = f"""/no_think
You are a tool selector. Your ONLY job is to pick the ONLY ONE correct tool.

USER QUERY: "{query}"

AVAILABLE TOOLS:
{allowed_tools_with_desc}

RULES:
1. Match the query's INTENT to the correct tool
2. Return ONLY the tool name (e.g., "leave_balance")
3. If no tool matches, return "NONE"
"""

        return prompt