class QueryEnhancer:

    def __init__(self, llm):
        self.llm = llm

    def enhance(self, query, history):
        enahance_prompt = f"""
You are a query enhancer now.

History:
{history}

Query:
{query}

Enhanced query Answer:
Rewrite the user query into a clear search query. Keep the original intent unchanged. Do not generalize the question.
Resolve words like "it", "that", and "those" using the history.

Return ONLY the rewritten query.
Do not add explanations.
Do not add quotes.
Do not add labels like "Enhanced query:".

If the user asks a follow-up question, always use previous conversation to resolve missing nouns.
Do not answer the question.
Do not say you need clarification.

The rewritten query must be understandable without chat history.

Never use words like:
- it
- that
- this
- those

The output should be a complete standalone search query.
"""
        results = self.llm.invoke(enahance_prompt)
        return results