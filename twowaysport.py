import requests
import json
import pandas as pd
from config import BANKROLL

def calculate_arbitrage(bet1,bet2):
    imp_bet1 = (1/bet1) *100
    imp_bet2 = (1/bet2) *100
    total_imp = imp_bet1 + imp_bet2
    if total_imp < 100 :
        bet1_stake = (BANKROLL*imp_bet1) / total_imp
        bet2_stake = (BANKROLL*imp_bet2) / total_imp
        return total_imp,bet1_stake,bet2_stake
    else:
        return False


def find_arbitrage(match):
    high_home_odds = []
    high_away_odds = []
    site_odds = match[1]
    home_name = match[0][0]
    away_name = match[0][1]

    for site in site_odds:
        odds = site[1]
        home = odds[0]
        away = odds[1]
        high_home_odds.append(home)
        high_away_odds.append(away)

    max_home = max(high_home_odds)
    max_away = max(high_away_odds)
    arbitrage = calculate_arbitrage(max_home,max_away)
    
    if arbitrage != False:
        implied_margin = arbitrage[0]
        imp_home_stake = arbitrage[1]
        imp_away_stake = arbitrage[2]
        for site in site_odds:
            name = site[0]
            odds =site[1]
            home = odds[0]
            away = odds[1]
            if home == max_home:
                print(f'Site: {name:<15}    NAME: {home_name:<25}   BET: £{imp_home_stake:.2f} @ {home}')
            if away == max_away:
                print(f'Site: {name:<15}    NAME: {away_name:<25}   BET: £{imp_away_stake:.2f} @ {away}')
        print(f'Total Profit:  £{(imp_home_stake*max_home)-BANKROLL:.2f}')
        print()
        print()


def two_way_sport(data):
    # parses data and finds any arbitrage
    # prints bet instructions
    for game in data:
        team = game['teams']
        sites = game['sites']
        site = [i['site_key']for i in sites]
        odd = [i['odds']['h2h'] for i in sites]
        joined = list(zip(site,odd))
        match = [team,joined]
        find_arbitrage(match)
