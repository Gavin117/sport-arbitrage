import requests
import json
from config import API_KEY
from twowaysport import two_way_sport
from threewaysport import three_way_sport
#get all active sports by sports key and save in a list:

def get_sport_keys():
    # Get a list of in-season sports by their keys
    sports_response = requests.get('https://api.the-odds-api.com/v3/sports', params={'api_key': API_KEY})
    sports_json = json.loads(sports_response.text)
    num_sports = len(sports_json['data'])
    if not sports_json['success']:
        print('There was a problem with the sports request:',sports_json['msg'])
    else:
        print(f'Successfully got {num_sports} sports')
        print('Remaining requests', sports_response.headers['x-requests-remaining'])
        print('Used requests', sports_response.headers['x-requests-used'])
        sports_keys = [i['key'] for i in sports_json['data']]
        return sports_keys

def get_odds(sport_key):
        ''' odds_json['data'] contains a list of live and 
         upcoming events and odds for different bookmakers.
         Events are ordered by start time (live events are first)'''

        odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
            'api_key': API_KEY,
            'sport': sport_key,
            'region': 'uk', # uk | us | eu | au
            'mkt': 'h2h' # h2h | spreads | totals
        })
        
        odds_json = json.loads(odds_response.text)
        num_events = len(odds_json['data'])

        if not odds_json['success']:
            print('There was a problem with the odds request:', odds_json['msg'])
        else:
             print('Requests->  Remaining: ', odds_response.headers['x-requests-remaining'],' Used: ', odds_response.headers['x-requests-used'])
            print(f'Successfully got {num_events} events')
            print(sport_key)
            print()
            #print(f'Starting bankroll: £{bankroll}')
            print()
            return odds_json['data']


def find_arbitrage(data):
    #remove unwanted sites
    sites_to_remove = ['marathonbet']
    for teams in data:
        sites = teams['sites']
        for site in sites:
            for remove_site in sites_to_remove:
                if site['site_key'] == remove_site:
                    sites.remove(site)

    #send data to the correct arb checker 2way or 3way sport
    if (len(data[0]['sites'][0]['odds']['h2h'])) == 2:
        two_way_sport(data)
    elif (len(data[0]['sites'][0]['odds']['h2h'])) == 3:
        three_way_sport(data)
    else:
        print('Sorry there was an issue with the request')


if(__name__=="__main__"):
    all_sports = []

    for sport in all_sports:
        data = get_odds(sport)
        find_arbitrage(data)
