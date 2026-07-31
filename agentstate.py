class AgentState:
    def __init__(self, query, history):
        self.user_query = query
        self.history = history
        self.enhanced_query = None
        self.latest_action = None
        self.latest_observation = None
        self.iteration = 0
        self.execution_history = []
        self.finished = False