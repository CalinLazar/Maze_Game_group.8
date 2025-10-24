# -----------------------------------------------------------------------------
# File: corridor.py
# ACS School Project - Simple Maze Example
# Organization: THUAS (The Hague University of Applied Sciences)
# Location: Delft
# Date: July 2025
# -----------------------------------------------------------------------------

import sys
import random
from .utils import chooseNextRoom
from .leaderboard import update_leaderboard, show_top_players
import time

def enterCorridor(state):
    print("\n🚶 You are standing in the school's main corridor.")
    print("You see a long corridor with many doors and glass walls on both side. Behind these door are rooms, waiting to be explored.")

    available_rooms = ["teachersroom1", "lab2001"]

    if state["visited"]["teachersroom1"]:
        available_rooms.append("classroom2015")
    if state["visited"]["lab2001"]:
        available_rooms.append("projectroom1")
    if state["visited"]["projectroom1"]:
        available_rooms.append("projectroom3")
    if state["visited"]["projectroom3"]:
        available_rooms.append("frontdesk")

    escape_trial = 0
    bribe_cost = 200

    def handle_look():
        print("\nYou take a look around.")
        print("Students and teachers are walking in both directions along the corridor. You see several labeled doors.")
        print(f"- Possible doors: {', '.join(available_rooms)}")
        print("- Your current inventory:", state["inventory"])

        nonlocal escape_trial
        if escape_trial == 0 and all([
            state["visited"]["teachersroom1"],
            state["visited"]["classroom2015"],
            state["visited"]["lab2001"],
            state["visited"]["projectroom1"],
            state["visited"]["projectroom3"],
            "Good Classmate Badge" in state['inventory']
        ]):
            user_last_call = str(input("Are you ready for your final challenge? (yes/no)\n"))
            if user_last_call.lower() == 'yes':
                print("You need to choose one of the rooms you have visited to hide from the principal!\nLets hope you are lucky...")
                print("The available rooms are:", list(state['visited']))
                user_room_choice = input("Enter the name of the room you choose to hide in: \n")
                outcome = random.random()

                if outcome < 0.7:
                    print("\nYou hid successfully! The principal couldn’t find you.")
                    print("✨ Congratulations, you have ESCAPED the maze! ✨")

                    end_time = time.time()
                    elapsed = int(end_time - state.get("start_time", end_time))
                    player_name = input("Enter your name for the leaderboard: ")
                    update_leaderboard(player_name, state["coins"], elapsed)
                    show_top_players()
                    sys.exit()
                else:
                    print("\nSuddenly the principal’s voice echoes: \"I FOUND YOU!!!!!!\"")
                    print(f"The principal demands {bribe_cost} coins to let you go...")
                    if state["coins"] >= bribe_cost:
                        give_choice = input(f"Enter 'give' to pay {bribe_cost} coins: ").strip().lower()
                        if give_choice == 'give':
                            state["coins"] -= bribe_cost
                            print(f"You pay {bribe_cost} coins and escape successfully!")
                            end_time = time.time()
                            elapsed = int(end_time - state.get("start_time", end_time))
                            player_name = input("Enter your name for the leaderboard: ")
                            update_leaderboard(player_name, state["coins"], elapsed)
                            show_top_players()
                            sys.exit()
                        else:
                            print("You refused to pay. The principal catches you. Game over.")
                            sys.exit()
                    else:
                        print("You don’t have enough coins. Game over.")
                        sys.exit()
            escape_trial += 1

    def handle_help():
        print("\nAvailable commands:")
        print("- look around         : See what's in the corridor and where you can go.")
        print("- go <room name>      : Move to another room. Example: go classroom2015")
        print("- ?                   : Show this help message.")
        print("- leaderbaord         : Display current leaderboard.")
        print("- wallet              : Show how many coins you have.")
        print("- quit                : Quit the game.")

    def handle_go(room_name):
        room = room_name.lower()
        if room in available_rooms:
            print(f"You walk toward the door to {room}.")
            state["previous_room"] = "corridor"
            return room
        else:
            print(f"❌ '{room_name}' is not a valid exit. Use 'look around' to see available options.")
            return None

    while True:
        command = input("\n> ").strip().lower()

        if command == "look around":
            handle_look()
        elif command == "?":
            handle_help()
        elif command.startswith("go "):
            room = command[3:].strip()
            result = handle_go(room)
            if result:
                return result
        elif command == "leaderboard":
            from .leaderboard import show_top_players
            show_top_players()
        elif command == "wallet":
            from .utils import show_wallet
            show_wallet(state)
        elif command == "quit":
            print("👋 You leave the school and the adventure comes to an end. Game over.")
            sys.exit()
        else:
            print("❓ Unknown command. Type '?' to see available commands.")
