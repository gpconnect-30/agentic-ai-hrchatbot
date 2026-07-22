class HRPromptTemplate:
    def create(self, query, tool_decision, history):
        print(tool_decision)
        if tool_decision["source"] == "tools":
            prompt = f"""
    You are an AI HR Support Assistant.

    Answer the employee's question using ONLY the provided company policy.
    If the question is unrelated to the company policies, politely explain that you can only answer questions based on the provided company documents.

    If the answer is not available in the provided context,
    say:
    "I couldn't find that information in the available company policies."
    
    Use the chat history to understand follow-up questions. If the user says 'it', 'that', or 'those', resolve them using the previous conversation.
    {history}

    Employee Quesiton:
    {query}
    Tool result:
    {tool_decision}
    Answer:
    give user human readable format 
"""
        else:
            content = []
            for i in tool_decision:
                content.append(i.page_content)
            context = "\n\n".join(content)

            prompt = f"""
    You are an AI HR Support Assistant.

    Answer the employee's question using ONLY the provided company policy.
    If the question is unrelated to the company policies, politely explain that you can only answer questions based on the provided company documents.

    If the answer is not available in the provided context,
    say:
    "I couldn't find that information in the available company policies."
        
        Company Policy:
        {context}

        Use the chat history to understand follow-up questions. If the user says 'it', 'that', or 'those', resolve them using the previous conversation.
        {history}

        Employee Quesiton:
        {query}
        Answer:
        give user human readable format 
    """
        return prompt
