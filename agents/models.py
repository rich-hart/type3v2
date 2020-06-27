from django.db import models

from bases.models import Base


class Agent(Base):
    # profile
    pass

# TODO: USE Human class to load in professional human training test data. 
class Human(Agent):
    pass

class Computer(Agent):
    # profile
    pass

class Action(Base):
    pass

class Policy(Base):
    pass

#TODO: Use procedure to executre many schedules. 
# 1-1 with algo?:
#class Procedure(Policy):
#    Link to neo4j root schedule
#    pass

