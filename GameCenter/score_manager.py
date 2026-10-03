import json
import os
from datetime import datetime

SCORE_FILE = "score.json"
def load_scores():
    if not os.path.exists(SCORE_FILE):
        return []
    try:
        with open(SCORE_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_scores(scores):
    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f)

def find_player(players, player_name):
    for player in players:
        if player['name'] == player_name:
            return player
    return None

def update_score(player_name, game, new_scores):
    players = load_scores()
    player = find_player(players, player_name)
    score_key = f"score_{game}"
    if player is None: # нов играч
        new_players = {"name": player_name, "score_angry_birds": 0, "score_snake": 0}
        new_players[score_key] = new_scores
        players.append(new_players)
    else: # съществуващ играч
        if score_key not in players:
            player[score_key] = new_scores
        else:
            if new_scores>player[score_key]:
                player[score_key] = new_scores
    save_scores(players)


