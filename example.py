#The is an an example response returned by sports_arbitrage.py slightly simplified for the purpose of an example.

response = [
  {
  'name': ['Phoenix Suns', 'Utah Jazz'], 
  'arbitrage': [
                  [
                    {'site_key': 'marathonbet', 'last_update': 1645982572, 'odds': {'h2h': [2.28, 1.77]}}, 
                   {'site_key': 'matchbook', 'last_update': 1645982572, 'odds': {'h2h': [2.2, 1.8]}}
                  ],
                  [
                    {'site_key': 'marathonbet', 'last_update': 1645982572, 'odds': {'h2h': [2.28, 1.77]}}, 
                    {'site_key': 'betfair', 'last_update': 1645982570, 'odds': {'h2h': [2.2, 1.8]}}
                  ]
                ]
     },
 {
   'name': ['Houston Rockets', 'Los Angeles Clippers'], 
   'arbitrage': [
                     [
                       {'site_key': 'coral', 'last_update': 1645982577, 'odds': {'h2h': [3.2, 1.36]}}, 
                       {'site_key': 'betfair',  'last_update': 1645982570, 'odds': {'h2h': [3.15, 1.46]}}
                     ],
                     [
                       {'site_key': 'marathonbet', 'last_update': 1645982572, 'odds': {'h2h': [3.32, 1.38]}}, 
                       {'site_key': 'betfair', 'last_update': 1645982570, 'odds': {'h2h': [3.15, 1.46]}}
                     ]
   ]
 }, 
 {
  'name': ['Dallas Mavericks', 'Golden State Warriors'], 
  'arbitrage': [
                    [
                        {'site_key': 'marathonbet', 'last_update': 1645982572, 'odds': {'h2h': [2.5, 1.66]}}, 
                        {'site_key': 'matchbook', 'last_update': 1645982572, 'odds': {'h2h': [2.4, 1.71]}}
                    ], 
                    [
                      {'site_key': 'marathonbet', 'last_update': 1645982572, 'odds': {'h2h': [2.5, 1.66]}}, 
                     {'site_key': 'betfair', 'last_update': 1645982570, 'odds': {'h2h': [2.4, 1.71]}}
                    ]
               ]
 }, 
 {
 'name': ['Los Angeles Lakers', 'New Orleans Pelicans'], 
 'arbitrage': [
                [
                  {'site_key': 'matchbook', 'last_update': 1645982572, 'odds': {'h2h': [2.02, 1.97]}}, 
                  {'site_key': 'williamhill', 'last_update': 1645982572, 'odds': {'h2h': [1.83, 2.0]}}
               ]
            ]
 }
]


#This method of arbitrage relies on the savings earned from placing two simulatenous bets on opposing teams.
# If there is a difference between the cost to place both bets and the profit earned when one bet wins we have an arbitrage opportunity.

#Lets look at the first arbitrage opportunity
arb_1 = response[0]['arbitrage'][0]

#Prints out the odds for each site
for odds in arb_1:
    print(odds['odds']['h2h'])


#Lets create a bet using the odds
def example_bet(bet_1,bet_2):
    bank = 1000
    total_outlay = (bank / bet_1) + (bank / bet_2)
    print(f'The total outlay = {total_outlay}, from a starting balance of {bank} meaning the profit is ${bank-total_outlay} in savings!')
    
    
example_bet(2.28,1.8)

#returns : The total outlay = 994.1520467836258, from a starting balance of 1000 meaning the profit is $5.847953216374208 in savings!
