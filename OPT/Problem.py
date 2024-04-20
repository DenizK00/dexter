from Equation import Equation
import pyomo.environ as pyo

class Problem:
    def __init__(self, objective:str, constraints:list[str]):
        self.objective = Equation(objective.upper().strip("max"))
        self.constraints = [Equation(c, str(i)) for i, c in enumerate(constraints)]
        self.definition = str(self.objective) + "\n" + "\n".join(str(constraint) for constraint in self.constraints)

        self.model = self.construct_model()

    def __str__(self):
        return self.definition
    
    def construct_model(self) -> pyo.ConcreteModel:
        pass
        


p1 = Problem(objective="Max 3x + 5y", constraints=["2x + 10y <= 20"])
print(p1.objective)