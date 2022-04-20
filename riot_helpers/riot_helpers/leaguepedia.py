
def get_timeline_stats(data):
    timeline_data = {
        '1': {},
        '2': {},
        '3': {},
        '4': {},
        '5': {},
        '6': {},
        '7': {},
        '8': {},
        '9': {},
        '10': {}
    }
    
    
    for frame in data['frames']:
        if (frame['timestamp'] == 0):
            continue
        else:
            frame_min = (frame['timestamp'] / 60000)
        
        if 10 <= frame_min <= 15:
                        
            for participantStatsId, participantStats in frame['participantFrames'].items():
                
                participant_cs = participantStats['minionsKilled'] + participantStats['jungleMinionsKilled']
                participant_dmg = participantStats['damageStats']['totalDamageDoneToChampions']
                participant_gold = participantStats['totalGold']
                participant_xp = participantStats['xp']
                
                ##### teammates timeline
                team_cs = 0
                team_gold = 0
                team_dmg = 0
                for teamMateStatsId, teamMateStats in frame['participantFrames'].items():
                    if (int(teamMateStatsId) <= 5 and int(participantStatsId) <= 5) or (int(teamMateStatsId) > 5 and int(participantStatsId) > 5):
                        team_cs = team_cs + (teamMateStats['minionsKilled'] + teamMateStats['jungleMinionsKilled'])
                        team_gold = team_gold + teamMateStats['totalGold']
                        team_dmg = team_dmg + teamMateStats['damageStats']['totalDamageDoneToChampions']
                        
                        
                ##### matchup timeline
                matchup_cs = 0
                matchup_dmg = 0
                matchup_gold = 0
                matchup_xp = 0
                for matchupStatsId, matchupStats in frame['participantFrames'].items():
                    if (int(participantStatsId) + 5 == int(matchupStatsId)) or (int(participantStatsId) - 5 == int(matchupStatsId)):
                        matchup_cs = matchupStats['minionsKilled'] + matchupStats['jungleMinionsKilled']
                        matchup_dmg = matchupStats['damageStats']['totalDamageDoneToChampions']
                        matchup_gold = matchupStats['totalGold']
                        matchup_xp = matchupStats['xp']
                        
                timeline_data[str(participantStatsId)]['cs_diff_15'] = participant_cs - matchup_cs
                timeline_data[str(participantStatsId)]['dmg_diff_15'] = participant_dmg - matchup_dmg
                timeline_data[str(participantStatsId)]['gold_diff_15'] = participant_gold - matchup_gold
                timeline_data[str(participantStatsId)]['xp_diff_15'] = participant_xp - matchup_xp
                
                timeline_data[str(participantStatsId)]['cs_team_15'] = team_cs
                timeline_data[str(participantStatsId)]['cs_share_15'] = participant_cs / team_cs
                timeline_data[str(participantStatsId)]['gold_team_15'] = team_gold
                timeline_data[str(participantStatsId)]['gold_share_15'] = participant_gold / team_gold
                timeline_data[str(participantStatsId)]['dmg_team_15'] = team_dmg
                timeline_data[str(participantStatsId)]['dmg_share_15'] = participant_dmg / team_dmg
                
                
                
        if frame_min > 15:
            break
        
    
    return timeline_data
            


def get_postgame_stats_v4(data):
    
    postgame_data = []
    
    game_id = data['game_id']
    blue_team = data['blue_team']
    red_team = data['red_team']
    league = data['league']
    
    participant_data = {
            "game_id": game_id,
            "league": league,
            "blue_team": blue_team,
            "red_team": red_team,
            "summonerId": "",
            "participantId": "",
            "summonerName": "",
            "teamId": "",
            "team": "",
            "team_vs": "",
            "teamPosition": "",
            "assists": "",
            "baronKills": "",
            "bountyLevel": "",
            "champExperience": "",
            "champLevel": "",
            "championId": "",
            "championName": "",
            "consumablesPurchased": "",
            "damageDealtToBuildings": "",
            "damageDealtToObjectives": "",
            "damageDealtToTurrets": "",
            "damageSelfMitigated": "",
            "deaths": "",
            "detectorWardsPlaced": "",
            "doubleKills": "",
            "dragonKills": "",
            "firstBloodAssist": "",
            "firstBloodKill": "",
            "firstTowerAssist": "",
            "firstTowerKill": "",
            "gameEndedInEarlySurrender": "",
            "gameEndedInSurrender": "",
            "goldEarned": "",
            "goldSpent": "",
            "inhibitorKills": "",
            "inhibitorTakedowns": "",
            "inhibitorsLost": "",
            "item0": "",
            "item1": "",
            "item2": "",
            "item3": "",
            "item4": "",
            "item5": "",
            "item6": "",
            "itemsPurchased": "",
            "killingSprees": "",
            "kills": "",
            "largestCriticalStrike": "",
            "largestKillingSpree": "",
            "largestMultiKill": "",
            "longestTimeSpentLiving": "",
            "magicDamageDealt": "",
            "magicDamageDealtToChampions": "",
            "magicDamageTaken": "",
            "neutralMinionsKilled": "",
            "nexusKills": "",
            "nexusLost": "",
            "nexusTakedowns": "",
            "objectivesStolen": "",
            "objectivesStolenAssists": "",
            "pentaKills": "",
            "physicalDamageDealt": "",
            "physicalDamageDealtToChampions": "",
            "physicalDamageTaken": "",
            "quadraKills": "",
            "sightWardsBoughtInGame": "",
            "spell1Casts": "",
            "spell1Id": "",
            "spell2Casts": "",
            "spell2Id": "",
            "spell3Casts": "",
            "spell4Casts": "",
            "summoner1Casts": "",
            "summoner2Casts": "",
            "timeCCingOthers": "",
            "timePlayed": "",
            "totalDamageDealt": "",
            "totalDamageDealtToChampions": "",
            "totalDamageShieldedOnTeammates": "",
            "totalDamageTaken": "",
            "totalHeal": "",
            "totalHealsOnTeammates": "",
            "totalMinionsKilled": "",
            "totalTimeCCDealt": "",
            "totalTimeSpentDead": "",
            "totalUnitsHealed": "",
            "tripleKills": "",
            "trueDamageDealt": "",
            "trueDamageDealtToChampions": "",
            "trueDamageTaken": "",
            "turretKills": "",
            "turretTakedowns": "",
            "turretsLost": "",
            "unrealKills": "",
            "visionScore": "",
            "visionWardsBoughtInGame": "",
            "wardsKilled": "",
            "wardsPlaced": "",
            "win": "",
            "rune0": "",
            "rune1": "",
            "rune2": "",
            "rune3": "",
            "rune4": "",
            "rune5": "",
        }
    postgame_data.append(participant_data)
        
    return postgame_data
    


def get_postgame_stats_v5(data):
    
    postgame_data = []
    
    game_id = data['game_id']
    blue_team = data['blue_team']
    red_team = data['red_team']
    league = data['league']

    for participant in data['participants']:
        gameDuration = data['gameDuration']
        assists = participant['assists']
        baronKills = participant['baronKills']
        bountyLevel = participant['bountyLevel']
        champExperience = participant['champExperience']
        champLevel = participant['champLevel']
        championId = participant['championId']
        championName = participant['championName']
        consumablesPurchased = participant['consumablesPurchased']
        damageDealtToBuildings = participant['damageDealtToBuildings']
        damageDealtToObjectives = participant['damageDealtToObjectives']
        damageDealtToTurrets = participant['damageDealtToTurrets']
        damageSelfMitigated = participant['damageSelfMitigated']
        deaths = participant['deaths']
        detectorWardsPlaced = participant['detectorWardsPlaced']
        doubleKills = participant['doubleKills']
        dragonKills = participant['dragonKills']
        firstBloodAssist = participant['firstBloodAssist']
        firstBloodKill = participant['firstBloodKill']
        firstTowerAssist = participant['firstTowerAssist']
        firstTowerKill = participant['firstTowerKill']
        gameEndedInEarlySurrender = participant['gameEndedInEarlySurrender']
        gameEndedInSurrender = participant['gameEndedInSurrender']
        goldEarned = participant['goldEarned']
        goldSpent = participant['goldSpent']
        inhibitorKills = participant['inhibitorKills']
        inhibitorTakedowns = participant['inhibitorTakedowns']
        inhibitorsLost = participant['inhibitorsLost']
        item0 = participant['item0']
        item1 = participant['item1']
        item2 = participant['item2']
        item3 = participant['item3']
        item4 = participant['item4']
        item5 = participant['item5']
        item6 = participant['item6']
        itemsPurchased = participant['itemsPurchased']
        killingSprees = participant['killingSprees']
        kills = participant['kills']
        largestCriticalStrike = participant['largestCriticalStrike']
        largestKillingSpree = participant['largestKillingSpree']
        largestMultiKill = participant['largestMultiKill']
        longestTimeSpentLiving = participant['longestTimeSpentLiving']
        magicDamageDealt = participant['magicDamageDealt']
        magicDamageDealtToChampions = participant['magicDamageDealtToChampions']
        magicDamageTaken = participant['magicDamageTaken']
        neutralMinionsKilled = participant['neutralMinionsKilled']
        nexusKills = participant['nexusKills']
        nexusLost = participant['nexusLost']
        nexusTakedowns = participant['nexusTakedowns']
        objectivesStolen = participant['objectivesStolen']
        objectivesStolenAssists = participant['objectivesStolenAssists']
        participantId = participant['participantId']
        pentaKills = participant['pentaKills']
        physicalDamageDealt = participant['physicalDamageDealt']
        physicalDamageDealtToChampions = participant['physicalDamageDealtToChampions']
        physicalDamageTaken = participant['physicalDamageTaken']
        quadraKills = participant['quadraKills']
        sightWardsBoughtInGame = participant['sightWardsBoughtInGame']
        spell1Casts = participant['spell1Casts']
        spell1Id = participant['spell1Id']
        spell2Casts = participant['spell2Casts']
        spell2Id = participant['spell2Id']
        spell3Casts = participant['spell3Casts']
        spell4Casts = participant['spell4Casts']
        summoner1Casts = participant['summoner1Casts']
        summoner2Casts = participant['summoner2Casts']
        summonerName = participant['summonerName']
        teamId = participant['teamId']
        if teamId == 100:
            team = blue_team
            team_vs = red_team
        else:
            team = red_team
            team_vs = blue_team
        if participantId == 1 or participantId == 6:
            teamPosition = "Top"
        elif participantId == 2 or participantId == 7:
            teamPosition = "Jungle"
        elif participantId == 3 or participantId == 8:
            teamPosition = "Mid"
        elif participantId == 4 or participantId == 9:
            teamPosition = "Adc"
        elif participantId == 5 or participantId == 10:
            teamPosition = "Support"
        timeCCingOthers = participant['timeCCingOthers']
        timePlayed = participant['timePlayed']
        totalDamageDealt = participant['totalDamageDealt']
        totalDamageDealtToChampions = participant['totalDamageDealtToChampions']
        totalDamageShieldedOnTeammates = participant['totalDamageShieldedOnTeammates']
        totalDamageTaken = participant['totalDamageTaken']
        totalHeal = participant['totalHeal']
        totalHealsOnTeammates = participant['totalHealsOnTeammates']
        totalMinionsKilled = participant['totalMinionsKilled']
        totalTimeCCDealt = participant['totalTimeCCDealt']
        totalTimeSpentDead = participant['totalTimeSpentDead']
        totalUnitsHealed = participant['totalUnitsHealed']
        tripleKills = participant['tripleKills']
        trueDamageDealt = participant['trueDamageDealt']
        trueDamageDealtToChampions = participant['trueDamageDealtToChampions']
        trueDamageTaken = participant['trueDamageTaken']
        turretKills = participant['turretKills']
        turretTakedowns = participant['turretTakedowns']
        turretsLost = participant['turretsLost']
        unrealKills = participant['unrealKills']
        visionScore = participant['visionScore']
        visionWardsBoughtInGame = participant['visionWardsBoughtInGame']
        wardsKilled = participant['wardsKilled']
        wardsPlaced = participant['wardsPlaced']
        if participant['win'] == True:
            win = 1
        else:
            win = 0
        rune0 = participant['perks']['styles'][0]['selections'][0]['perk']
        rune1 = participant['perks']['styles'][0]['selections'][1]['perk']
        rune2 = participant['perks']['styles'][0]['selections'][2]['perk']
        rune3 = participant['perks']['styles'][0]['selections'][3]['perk']
        rune4 = participant['perks']['styles'][1]['selections'][0]['perk']
        rune5 = participant['perks']['styles'][1]['selections'][1]['perk']
        summonerId = participant['summonerId']
        
        
        dmg_share = 0
        gold_share = 0
        kill_share = 0
        kp = 0
        
        team_dmg = 0
        team_gold = 0
        team_kills = 0
        for teamMateStats in data['participants']:
            if str(teamMateStats['teamId']) == str(teamId):
                team_dmg = team_dmg + teamMateStats['totalDamageDealtToChampions']
                team_gold = team_gold + teamMateStats['goldEarned']
                team_kills = team_kills + teamMateStats['kills']
                
        dmg_share = totalDamageDealtToChampions / team_dmg
        gold_share = goldEarned / team_gold
        if kills == 0 or team_kills == 0:
            kill_share = 0
        else:
            kill_share = kills / team_kills
            
        if (kills + assists) == 0 or team_kills == 0:
            kp = 0
        else:
            kp = (kills + assists) / team_kills
    
        participant_data = {
            "game_id": game_id,
            "league": league,
            "gameDuration": gameDuration,
            "blue_team": blue_team,
            "red_team": red_team,
            "summonerId": summonerId,
            "participantId": participantId,
            "summonerName": summonerName,
            "teamId": teamId,
            "team": team,
            "team_vs": team_vs,
            "teamPosition": teamPosition,
            "assists": assists,
            "baronKills": baronKills,
            "bountyLevel": bountyLevel,
            "champExperience": champExperience,
            "champLevel": champLevel,
            "championId": championId,
            "championName": championName,
            "consumablesPurchased": consumablesPurchased,
            "damageDealtToBuildings": damageDealtToBuildings,
            "damageDealtToObjectives": damageDealtToObjectives,
            "damageDealtToTurrets": damageDealtToTurrets,
            "damageSelfMitigated": damageSelfMitigated,
            "deaths": deaths,
            "detectorWardsPlaced": detectorWardsPlaced,
            "doubleKills": doubleKills,
            "dragonKills": dragonKills,
            "firstBloodAssist": firstBloodAssist,
            "firstBloodKill": firstBloodKill,
            "firstTowerAssist": firstTowerAssist,
            "firstTowerKill": firstTowerKill,
            "gameEndedInEarlySurrender": gameEndedInEarlySurrender,
            "gameEndedInSurrender": gameEndedInSurrender,
            "goldEarned": goldEarned,
            "goldSpent": goldSpent,
            "inhibitorKills": inhibitorKills,
            "inhibitorTakedowns": inhibitorTakedowns,
            "inhibitorsLost": inhibitorsLost,
            "item0": item0,
            "item1": item1,
            "item2": item2,
            "item3": item3,
            "item4": item4,
            "item5": item5,
            "item6": item6,
            "itemsPurchased": itemsPurchased,
            "killingSprees": killingSprees,
            "kills": kills,
            "largestCriticalStrike": largestCriticalStrike,
            "largestKillingSpree": largestKillingSpree,
            "largestMultiKill": largestMultiKill,
            "longestTimeSpentLiving": longestTimeSpentLiving,
            "magicDamageDealt": magicDamageDealt,
            "magicDamageDealtToChampions": magicDamageDealtToChampions,
            "magicDamageTaken": magicDamageTaken,
            "neutralMinionsKilled": neutralMinionsKilled,
            "nexusKills": nexusKills,
            "nexusLost": nexusLost,
            "nexusTakedowns": nexusTakedowns,
            "objectivesStolen": objectivesStolen,
            "objectivesStolenAssists": objectivesStolenAssists,
            "pentaKills": pentaKills,
            "physicalDamageDealt": physicalDamageDealt,
            "physicalDamageDealtToChampions": physicalDamageDealtToChampions,
            "physicalDamageTaken": physicalDamageTaken,
            "quadraKills": quadraKills,
            "sightWardsBoughtInGame": sightWardsBoughtInGame,
            "spell1Casts": spell1Casts,
            "spell1Id": spell1Id,
            "spell2Casts": spell2Casts,
            "spell2Id": spell2Id,
            "spell3Casts": spell3Casts,
            "spell4Casts": spell4Casts,
            "summoner1Casts": summoner1Casts,
            "summoner2Casts": summoner2Casts,
            "timeCCingOthers": timeCCingOthers,
            "timePlayed": timePlayed,
            "totalDamageDealt": totalDamageDealt,
            "totalDamageDealtToChampions": totalDamageDealtToChampions,
            "totalDamageShieldedOnTeammates": totalDamageShieldedOnTeammates,
            "totalDamageTaken": totalDamageTaken,
            "totalHeal": totalHeal,
            "totalHealsOnTeammates": totalHealsOnTeammates,
            "totalMinionsKilled": totalMinionsKilled,
            "totalTimeCCDealt": totalTimeCCDealt,
            "totalTimeSpentDead": totalTimeSpentDead,
            "totalUnitsHealed": totalUnitsHealed,
            "tripleKills": tripleKills,
            "trueDamageDealt": trueDamageDealt,
            "trueDamageDealtToChampions": trueDamageDealtToChampions,
            "trueDamageTaken": trueDamageTaken,
            "turretKills": turretKills,
            "turretTakedowns": turretTakedowns,
            "turretsLost": turretsLost,
            "unrealKills": unrealKills,
            "visionScore": visionScore,
            "visionWardsBoughtInGame": visionWardsBoughtInGame,
            "wardsKilled": wardsKilled,
            "wardsPlaced": wardsPlaced,
            "win": win,
            "rune0": rune0,
            "rune1": rune1,
            "rune2": rune2,
            "rune3": rune3,
            "rune4": rune4,
            "rune5": rune5,
            "dmg_share": dmg_share,
            "gold_share": gold_share,
            "kill_share": kill_share,
            "kp": kp
        }
        postgame_data.append(participant_data)
        
    return postgame_data

