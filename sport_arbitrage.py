import json
import requests
import time

#GOAL: when run display all possible arbitrage opportunities with percent gain and details of the bet i.e teams/players and betting site
    
def get_sport_keys():
    # Get a list of in-season sports by their keys
    sports_response = requests.get('https://api.the-odds-api.com/v3/sports', params={'api_key': api_key})
    sports_json = json.loads(sports_response.text)
    num_sports = len(sports_json['data'])
    if not sports_json['success']:
        print('There was a problem with the sports request:',sports_json['msg'])
    else:
        print(f'Successfully got {num_sports} sports')
        print('Remaining requests', sports_response.headers['x-requests-remaining'])
        print('Used requests', sports_response.headers['x-requests-used'])
        sports_keys = [i['key'] for i in sports_json['data']]
        print(sports_keys)


def get_odds(sport_key):
        ''' odds_json['data'] contains a list of live and 
         upcoming events and odds for different bookmakers.
         Events are ordered by start time (live events are first)'''

        odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
            'api_key': api_key,
            'sport': sport_key,
            'region': 'uk', # uk | us | eu | au
            'mkt': 'h2h' # h2h | spreads | totals
        })
        
        odds_json = json.loads(odds_response.text)
        num_events = len(odds_json['data'])

        if not odds_json['success']:
            print('There was a problem with the odds request:', odds_json['msg'])
        else:
            print(f'Successfully got {num_events} events')
            print('Remaining requests', odds_response.headers['x-requests-remaining'])
            print('Used requests', odds_response.headers['x-requests-used'])
            return odds_json['data']

def odds_margin(odd_1,odd_2):
    return ((1/odd_1) + (1/odd_2))*100

def is_arbitrage(odds_site_1,odds_site_2):
    home = odds_site_1[0]
    away = odds_site_2[1]

    margin = odds_margin(home,away)
    if margin < 100:
        return True
    else:
        return None



def check_all_games(games):
    
    all_arbitrages = []

    for game in games:
        arbitrages = []
        name = game['teams']
        sites= game['sites']
        
        while len(sites) > 0:
            #print(f'num of sites remaining {len(sites)}')
            site_1 = sites[0]
            odds_site_1 = site_1['odds']['h2h']
            
            for site_2 in sites:
                odds_site_2 = site_2['odds']['h2h']
                arbitrage = is_arbitrage(odds_site_1,odds_site_2)
                
                if arbitrage == True:
                    #print('Arbitrage!',site_1,site_2,sep='\n')
                    arbitrages.append([site_1,site_2])
                else:
                    #print('No Arbitrage!\n')
                    pass
            
            sites.pop(0)

        if arbitrages != []:
            all_arbitrages.append({'name':name,'arbitrage':arbitrages})

    return all_arbitrages



if(__name__=="__main__"):
    api_key = ''
    get_sport_keys()
    games = get_odds('basketball_nba')
    print(check_all_games(games))
