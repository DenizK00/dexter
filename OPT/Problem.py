from Equation import Equation
import pyomo.environ as pyo

class Problem:
    def __init__(self, objective:str, constraints:list[str]):
        self.objective = Equation(objective.upper().strip("max"))
        self.constraints = [Equation(c, str(i)) for i, c in enumerate(constraints)]
        self.definition = str(self.objective) + "\n" + "\n".join(str(constraint) for constraint in self.constraints)
        self.model = self.construct_model()
        
        var_set = set()
        for constraint in self.constraints:
            for var in constraint.variables:
                var_set.add(var)

        self.variables = var_set


    def __str__(self):
        return self.definition
    
    def construct_model(self) -> pyo.ConcreteModel:
        model = pyo.ConcreteModel        


p1 = Problem(objective="Max 3x + 5y", constraints=["2x + 10y <= 20"])
print(p1.objective)
print(p1.variables)