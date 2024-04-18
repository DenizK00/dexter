class Problem:
    def __init__(self, objective:str, constraints:list[str]):
        self.objective = Equation(objective.strip("max", "min"))