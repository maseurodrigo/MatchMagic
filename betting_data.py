# Import necessary modules
import requests, json

from typing import Final
from jsonpath_ng import jsonpath, parse

def check_json_path_exists(data, path):
    
    # Strip out the square brackets and replace ][ or [ with a dot, and ] with an empty string
    keys = path.strip('[]').replace('][', '.').replace('[', '.').replace(']', '').split('.')
    
    current = data

    # Traverse through each key in the path
    for key in keys:
        # Check if the current level is a dictionary and the key exists
        if isinstance(current, dict) and key in current:
            # Move to the next level in the dictionary
            current = current[key]
        else:
            # If the key doesn't exist or current isn't a dictionary return False
            return False
    # If all keys are found return True
    return True
    
# Getting parameterized data from predicd api
def GetBettingData(authToken: str, apiUrl: str, teamA: str, goalsTeamA: int, teamB: str, goalsTeamB: int, pickedBet: str) -> tuple[str, str, str]:
    
    # Define the headers to be sent with the GET request
    headers = {
        "User-Agent": "MatchMagic/1.0",
        "Accept": "application/json",
        "Authorization": authToken
    }

    # Make the GET request with headers
    response = requests.get(apiUrl, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        try:
            data = response.json()

            # Loop through each match and print analysis
            for match in data:

                # Check if teamA is in team1 and teamB is in team2 (case-insensitive)
                if teamA.lower() in match["team1"].lower() and teamB.lower() in match["team2"].lower():

                    # If the pickedBet is 1 (team1 to win)
                    if pickedBet == "1":

                        # Define the paths
                        pathWin = "match['markets']['win1']['v']"
                        pathOver = f"match['markets']['totals'][{max((goalsTeamA + goalsTeamB) - 1, 0)}]['over']['v']"
                        pathTeamOver = f"match['markets']['totals1'][{max(goalsTeamA - 1, 0)}]['over']['v']"

                        # Check and get the values if paths exist, otherwise return null
                        valueWin = match["markets"]["win1"]["v"] if check_json_path_exists(data, pathWin) else "---"
                        valueOver = match["markets"]["totals"][max((goalsTeamA + goalsTeamB) - 1, 0)]["over"]["v"] if check_json_path_exists(data, pathOver) else "---"
                        valueTeamOver = match["markets"]["totals1"][max(goalsTeamA - 1, 0)]["over"]["v"] if check_json_path_exists(data, pathTeamOver) else "---"

                        return valueWin, valueOver, valueTeamOver

                    # If the pickedBet is 1x (team1 to win or draw)
                    elif pickedBet == "1x":

                        # Define the paths
                        pathWin = "match['markets']['win1X']['v']"
                        pathOver = f"match['markets']['totals'][{max((goalsTeamA + goalsTeamB) - 1, 0)}]['over']['v']"
                        pathTeamOver = f"match['markets']['totals1'][{max(goalsTeamA - 1, 0)}]['over']['v']"

                        # Check and get the values if paths exist, otherwise return null
                        valueWin = match["markets"]["win1X"]["v"] if check_json_path_exists(data, pathWin) else "---"
                        valueOver = match["markets"]["totals"][max((goalsTeamA + goalsTeamB) - 1, 0)]["over"]["v"] if check_json_path_exists(data, pathOver) else "---"
                        valueTeamOver = match["markets"]["totals1"][max(goalsTeamA - 1, 0)]["over"]["v"] if check_json_path_exists(data, pathTeamOver) else "---"
                        
                        return valueWin, valueOver, valueTeamOver

                    # If the pickedBet is 2 (team2 to win)
                    elif pickedBet == "2":

                        # Define the paths
                        pathWin = "match['markets']['win2']['v']"
                        pathOver = f"match['markets']['totals'][{max((goalsTeamA + goalsTeamB) - 1, 0)}]['over']['v']"
                        pathTeamOver = f"match['markets']['totals2'][{max(goalsTeamB - 1, 0)}]['over']['v']"

                        # Check and get the values if paths exist, otherwise return null
                        valueWin = match["markets"]["win2"]["v"] if check_json_path_exists(data, pathWin) else "---"
                        valueOver = match["markets"]["totals"][max((goalsTeamA + goalsTeamB) - 1, 0)]["over"]["v"] if check_json_path_exists(data, pathOver) else "---"
                        valueTeamOver = match["markets"]["totals2"][max(goalsTeamB - 1, 0)]["over"]["v"] if check_json_path_exists(data, pathTeamOver) else "---"
                        
                        return valueWin, valueOver, valueTeamOver

                    # If the pickedBet is x2 (team2 to win or draw)
                    elif pickedBet == "x2":

                        # Define the paths
                        pathWin = "match['markets']['winX2']['v']"
                        pathOver = f"match['markets']['totals'][{max((goalsTeamA + goalsTeamB) - 1, 0)}]['over']['v']"
                        pathTeamOver = f"match['markets']['totals2'][{max(goalsTeamB - 1, 0)}]['over']['v']"

                        # Check and get the values if paths exist, otherwise return null
                        valueWin = match["markets"]["winX2"]["v"] if check_json_path_exists(data, pathWin) else "---"
                        valueOver = match["markets"]["totals"][max((goalsTeamA + goalsTeamB) - 1, 0)]["over"]["v"] if check_json_path_exists(data, pathOver) else "---"
                        valueTeamOver = match["markets"]["totals2"][max(goalsTeamB - 1, 0)]["over"]["v"] if check_json_path_exists(data, pathTeamOver) else "---"
                        
                        return valueWin, valueOver, valueTeamOver

            return "---", "---", "---"

        except json.JSONDecodeError:
            return "Failed to parse JSON response"
    else:
        return f"Request failed with status code: {response.status_code}"