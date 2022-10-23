import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results.csv", sep = ";")

df1 = df.sort_values(by = ["#Players", "Board edge"])
players_values = list(set(list(df["#Players"])))
players_df = df1.groupby(df["#Players"])

df2= df.sort_values(by = ["Board edge", "#Players"])
board_size = list(set(list(df2["Board edge"])))
size_df = df2.groupby(df2["Board edge"])

#time in function of the size of the board distinct by the number of players
fig = plt.figure()
for i in players_values:
    plt.plot(players_df.get_group(i)["Board edge"], players_df.get_group(i)["Time to win"])
plt.ylabel("Time to win")
plt.xlabel("Board edge")
plt.legend(labels = players_values, title = "#Players")
plt.savefig("graphs/board_edge_vs_time.png")
plt.close(fig)

#time in function of the mobility speed distinct by the number of players
fig = plt.figure()
for i in players_values:
    plt.plot(players_df.get_group(i)["Mobility speed (cell per iteration)"], players_df.get_group(i)["Time to win"])
plt.ylabel("Time to win")
plt.xlabel("Mobility speed (cell per iteration)")
plt.legend(labels = players_values, title = "#Players")
plt.savefig("graphs/mobility_speed_vs_time.png")
plt.close(fig)

#time in function of the number of players distinct on the board size
fig = plt.figure()
for i in board_size:
    plt.plot(size_df.get_group(i)["#Players"], size_df.get_group(i)["Time to win"])
plt.ylabel("Time to win")
plt.xlabel("#Players")
plt.legend(labels = board_size, title = "Board edge")
plt.savefig("graphs/players_vs_time.png")
plt.close(fig)

#kills in function of the size of the board distinct by the number of players
fig = plt.figure()
for i in players_values:
    plt.plot(players_df.get_group(i)["Board edge"], players_df.get_group(i)["#Kills for the winner"])
plt.ylabel("#Kills for the winner")
plt.xlabel("Board edge")
plt.legend(labels = players_values, title = "#Players")
plt.savefig("graphs/board_edge_vs_kills.png")
plt.close(fig)

#kills in function of the mobility speed distinct by the number of players
fig = plt.figure()
for i in players_values:
    plt.plot(players_df.get_group(i)["Mobility speed (cell per iteration)"], players_df.get_group(i)["#Kills for the winner"])
plt.ylabel("#Kills for the winner")
plt.xlabel("Mobility speed (cell per iteration)")
plt.legend(labels = players_values, title = "#Players")
plt.savefig("graphs/mobility_speed_vs_kills.png")
plt.close(fig)

#kills in function of the number of players distinct on the board size
fig = plt.figure()
for i in board_size:
    plt.plot(size_df.get_group(i)["#Players"], size_df.get_group(i)["#Kills for the winner"])
plt.ylabel("#Kills for the winner")
plt.xlabel("#Players")
plt.legend(labels = board_size, title = "Board edge")
plt.savefig("graphs/layers_vs_kills.png")
plt.close(fig)

#avg kill rate in function of the size of the board distinct by the number of players
fig = plt.figure()
for i in players_values:
    plt.plot(players_df.get_group(i)["Board edge"], players_df.get_group(i)["Avg rate kills"])
plt.ylabel("Avg rate kills")
plt.xlabel("Board edge")
plt.legend(labels = players_values, title = "#Players")
plt.savefig("graphs/board_edge_vs_avg_kill_rate.png")
plt.close(fig)

#avg_kill_rate in function of the mobility speed distinct by the number of players
fig = plt.figure()
for i in players_values:
    plt.plot(players_df.get_group(i)["Mobility speed (cell per iteration)"], players_df.get_group(i)["Avg rate kills"])
plt.ylabel("Avg rate kills")
plt.xlabel("Mobility speed (cell per iteration)")
plt.legend(labels = players_values, title = "#Players")
plt.savefig("graphs/mobility_speed_vs_avg_kill_rate.png")
plt.close(fig)

#avg kill rate in function of the number of players distinct on the board size
fig = plt.figure()
for i in board_size:
    plt.plot(size_df.get_group(i)["#Players"], size_df.get_group(i)["Avg rate kills"])
plt.ylabel("Avg rate kills")
plt.xlabel("#Players")
plt.legend(labels = board_size, title = "Board edge")
plt.savefig("graphs/splayers_vs_avg_kill_rate.png")
plt.close(fig)
