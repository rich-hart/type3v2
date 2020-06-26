from django.db import models

from bases.models import Base

class Action(Base):
    pass

class Policy(Base):
    pass

#TODO: Use procedure to executre many schedules. 
# 1-1 with algo?:
#class Procedure(Policy):
#    Link to neo4j root schedule
#    pass

