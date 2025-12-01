import gurobipy as gp
from gurobipy import GRB

m = gp.Model("Ohio_State_Scooter_Optimization")
m.Params.LogToConsole = 0

# Scooters available in region i (North, East, South, West) at time t (Morning, Afternoon, Evening)
s = m.addVars(4, 3, vtype=GRB.INTEGER, lb=0, name="scooters")

# Rides starting in region i at time t
r = m.addVars(4, 3, vtype=GRB.INTEGER, lb=0, name="rides")      

m.setObjective(r[0,0] + r[0,1] + r[0,2] + r[1,0] + r[1,1] + r[1,2] + r[2,0] + r[2,1] + r[2,2] + r[3,0] + 
               r[3,1] + r[3,2], GRB.MAXIMIZE)

# Fleet size of 500 total scooters available in the morning, every other time based off original scooters
m.addConstr(s[0,0] + s[1,0] + s[2,0] + s[3,0] == 500)

# Demand Constraints
# Demand Calculated using total students * .06 as well as added demand from students going to and from classes.
# Because class buildings are approximately evenly distributed across campus all rides leaving a region is split evenly
# between the other regions and added to their afternoon demand as they finish their morning classes and leave for home.
m.addConstr(r[0,0] <= 468)
m.addConstr(r[0,1] <= 1110)
m.addConstr(r[0,2] <= 434)

m.addConstr(r[1,0] <= 1351)
m.addConstr(r[1,1] <= 601)
m.addConstr(r[1,2] <= 50)

m.addConstr(r[2,0] <= 591)
m.addConstr(r[2,1] <= 1103)
m.addConstr(r[2,2] <= 417)

m.addConstr(r[3,0] <= 314)
m.addConstr(r[3,1] <= 1118)
m.addConstr(r[3,2] <= 459)

# Total Battery Constraint, rides must be less than 500 * 15
m.addConstr(r[0,0] + r[0,1] + r[0,2] + r[1,0] + r[1,1] + r[1,2] + r[2,0] + r[2,1] + r[2,2] + r[3,0] + r[3,1] + r[3,2] <= 7500)

# Splitting the total battery into time periods allowing 5 rides per time period and 15 rides total before battery is depleted.
m.addConstr(r[0,0] <= 5 * s[0,0])
m.addConstr(r[0,1] <= 5 * s[0,1])
m.addConstr(r[0,2] <= 5 * s[0,2])

m.addConstr(r[1,0] <= 5 * s[1,0])
m.addConstr(r[1,1] <= 5 * s[1,1])
m.addConstr(r[1,2] <= 5 * s[1,2])

m.addConstr(r[2,0] <= 5 * s[2,0])
m.addConstr(r[2,1] <= 5 * s[2,1])
m.addConstr(r[2,2] <= 5 * s[2,2])

m.addConstr(r[3,0] <= 5 * s[3,0])
m.addConstr(r[3,1] <= 5 * s[3,1])
m.addConstr(r[3,2] <= 5 * s[3,2])

# Scooter flow determining number of scooters in each region during the afternoon
# East rides are split into third going to class in three other regions, but because there are no classes in east region
# The North, South, and West rides are split in half assuming the students are traveling to class
m.addConstr(s[0,1] == s[0,0] - r[0,0] + (0.33 * r[1,0] + 0.5 * r[2,0] + 0.5 * r[3,0]))

m.addConstr(s[1,1] == s[1,0] - r[1,0]) #East residents ride to class, no classes east of high street so no rides coming in.

m.addConstr(s[2,1] == s[2,0] - r[2,0] + (0.5 * r[0,0] + 0.33 * r[1,0] + 0.5 * r[3,0]))

m.addConstr(s[3,1] == s[3,0] - r[3,0] + (0.5 * r[0,0] + 0.33 * r[1,0] + 0.5 * r[2,0]))


# Scooter flow determining number of scooters in each region during the evening
# 40% of North, South, West locations demand comes from east residents riding home from class. The rest of the demand is split 
# evenly for people going to class and returning home. Rides from East are all still going to class so split by 3.
m.addConstr(s[0,2] == s[0,1] - r[0,1] + (0.33 * r[1,1] + 0.3 * r[2,1] + 0.3 * r[3,1]))

m.addConstr(s[1,2] == s[1,1] - r[1,1] + (0.4 * r[0,1] + 0.4 * r[2,1] + 0.4 * r[3,1]))

m.addConstr(s[2,2] == s[2,1] - r[2,1] + (0.3 * r[0,1] + 0.33 * r[1,1] + 0.3 * r[3,1]))

m.addConstr(s[3,2] == s[3,1] - r[3,1] + (0.3 * r[0,1] + 0.33 * r[1,1] + 0.3 * r[2,1]))

m.optimize()

print("Objective =", m.objVal)

for v in m.getVars():
    print(v.VarName, v.X)
