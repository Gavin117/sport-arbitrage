import requests
import json
from config import BANKROLL
#https://www.aussportsbetting.com/2009/01/20/arbitrage-betting-2-three-outcome-betting/#:~:text=Three%2DOutcome%20Arbitrage%20Theory&text=The%20sum%20of%20the%20inverses,that%20the%20bookmaker%20is%20taking.


def calculate_arbitrage(home,draw,away):
    '''
    input
    home = 2.38 #odds for outcome 1 (Everton win).
    draw = 3.65 #odds for outcome 2 (draw)
    away = 3.68 #odds for outcome 3 (Everton loss)

    returns
    stakes for each bet plus total profit

    '''
    b1_stake = BANKROLL / (1 + home/draw + home/away)
    b2_stake = BANKROLL / (1 + draw/home + draw/away)
    b3_stake = BANKROLL / (1 + away/home + away/draw)
    profit = b1_stake*home - BANKROLL
    if profit > 0 :
        return b1_stake,b2_stake,b3_stake,profit
    else:
        return False



def find_arbitrage(match):
    high_home_odds = []
    high_draw_odds = []
    high_away_odds = []

    site_odds = match[1]
    home_name = match[0][0]
    draw_name = match[0][1]
    away_name = match[0][2]

    for site in site_odds:
        odds = site[1]
        home = odds[0]
        draw = odds[1]
        away = odds[2]
        high_home_odds.append(home)
        high_draw_odds.append(draw)
        high_away_odds.append(away)

    max_home = max(high_home_odds)
    max_draw = max(high_draw_odds)
    max_away = max(high_away_odds)
    arbitrage = calculate_arbitrage(max_home,max_draw,max_away)
    if arbitrage != False:
        print(f'{home_name}  vs  {away_name}')
        for site in site_odds:
            name = site[0]
            odds =site[1]
            home = odds[0]
            draw = odds[1]
            away = odds[2]
            if home == max_home:
                print(f'Site: {name:<15}    NAME: {home_name:<25}   BET: £{arbitrage[0]:.2f} @ {home}')
            if draw == max_draw:
                print(f'Site: {name:<15}    NAME: {draw_name:<25}   BET: £{arbitrage[1]:.2f} @ {draw}')
            if away == max_away:
                print(f'Site: {name:<15}    NAME: {away_name:<25}   BET: £{arbitrage[2]:.2f} @ {away}')
        print(f'Total Profit:  £{arbitrage[3]:.2f}')
        print()

def three_way_sport(data):
    for game in data:
        team = [game['teams'][0],'Draw',game['teams'][1]]
        sites = game['sites']
        site = [i['site_key']for i in sites]
        odd = [i['odds']['h2h'] for i in sites]
        joined = list(zip(site,odd))
        match = [team,joined]
        find_arbitrage(match)



#print(calculate_arbitrage(3.55,3.77,2.08))