# -----------------------------------------------------------------------------
# File: leaderboard.py
# ACS School Project - Simple Maze Example
# Organization: THUAS (The Hague University of Applied Sciences)
# Location: Delft
# Date: October 2025
# File coded by Ivaylo Ivanov
# -----------------------------------------------------------------------------

import requests
import json
import time

BASE_URL = f"https://api.jsonbin.io/v3/b/68fb6f27ae596e708f28ee52"
HEADERS = {
    "Content-Type": "application/json",
    "X-Master-Key": "$2a$10$He31aGvFgGQVVsu6ygrqCufv1Gwd693YAfIN.QUT0H19/Oi3l2GVy"
}

def fetch_leaderboard():
    try:
        response = requests.get(BASE_URL, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data["record"]["players"]
    except Exception as e:
        print("Failed to fetch leaderboard:", e)
        return []

def update_leaderboard(name, coins, time_taken):
    leaderboard = fetch_leaderboard()

    leaderboard.append({
        "name": name,
        "coins": coins,
        "time": time_taken,
        "timestamp": int(time.time())
    })

    leaderboard = sorted(leaderboard, key=lambda x: (x["time"], -x["coins"]))

    leaderboard = leaderboard[:10]

    try:
        response = requests.put(
            BASE_URL,
            headers=HEADERS,
            json={"players": leaderboard}
        )
        response.raise_for_status()
        print("Leaderboard updated successfully!")
    except Exception as e:
        print("Failed to update leaderboard:", e)

def show_top_players():
    leaderboard = fetch_leaderboard()
    if not leaderboard:
        print("No leaderboard data yet.")
        return

    print("\nTOP 5 PLAYERS")
    print("=====================================")
    for i, player in enumerate(leaderboard[:5], start=1):
        print(f"{i}. {player['name']}  |  Time: {player['time']}s  |  Coins: {player['coins']}")
    print("=====================================\n")
