from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


class MyAgent(Agent):
    def __init__(self, name, model):
        super().__init__(name, model)
        self.name = name
        self.infection = 0

    def step(self):
        print("{} activated".format(self.name))
        

class MyModel(Model):
    def __init__(self, n_agents):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(10, 10, torus=True)
        for i in range(n_agents):
            a = MyAgent(i, self)
            self.schedule.add(a)
            coords = (self.random.randrange(0, 10), self.random.randrange(0, 10))
            self.grid.place_agent(a, coords)
        
        self.dc = DataCollector(model_reporters={"agent_count": lambda m: m.schedule.get_agent_count()},
                                agent_reporters={"name": lambda a: a.name})

    def step(self):
        self.schedule.step()
        self.dc.collect(self)

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}
    return portrayal

# grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
# server = ModularServer(MyModel,
#                        [grid],
#                        "My Model",
#                        {'n_agents': 10})
# server.launch()

if __name__ == '__main__':
    model = MyModel(5)
    for _ in range(10):
        model.step()
    
    model_df = model.dc.get_model_vars_dataframe()
    agent_df = model.dc.get_agent_vars_dataframe()

    print(agent_df)