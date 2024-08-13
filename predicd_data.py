# Import necessary modules
import requests, json

from typing import Final
from datetime import datetime
from betting_data import GetBettingData

# Getting parameterized data from predicd api
def GetPredicdData(authTokenPredicd: str, authTokenBetting: str, apiUrlPredicd: str, apiUrlBetting: str, doubleChance: int, win: int) -> str:
    
    dateFormat: Final = "%Y-%m-%dT%H:%M:%SZ"
    
    # Define the headers to be sent with the GET request
    headers = {
        "User-Agent": "MatchMagic/1.0",
        "Accept": "application/json",
        "Authorization": authTokenPredicd
    }

    # Make the GET request with headers
    response = requests.get(apiUrlPredicd, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        try:
            data = response.json()
            
            # Initialize an empty string
            data_string = ""

            # Loop through each match and print analysis
            for match in data:
                prob_home_win = match['probHomeWin']
                prob_away_win = match['probAwayWin']
                prob_draw = match['probDraw']

                # Check for high probability home win
                if prob_home_win > win:
                    oddResult, oddOver = GetBettingData(authTokenBetting, apiUrlBetting, match['homeTeamName'], round(match['expectedHomeGoals']), match['awayTeamName'], round(match['expectedAwayGoals']), '1')

                    data_string += f"""
                    \n\n🏟️ {match['homeTeamName']} vs {match['awayTeamName']}
                    \n⏱️ {datetime.strptime(match['dateTime'], dateFormat).strftime('%H:%M')}
                    \n 🎯 {match['homeTeamName']} ({match['probHomeWin']}%) : [{oddResult}]
                    \n ⚽️ Over {round(match['expectedHomeGoals']) - 0.5} : [{oddOver}]"""

                # Check if the probability of a home win or a draw exceeds the threshold
                elif ((prob_home_win + prob_draw) > doubleChance):
                    oddResult, oddOver = GetBettingData(authTokenBetting, apiUrlBetting, match['homeTeamName'], round(match['expectedHomeGoals']), match['awayTeamName'], round(match['expectedAwayGoals']), '1x')

                    data_string += f"""
                    \n\n🏟️ {match['homeTeamName']} vs {match['awayTeamName']}
                    \n⏱️ {datetime.strptime(match['dateTime'], dateFormat).strftime('%H:%M')}
                    \n 🎯 1x ({match['probHomeWin']}% + {match['probDraw']}%) : [{oddResult}]
                    \n ⚽️ Over {round(match['expectedHomeGoals']) - 0.5} : [{oddOver}]"""

                # Check for high probability away win
                elif prob_away_win > win:
                    oddResult, oddOver = GetBettingData(authTokenBetting, apiUrlBetting, match['homeTeamName'], round(match['expectedHomeGoals']), match['awayTeamName'], round(match['expectedAwayGoals']), '2')

                    data_string += f"""
                    \n\n🏟️ {match['homeTeamName']} vs {match['awayTeamName']}
                    \n⏱️ {datetime.strptime(match['dateTime'], dateFormat).strftime('%H:%M')}
                    \n 🎯 {match['awayTeamName']} ({match['probAwayWin']}%) : [{oddResult}]
                    \n ⚽️ Over {round(match['expectedAwayGoals']) - 0.5} : [{oddOver}]"""
                    
                # Check if the probability of an away win or a draw exceeds the threshold
                elif ((prob_away_win + prob_draw) > doubleChance):
                    oddResult, oddOver = GetBettingData(authTokenBetting, apiUrlBetting, match['homeTeamName'], round(match['expectedHomeGoals']), match['awayTeamName'], round(match['expectedAwayGoals']), 'x2')

                    data_string += f"""
                    \n\n🏟️ {match['homeTeamName']} vs {match['awayTeamName']}
                    \n⏱️ {datetime.strptime(match['dateTime'], dateFormat).strftime('%H:%M')}
                    \n 🎯 x2 ({match['probDraw']}% + {match['probAwayWin']}%) : [{oddResult}]
                    \n ⚽️ Over {round(match['expectedAwayGoals']) - 0.5} : [{oddOver}]"""

            return data_string if data_string else "No predictions for these requirements!"

        except json.JSONDecodeError:
            return "Failed to parse JSON response"
    else:
        return f"Request failed with status code: {response.status_code}"