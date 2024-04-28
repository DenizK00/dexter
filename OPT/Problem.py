from Equation import Equation
import pyomo.environ as pyo

class Problem:
    def __init__(self, objective:str, constraints:list[str]):
        self.model = self.construct_model(objective, constraints)

    def __str__(self):
        return self.definition
    
    def __repr__(self):
        return f"Problem(objective={self.objective!r}, constraints={self.constraints})"
    
    def construct_model(self, objective, constraints) -> pyo.ConcreteModel:
        model = pyo.ConcreteModel()

        self.objective = Equation(objective.upper().strip("max"))
        self.constraints = [Equation(c, str(i)) for i, c in enumerate(constraints)]

        self.definition = str(self.objective) + "\n" + "\n".join(str(constraint) for constraint in self.constraints)
        
        return model
            
    def solve(self):
        pass

