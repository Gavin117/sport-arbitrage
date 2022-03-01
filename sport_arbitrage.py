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

x =[{'name': ['Phoenix Suns', 'Utah Jazz'], 
    'arbitrage': [[{'site_key': 'marathonbet', 'site_nice': 'Marathon Bet', 'last_update': 1645982572, 'odds': {'h2h': [2.28, 1.77]}}, {'site_key': 'matchbook', 'site_nice': 'Matchbook', 'last_update': 1645982572, 'odds': {'h2h': [2.2, 1.8], 'h2h_lay': [2.24, 1.84]}}],
             [{'site_key': 'marathonbet', 'site_nice': 'Marathon Bet', 'last_update': 1645982572, 'odds': {'h2h': [2.28, 1.77]}}, {'site_key': 'betfair', 'site_nice': 'Betfair', 'last_update': 1645982570, 'odds': {'h2h': [2.2, 1.8], 'h2h_lay': [2.26, 1.84]}}]]},
 {'name': ['Houston Rockets', 'Los Angeles Clippers'], 
 'arbitrage': [[{'site_key': 'coral', 'site_nice': 'Coral', 'last_update': 1645982577, 'odds': {'h2h': [3.2, 1.36]}}, {'site_key': 'betfair', 'site_nice': 'Betfair', 'last_update': 1645982570, 'odds': {'h2h': [3.15, 1.46], 'h2h_lay': [3.2, 1.47]}}],
         [{'site_key': 'marathonbet', 'site_nice': 'Marathon Bet', 'last_update': 1645982572, 'odds': {'h2h': [3.32, 1.38]}}, {'site_key': 'betfair', 'site_nice': 'Betfair', 'last_update': 1645982570, 'odds': {'h2h': [3.15, 1.46], 'h2h_lay': [3.2, 1.47]}}]]}, 
 {'name': ['Dallas Mavericks', 'Golden State Warriors'], 'arbitrage': [[{'site_key': 'marathonbet', 'site_nice': 'Marathon Bet', 'last_update': 1645982572, 'odds': {'h2h': [2.5, 1.66]}}, {'site_key': 'matchbook', 'site_nice': 'Matchbook', 'last_update': 1645982572, 'odds': {'h2h': [2.4, 1.71], 'h2h_lay': [2.42, 1.72]}}], 
    [{'site_key': 'marathonbet', 'site_nice': 'Marathon Bet', 'last_update': 1645982572, 'odds': {'h2h': [2.5, 1.66]}}, {'site_key': 'betfair', 'site_nice': 'Betfair', 'last_update': 1645982570, 'odds': {'h2h': [2.4, 1.71], 'h2h_lay': [2.42, 1.72]}}]]}, 
 {'name': ['Los Angeles Lakers', 'New Orleans Pelicans'], 
 'arbitrage': [[{'site_key': 'matchbook', 'site_nice': 'Matchbook', 'last_update': 1645982572, 'odds': {'h2h': [2.02, 1.97], 'h2h_lay': [2.04, 1.99]}}, {'site_key': 'williamhill', 'site_nice': 'William Hill', 'last_update': 1645982572, 'odds': {'h2h': [1.83, 2.0]}}]]}]

def example_bet():
    bank = 1000
    total_outlay = (bank / 2.28) + (bank / 1.79)
    print(f'The total outlay = {total_outlay}, from a starting balance of {bank} meaning the profit is ${bank-total_outlay} in savings!')


if(__name__=="__main__"):
    api_key = ''
    get_sport_keys()
    games = get_odds('basketball_nba')
    print(check_all_games(games))
