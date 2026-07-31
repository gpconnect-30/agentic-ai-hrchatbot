class CheckerPrompt:
    def create(self, query, enhanced_query, execution_history):
        prompt = f"""

User query: {query}
Enhanced query: {enhanced_query}
execution history: {execution_history}

Rules:
- If all parts of the query are answered → {{"status": "COMPLETE"}}
- If something is missing → {{"status": "MISSING", "info": "what is missing"}}
- Return ONLY the JSON. Nothing else.
"""
        return prompt