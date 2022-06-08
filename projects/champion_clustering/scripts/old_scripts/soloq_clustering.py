import numpy as np
import sklearn.datasets
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import umap

import warnings

warnings.filterwarnings("ignore")

# sns.set(style='white', context='notebook', rc={'figure.figsize':(14,10)})


# soloq_games = pd.read_csv("../data/soloq/Europe_stats.csv")
# soloq_games = soloq_games.dropna()
# # delete games with < 15 mins
# soloq_games = soloq_games[soloq_games['gameEndedInEarlySurrender'] == False]


relevant_cols = [
    "teamPosition", "championId", "championName", "gameDuration", "win",
    "neutralMinionsKilled", "totalMinionsKilled", "cs_diff_at_15",
    "champExperience", "xp_diff", "xp_diff_per_min", "xp_per_min_3_15",
    "damageDealtToBuildings", "damageDealtToObjectives", "damageDealtToTurrets", "damageSelfMitigated", "magicDamageDealt", "magicDamageDealtToChampions", "magicDamageTaken",
    "physicalDamageDealt", "physicalDamageDealtToChampions", "physicalDamageTaken", "totalDamageDealt", "totalDamageDealtToChampions", "totalDamageShieldedOnTeammates",
    "totalDamageTaken", "totalHeal", "totalHealsOnTeammates", "totalUnitsHealed", "trueDamageDealt", "trueDamageDealtToChampions", "trueDamageTaken",
    "totalTimeCCDealt", "timeCCingOthers", "totalTimeSpentDead", "dmg_per_minute_diff", "dmg_per_minute_diff_15", "kills", "deaths", "assists", "kill_share", "kill_participation",
    "doubleKills", "tripleKills", "quadraKills", "pentaKills", "firstBloodAssist", "firstBloodKill", "killingSprees", "largestKillingSpree", "largestMultiKill",
    "goldEarned", "goldSpent", "gold_share", "gold_earned_per_min", "gold_diff_15", "gold_10k_time",
    "inhibitorKills", "inhibitorTakedowns", "inhibitorsLost", 
    "itemsPurchased", "consumablesPurchased",
    "largestCriticalStrike", "longestTimeSpentLiving",
    "firstTowerAssist", "firstTowerKill", "objectivesStolen", "objectivesStolenAssists", "turretKills", "turretTakedowns", "turretsLost",
    "sightWardsBoughtInGame", "visionScore", "visionWardsBoughtInGame", "detectorWardsPlaced", "wardsKilled", "wardsPlaced",
    "spell1Casts", "spell2Casts", "spell3Casts", "spell4Casts", "summoner1Casts", "summoner2Casts",
    "lane_proximity", "jungle_proximity", "percent_mid_lane", "percent_side_lanes", "forward_percentage", "counter_jungle_time_percentage",
]


# select only relevant cols
soloq = soloq_games[ relevant_cols ]


def clean_data(df, role):
    games_df = df[ df['teamPosition'] == role ]
    # list of champions with more than 250 games played
    top_champs = [i for i, x in games_df.championName.value_counts().to_dict().items() if x > 500]
    games_df = games_df[games_df['championName'].isin(top_champs)]
    games_df = games_df.groupby(by='championName').apply(lambda x: x.sample(n=500)).reset_index(level=1, drop=True).drop(['championName'], axis=1).reset_index()
    try:
        games_df = games_df.drop(['teamPosition'], axis=1)
        games_df = games_df.drop(['Unnamed: 0'], axis=1)
    except Exception as e:
        print(e)
    return games_df
    



top_soloq = clean_data(soloq, "TOP")
jungle_soloq = clean_data(soloq, "JUNGLE") 
mid_soloq = clean_data(soloq, "MIDDLE") 
bottom_soloq = clean_data(soloq, "BOTTOM") 
utility_soloq = clean_data(soloq, "UTILITY")

print("top_soloq: ", top_soloq.shape[0])
print("jungle_soloq: ", jungle_soloq.shape[0])
print("mid_soloq: ", mid_soloq.shape[0])
print("bottom_soloq: ", bottom_soloq.shape[0])
print("utility_soloq: ", utility_soloq.shape[0])


scaler = StandardScaler()

top_soloq_values = top_soloq.drop(['championName', 'championId'], axis=1).values
scaled_top_soloq = StandardScaler().fit_transform(top_soloq_values)

umap_2d = umap.UMAP(n_components=2, init='random', random_state=0)
top_soloq_reduced_2 = umap_2d.fit_transform(scaled_top_soloq)


pendigits = sklearn.datasets.load_digits()
mnist = sklearn.datasets.fetch_openml('mnist_784')
fmnist = sklearn.datasets.fetch_openml('Fashion-MNIST')

mapper = umap.UMAP().fit(pendigits.data)

umap.plot.points(mapper)
