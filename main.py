
import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd
from datetime import datetime


page = requests.get("https://www.psl.co.za/matchcentre?type=log")


soup = BeautifulSoup(page.content, "html.parser")

table_tbody = soup.find("tbody", id="LogViewContent")

team_elements = table_tbody.find_all("tr") # contains a list of <tr> elements

psl_df = pd.DataFrame(columns=['position', 'logo', 'name', 'played', 'won','draw', 'lost', 'goals_for', 'goals_against','goal_difference','points','date_last_updated'])

for index,value in enumerate(team_elements):

    print(f"---------------Adding Team: {index}----------------------------------")

    team_position = value.find("h5", class_="team-meta__name").getText()

    team_logo = value.find("img")["src"]

    team_name = value.find("h6", class_="team-meta__name").getText()

    team_played = value.find("td", class_="logs-played").getText()

    team_won = value.find("td", class_="logs-win").getText()

    team_draw = value.find("td", class_="logs-draw").getText()

    team_lost = value.find("td", class_="logs-lost").getText()

    team_goals_for = value.find("td", class_="logs-goals-for").getText()

    team_goals_against = value.find("td", class_="logs-goals-against").getText()

    team_difference = value.find("td", class_="logs-goal-diff").getText()

    team_points= value.find("td", class_="logs-points").getText()
    
    full_team_info = {
        "position": team_position,
        "logo": urllib.parse.quote(team_logo, safe=":/"),
        "name": team_name,
        "played": team_played,
        "won": team_won,
        "draw": team_draw,
        "lost": team_lost,
        "goals_for": team_goals_for,
        "goals_against": team_goals_against,
        "goal_difference": team_difference,
        "points": team_points,
        "date_last_updated": datetime.now()
    }
    
    psl_df = pd.concat([psl_df, pd.DataFrame([full_team_info])], ignore_index=True)

    print(f"---------------Team {index} has been successfully added--------------------")

psl_df.to_csv('betway_premiership_league_table_windows.csv', index=False)
