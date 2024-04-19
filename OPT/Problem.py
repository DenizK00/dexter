from Equation import Equation

class Problem:
    def __init__(self, objective:str, constraints:list[str]):
        self.objective = Equation(objective.upper().strip("max"))
        self.constraints = [Equation(c) for c in constraints]



p1 = Problem(objective="Max 3x + 5y", constraints=["2x + 10y <= 20"])
print(p1.objective)