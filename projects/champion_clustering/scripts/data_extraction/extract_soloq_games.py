import pandas as pd
import json
from riotwatcher import LolWatcher

import riot_helpers



##################################################################
### unique from list
def get_unique(list):
    return (set(list))
##################################################################



##################################################################
### matchlist
def get_matchlist_by_patch(watcher, region, puuid):
    return watcher.match.matchlist_by_puuid(region, puuid, count=100)
##################################################################


##################################################################
##### get puuids from players
def get_puuids(watcher, players):
    puuids = {}
    for region in players:
        region_puuids = {}
        for league in players[region]:
            league_puuids = {}
            for player in players[region][league]:
                player_puuids = []
                for ign in players[region][league][player]:
                    puuid = ""
                    try:
                        if region == "Europe":
                            puuid = watcher.summoner.by_name("euw1", ign)['puuid']
                        elif region == "Asia":
                            puuid = watcher.summoner.by_name("kr", ign)['puuid']
                        elif region == "America":
                            puuid = watcher.summoner.by_name("na1", ign)['puuid']
                    except:
                        pass
                    player_puuids.append(puuid)
                league_puuids.update({player: player_puuids})
            region_puuids.update({league: league_puuids})
        puuids.update({region: region_puuids})
    return puuids
##################################################################


##################################################################
##### get list of games played by player's puuids
def get_puuids_games(watcher, puuids):
    total_match_history = {}
    for region in puuids:
        region_puuids = {}
        region_match_history = []
        for league in puuids[region]:
            league_puuids = {}
            for player in puuids[region][league]:
                player_puuids = []
                for puuid in puuids[region][league][player]:
                    # get player match history
                    try:
                        player_match_history = get_matchlist_by_patch(watcher, region, puuid)
                        region_match_history = region_match_history + player_match_history
                    except Exception as e:
                        print(e)
                        
        region_match_history = get_unique(region_match_history)
        total_match_history[region] = list(region_match_history)
    return total_match_history
##################################################################


##################################################################
##### extract soloq stats from games and store them in pandas dfs
def extract_and_store_games_stats(watcher, game_ids, path="../../data/soloq/"):
    for region in game_ids:
        print(region)
        game_region_stats = []
        for game_id in game_ids[region]:
            
            try:
                # game_data = requests.get("https://europe.api.riotgames.com/lol/match/v5/matches/" + game_id + "?api_key=" + API_KEY).json()
                game_data = watcher.match.by_id(region, game_id)
                timeline_data = watcher.match.timeline_by_match(region, game_id)
            except:
                # time.sleep(1)
                continue
            
            game_stats = riot_helpers.soloq.get_postgame_data(game_id, game_data, timeline_data)
            
            game_region_stats = game_region_stats + game_stats
        
        region_df = pd.DataFrame(game_region_stats)
        region_df.to_csv( path + region + "_stats.csv" )
##################################################################


####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
def main():
    API_KEY = "RGAPI-96c60f53-6735-4031-958f-47e841106f56"
    watcher = LolWatcher(API_KEY)


    try:
        # get all players' ign
        with open("../../data/soloq/aux_datasets/players.json", encoding="utf-8") as players_json:
            players = json.load(players_json)
            
        # get player's puuids
        puuids = get_puuids(watcher, players)
        
        # get player's games played
        game_ids = get_puuids_games(watcher, puuids)

        # extract soloq stats and store them in pandas dfs
        extract_and_store_games_stats(watcher, game_ids)
        
    except Exception as e:
        print(e)
    finally:
        # store puuids
        with open("../../data/soloq/aux_datasets/puuids.json", 'w', encoding="utf-8") as outfile:
            json.dump(puuids, outfile)
        # store game ids
        with open("../../data/soloq/aux_datasets/game_ids.json", 'w', encoding="utf-8") as outfile:
            json.dump(game_ids, outfile)
####################################################################################################################################
####################################################################################################################################

    
    
if __name__ == '__main__':
    main()
