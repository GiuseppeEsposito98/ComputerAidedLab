import pandas as pd
import matplotlib.pyplot as plt
#Edge_size;#Players;Time_to_win;Winner_kill;Avg_kill_per_player;Players_speed(cell per iteration)
df = pd.read_csv("result.csv", sep = ";")

df1 = df.sort_values(by = ["#Players", "Edge_size"])
players_values = list(df["#Players"].unique())
players_df = df1.groupby(df["#Players"])

df2= df.sort_values(by = ["Edge_size", "#Players"])
board_size = list(df2["Edge_size"].unique())
size_df = df2.groupby(df2["Edge_size"])

#time to win with respect to the size of the edgs distinct by the number of players
fig = plt.figure()
for i in players_values:
    plt.plot(players_df.get_group(i)["Edge_size"], players_df.get_group(i)["Time_to_win"])
plt.ylabel("Time_to_win")
plt.xlabel("Edge_size")
plt.legend(labels = players_values, title = "#Players")
plt.savefig("graphs/Edge_size-time_to_win.png")
plt.close(fig)

#time to win with respect to the players speed distinct by the number of players
fig = plt.figure()
for i in players_values:
    plt.plot(players_df.get_group(i)["Players_speed(cell per iteration)"], players_df.get_group(i)["Time_to_win"])
plt.ylabel("Time_to_win")
plt.xlabel("Players_speed(cell per iteration)")
plt.legend(labels = players_values, title = "#Players")
plt.savefig("graphs/players_speed-time_to_win.png")
plt.close(fig)

#time to win with respect to the number of players distinct on the edge size
fig = plt.figure()
for i in board_size:
    plt.plot(size_df.get_group(i)["#Players"], size_df.get_group(i)["Time_to_win"])
plt.ylabel("Time_to_win")
plt.xlabel("#Players")
plt.legend(labels = board_size, title = "Edge_size")
plt.savefig("graphs/#players-time_to_win.png")
plt.close(fig)

#winner kills with respect to the size of the edge distinct by the number of players
fig = plt.figure()
for i in players_values:
    plt.plot(players_df.get_group(i)["Edge_size"], players_df.get_group(i)["Winner_kill"])
plt.ylabel("Winner_kill")
plt.xlabel("Edge_size")
plt.legend(labels = players_values, title = "#Players")
plt.savefig("graphs/Edge_size-winner_kills.png")
plt.close(fig)

#winner kills with respect to the players speed distinct by the number of players
fig = plt.figure()
for i in players_values:
    plt.plot(players_df.get_group(i)["Players_speed(cell per iteration)"], players_df.get_group(i)["Winner_kill"])
plt.ylabel("Winner_kill")
plt.xlabel("Players_speed(cell per iteration)")
plt.legend(labels = players_values, title = "#Players")
plt.savefig("graphs/players_speed-winner_kills.png")
plt.close(fig)

#winner kills with respect to the number of players distinct on the edge size
fig = plt.figure()
for i in board_size:
    plt.plot(size_df.get_group(i)["#Players"], size_df.get_group(i)["Winner_kill"])
plt.ylabel("Winner_kill")
plt.xlabel("#Players")
plt.legend(labels = board_size, title = "Edge_size")
plt.savefig("graphs/#Players-winner_kills.png")
plt.close(fig)

#avg kill rate with respect to the size of the edge distinct by the number of players
fig = plt.figure()
for i in players_values:
    plt.plot(players_df.get_group(i)["Edge_size"], players_df.get_group(i)["Avg_kill_per_player"])
plt.ylabel("Avg_kill_per_player")
plt.xlabel("Edge_size")
plt.legend(labels = players_values, title = "#Players")
plt.savefig("graphs/Edge_size-avg_kill_per_player.png")
plt.close(fig)

#avg kill rate with respect to the players speed distinct by the number of players
fig = plt.figure()
for i in players_values:
    plt.plot(players_df.get_group(i)["Players_speed(cell per iteration)"], players_df.get_group(i)["Avg_kill_per_player"])
plt.ylabel("Avg_kill_per_player")
plt.xlabel("Players_speed(cell per iteration)")
plt.legend(labels = players_values, title = "#Players")
plt.savefig("graphs/Players_speed_vs_avg_kill_rate.png")
plt.close(fig)

#avg kill rate with respect to the number of players distinct on the edge size
fig = plt.figure()
for i in board_size:
    plt.plot(size_df.get_group(i)["#Players"], size_df.get_group(i)["Avg_kill_per_player"])
plt.ylabel("Avg_kill_per_player")
plt.xlabel("#Players")
plt.legend(labels = board_size, title = "Edge_size")
plt.savefig("graphs/splayers_vs_avg_kill_rate.png")
plt.close(fig)
