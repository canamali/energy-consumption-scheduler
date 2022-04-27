import random
from math import ceil

from numpy import sort

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


class X_n:
    def __init__(self, appliance, consumption=0, type_of_load="shiftable") -> None:
        self.name = appliance
        self.consumption = consumption
        self.type = type_of_load

    def set_hour(self, hour_of_the_day: int):
        if 1 <= hour_of_the_day <= 24:
            raise ("Hour should a number of the range [1, 24] inclusive.")
        self.hour_of_the_day = hour_of_the_day

    def __str__(self) -> str:
        return f"{self.name}-{self.type}"

    def __repr__(self) -> str:
        return f"{self.name}"


def user_n_duration(An_i):
    An_i["user__duration"] = random.uniform(
        An_i["average_use_duration"] * 0.7, An_i["average_use_duration"] * 1.25
    )
    An_i["user__duration"] = An_i["user__duration"] if An_i["user__duration"]<=24 else 24
    return An_i


# There would be 20 users in this game.
N = 1

# There should be a data point for shiftable and non- shiftable loads and we
# make that data for each users of the game randomly. We assigning
# probability of picking to those ones too at every hour and stuff
SHIFTABLE = "shiftable"
NON_SHIFTABLE = "non_shiftable"
LOADS_DATA = {
    "shiftable": [
        {
            "name": "washing machine",  # name of the appliance
            "average_use_duration": 1,  # the probability factor for whether a user would use it or not
            "consumption": 5.4,  # the consumption in kW/hr
            "type": SHIFTABLE,
        },
        {
            "name": "dishwasher",
            "average_use_duration": 3,
            "consumption": 4,
            "type": SHIFTABLE,
        },
        {
            "name": "cloth dryer",
            "average_use_duration": 2,
            "consumption": 8,
            "type": SHIFTABLE,
        },
        {
            "name": "plug in EV vehicles",
            "average_use_duration": 3,
            "consumption": 30.4,
            "type": SHIFTABLE,
        },
        {
            "name": "phone charging",
            "average_use_duration": 5,
            "consumption": 10,
            "blocks": 1.5,
            "spacing": 8,
            "type": SHIFTABLE,
        },
        {
            "name": "Laptop charging",
            "average_use_duration": 5,
            "consumption": 60,
            "blocks": 2,
            "spacing": 3,
            "type": SHIFTABLE,
        },
    ],
    "non-shiftable": [
        {
            "name": "refrigerator",
            "average_use_duration": 18,
            "consumption": 10.4,
            "type": NON_SHIFTABLE,
        },
        {
            "name": "lightening",
            "average_use_duration": 20,
            "consumption": 2,
            "type": NON_SHIFTABLE,
        },
        {
            "name": "heating",
            "average_use_duration": 20,
            "consumption": 25.4,
            "type": NON_SHIFTABLE,
        },
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

    shiftables_for_user_n = random.sample(
        LOADS_DATA["shiftable"], k=n__shiftable_appliances
    )
    shiftables_for_user_n = list(
        map(
            user_n_duration,
            shiftables_for_user_n,
        )
    )
    # print(shiftables_for_user_n[0])
    user_data.append(shiftables_for_user_n)

    n__non_shiftable_appliances = random.randint(
        1, len(LOADS_DATA["non-shiftable"])
    )  # randomly get a number of non-shifable appliances

    non_shiftables_for_user_n = random.sample(
        LOADS_DATA["non-shiftable"], k=n__non_shiftable_appliances
    )
    non_shiftables_for_user_n = list(
        map(
            user_n_duration,
            non_shiftables_for_user_n,
        )
    )
    user_data[i].extend(
        non_shiftables_for_user_n
    )  # concatenating the 2 for the given user

print(user_data[:3])
# what is missing, each user would need to have an xn
# getting the xn_s for the different players.
users_X_Ns = []
for i in range(N):# for each user
    users_X_Ns.append(list())
    for j in range(len(user_data[i])):
        current_A_n = user_data[i][j]
        X_n_i = [
            X_n(appliance=current_A_n["name"], consumption=current_A_n["consumption"], type_of_load=current_A_n["type"])
            for k in range(ceil(current_A_n["user__duration"]))
        ]
        users_X_Ns[i].extend(X_n_i)

# print((users_X_Ns[0]))
user_0_schedule_xn = [[] for i in range(24)] # each is for an hour of the day
xns_user0 = users_X_Ns[0]
non_shiftable = list(filter(lambda xn: xn.type == NON_SHIFTABLE, xns_user0))
shiftable = filter(lambda xn: xn.type == SHIFTABLE, xns_user0)
non_shiftable.sort(key=lambda x:x.name)
hour = 0
xn_prev = X_n(appliance=None)
while non_shiftable:
    xn = non_shiftable.pop()
    
    if xn.name != xn_prev.name:
        hour=0
    
    user_0_schedule_xn[hour].append(xn)
    hour+=1
    xn_prev = xn
    
print(user_0_schedule_xn)
# first, I have to guess how long user n is planning on using the equipment -> DONE
# get the number of chunks it can be broken down to
# spread then along the chunks within the alloted spacing of frames.
# DS for user n= [[], []...24], 24 lists of lists, each is an hour.

# use this to properly compute the lns
ln = [[random.random() * 40 + 10] for i in range(N)]
# print(ln)
# Note ln is the vector containing the scheduled daily energy consumption
# for all other users.

# Solve the optimazation problem
# - what are the inputs
# the inputs are the lns of all users
# the output is the minimum value ofr each player
has_not_converged = True
user_n = 0  # picking user 1, index 0
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
