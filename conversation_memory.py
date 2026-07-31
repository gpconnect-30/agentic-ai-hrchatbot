class ConversationMemory:
    def __init__(self):
        self.history = []
        self.execution_history = []
    def add(self, role, query):
        self.history.append({"role": role, "content": query})
    def get_history(self):
        return self.history

