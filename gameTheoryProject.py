import random

# Algorithm 1: Executed by each user.
#                                                                                                                                                  1:
# 2:# Randomly initialize ln and ln-1.
# 3:# Repeat
# 4:# At random time instances Do
# 5:# Solve local problem (29) using IPM [27].
# 6: If # changes compared to current schedule Then Update according to the new solution. 
# 7:Broadcast a control message to announce to the other ECS units across the system.
# 8: End
# 9: End
# 10: If a control message is received Then
# 11: Update accordingly.
# 12: End
# 13: Until no ECS unit announces any new schedule.


# There would be 20 users in this game.
N = 20

# There should be a data point for shiftable and non- shiftable loads and we
# make that data for each users of the game randomly. We assigning
# probability of picking to those ones too at every hour and stuff
LOADS_DATA = {
    "shiftable": [
        {
            "name": "washing machine",  # name of the appliance
            "p_value": 1
            / 24,  # the probability factor for whether a user would use it or not
            "consumption": 5.4,  # the consumption in kW/hr
        },
        {"name": "dishwasher", "p_value": 3 / 24, "consumption": 4},
        {"name": "cloth dryer", "p_value": 2 / 24, "consumption": 8},
        {"name": "plug in EV vehicles", "p_value": 3 / 24, "consumption": 30.4},
    ],
    "non-shiftable": [
        {"name": "refrigerator", "p_value": 18 / 24, "consumption": 10.4},
        {"name": "lightening", "p_value": 20 / 24, "consumption": 2},
        {"name": "heating", "p_value": 20 / 24, "consumption": 25.4},
    ],
}

# In the beginning each players consumption, ln, is randomly picked between
# 10 and 50. This initialising is for hour 1 of the day
# https://www.eia.gov/todayinenergy/detail.php?id=42915
user_data = []  # user appliance set--> `An_i` var in the paper

for i in range(N):
    # randomly get the number of shiftable and non shiftable appliance that user_i is using for the game
    n__shiftable_appliances = random.randint(
        1, len(LOADS_DATA["shiftable"])
    )  # randomly get a number of shifable appliances
    user_data.append(random.choices(LOADS_DATA["shiftable"], k=n__shiftable_appliances))

    n__non_shiftable_appliances = random.randint(
        1, len(LOADS_DATA["non-shiftable"])
    )  # randomly get a number of non-shifable appliances
    user_data[i].extend(
        random.choices(LOADS_DATA["non-shiftable"], k=n__shiftable_appliances)
    )  # concatenating the 2 for the given user

print(user_data[:3])
# what is missing, each user would need to have an xn

ln = [[random.random() * 40 + 10] for i in range(N)]

# Note ln is the vector containing the scheduled daily energy consumption
# for all other users.

# Solve the optimazation problem
# - what are the inputs
# the inputs are the lns of all users
# the output is the minimum value ofr each player
has_not_converged = True
user_n = 0 # picking user 1, index 0
# NOTE: we are working in one hour granularity
while has_not_converged:
    has_not_converged = False
# -see if xn for the particular hour has changed.
# NOTE: denotes the corresponding one-hour energy consumption that is
# scheduled for appliance a by user n at hour h

# - if so, update the appliances in the household to reflect this xn and do
# this with shitable loads

# - broadcast the ln of current user for other users to also make
# optimization.

# if That is to say if a user need better to better optimise
# things, based in the sent ln
# run optimization
