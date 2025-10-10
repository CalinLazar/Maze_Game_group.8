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

def enterCorridor(state):
    print("\n🚶 You are standing in the school's main corridor.")
    print("You see a long corridor with many doors and glass walls on both side. Behind these door are rooms, waiting to be explored.")

    # --- List of accessible rooms from here ---
    available_rooms = ["teachersroom1", "lab2001"]

    # --- Command handlers ---
    if state["visited"]["teachersroom1"] == True:
        available_rooms.append("classroom2015")

    if state["visited"]["lab2001"] == True:
        available_rooms.append("projectroom1")

    if state["visited"]["projectroom1"] == True:
        available_rooms.append("projectroom3")

    if state["visited"]["projectroom3"] == True:
        available_rooms.append("frontdesk")


    def handle_look():
        """Describe the corridor and show where the player can go."""
        print("\nYou take a look around.")
        print("Students and teachers are walking in both directions along the corridor. You see several labeled doors.")
        print(f"- Possible doors: {', '.join(available_rooms)}")
        print("- You current inventory:", state["inventory"])

        escape_trial = 0
        bribe_cost = 200
        if escape_trial == 0:

            if (
                    state["visited"]["teachersroom1"] == True
                    and state["visited"]["classroom2015"] == True
                    and state["visited"]["lab2001"] == True
                    and state["visited"]["projectroom1"] == True
                    and state["visited"]["projectroom3"] == True
                    and "Good Classmate Badge" in state['inventory']
            ):
                user_last_call = str(input("Are you ready for your final challenge? (yes/no)\n"))
                if user_last_call == 'yes':
                    print("You need to choose one of the rooms you have visited to hide from the principal!\n"
                          "Lets hope you are lucky...\n")
                    print("The available rooms are: ", list(state['visited']))
                    user_room_choice = input(("Enter the name of the room you choose to hide in: \n"))
                    outcome = random.random()

                    if outcome < 0.7:  # 70% randomised chance to win
                        print("\nYou hid successfully! The principal couldn’t find you.")
                        print("✨ Congratulations, you have ESCAPED the maze! ✨")
                        sys.exit()
                    else:
                        print("\nSuddenly the principal’s voice echoes: ")
                        print("\"I FOUND YOU!!!!!!\"")
                        print(f"The principal demands {bribe_cost} coins to let you go...")
                        print(r"""

                              ________________
                              \      __      /         __
                               \_____()_____/         /  )
                               '============`        /  /
                                #---\  /---#        /  /
                               (# @\| |/@  #)      /  /
                                \   (_)   /       /  /
                                |\ '---` /|      /  /
                        _______/ \\_____// \____/ o_|
                       /       \  /     \  /   / o_|
                      / |           o|        / o_| \
                     /  |  _____     |       / /   \ \
                    /   |  |===|    o|      / /\    \ \
                   |    |   \@/      |     / /  \    \ \
                   |    |___________o|__/----)   \    \/
                   |    '              ||  --)    \     |
                   |___________________||  --)     \    /
                        |           o|   ''''   |   \__/
                        |            |          |




                            """)

                        if state["coins"] >= bribe_cost:
                            state["coins"] -= bribe_cost
                            print("You have {state['coins']} coins left.\n")
                            user_bribe_choice = input("Enter 'give' to give the coins to the principal:\n")
                            if user_bribe_choice.strip().lower() == 'give':
                                print(f"You hand over {bribe_cost} coins. The principal grumbles but lets you go.")
                                print("!!!!!Congratulations, you have ESCAPED the maze!!!!!")
                                sys.exit()
                            else:
                                print("I am going to ask one more time...\n")
                                user_bribe_choice = input("Enter 'give' to give the coins to the principal:\n")
                                if user_bribe_choice.strip().lower() == 'give':
                                    print(f"You hand over {bribe_cost} coins. The principal grumbles but lets you go.\n")
                                    print("!!!!!Congratulations, you have ESCAPED the maze!!!!!")
                                    sys.exit()
                                else:
                                    print("You are stuck here for eternity...\n")
                        else:
                            print("You don’t have enough coins...")
                            print(
                                "👉 You must revisit coin-generating rooms (e.g., Teachers Room 1 or Classroom 2.015),")
                            print("earn more coins, and then return to the lobby to pay off the principal.")
                            escape_trial = escape_trial + 1
        elif escape_trial == 2:
            print("Well, well..."
                  "I hope you now have enough coins to escape...\n")
            pay_choice = str(input(f"Enter 'pay' to pay the fine of {bribe_cost} coins!\n"))
            if pay_choice.strip().lower() == 'pay' and state["coins"] >= bribe_cost:
                state["coins"] -= bribe_cost
                print(f"You hand over {bribe_cost} coins. The principal grumbles but lets you go.")
                print("!!!!!Congratulations, you have ESCAPED the maze!!!!!")
                sys.exit()
            else:
                print("Once again you don’t have enough coins...\n")
                print("You must revisit coin-generating rooms (e.g., Teachers Room 1 or Classroom 2.015)\n")
                print("This is your last chance to earn more coins, and then return to the"
                      "lobby to pay off the principal.\n")
                escape_trial = escape_trial + 1

        else:
            print("Remember... this is your last attempt to freedom..\n")
            pay_choice2 = str(input(f"Enter 'pay' to pay the fine of {bribe_cost} coins!\n"))
            if pay_choice2.strip().lower() == 'pay' and state["coins"] >= bribe_cost:
                state["coins"] -= bribe_cost
                print(f"You hand over {bribe_cost} coins. The principal grumbles but lets you go.")
                print("!!!!!Congratulations, you have ESCAPED the maze!!!!!")
                sys.exit()
            else:
                print("You were warned... your coins are not enough AGAIN!!!!"
                      "The principal stares at you angrily...\n"
                      "'MWAHAHAHA. It looks like I won... once again..'\n"
                      "You are stuck here forever now..\n")
                print(r"""
                    ┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
                    ███▀▀▀██┼███▀▀▀███┼███▀█▄█▀███┼██▀▀▀
                    ██┼┼┼┼██┼██┼┼┼┼┼██┼██┼┼┼█┼┼┼██┼██┼┼┼
                    ██┼┼┼▄▄▄┼██▄▄▄▄▄██┼██┼┼┼▀┼┼┼██┼██▀▀▀
                    ██┼┼┼┼██┼██┼┼┼┼┼██┼██┼┼┼┼┼┼┼██┼██┼┼┼
                    ███▄▄▄██┼██┼┼┼┼┼██┼██┼┼┼┼┼┼┼██┼██▄▄▄
                    ┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
                    ███▀▀▀███┼▀███┼┼██▀┼██▀▀▀┼██▀▀▀▀██▄┼
                    ██┼┼┼┼┼██┼┼┼██┼┼██┼┼██┼┼┼┼██┼┼┼┼┼██┼
                    ██┼┼┼┼┼██┼┼┼██┼┼██┼┼██▀▀▀┼██▄▄▄▄▄▀▀┼
                    ██┼┼┼┼┼██┼┼┼██┼┼█▀┼┼██┼┼┼┼██┼┼┼┼┼██┼
                    ███▄▄▄███┼┼┼─▀█▀┼┼─┼██▄▄▄┼██┼┼┼┼┼██▄
                    ┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
                    ┼┼┼┼┼┼┼┼██┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼██┼┼┼┼┼┼┼┼┼
                    ┼┼┼┼┼┼████▄┼┼┼▄▄▄▄▄▄▄┼┼┼▄████┼┼┼┼┼┼┼
                    ┼┼┼┼┼┼┼┼┼▀▀█▄█████████▄█▀▀┼┼┼┼┼┼┼┼┼┼
                    ┼┼┼┼┼┼┼┼┼┼┼█████████████┼┼┼┼┼┼┼┼┼┼┼┼
                    ┼┼┼┼┼┼┼┼┼┼┼██▀▀▀███▀▀▀██┼┼┼┼┼┼┼┼┼┼┼┼
                    ┼┼┼┼┼┼┼┼┼┼┼██┼┼┼███┼┼┼██┼┼┼┼┼┼┼┼┼┼┼┼
                    ┼┼┼┼┼┼┼┼┼┼┼█████▀▄▀█████┼┼┼┼┼┼┼┼┼┼┼┼
                    ┼┼┼┼┼┼┼┼┼┼┼┼███████████┼┼┼┼┼┼┼┼┼┼┼┼┼
                    ┼┼┼┼┼┼┼┼▄▄▄██┼┼█▀█▀█┼┼██▄▄▄┼┼┼┼┼┼┼┼┼
                    ┼┼┼┼┼┼┼┼▀▀██┼┼┼┼┼┼┼┼┼┼┼██▀▀┼┼┼┼┼┼┼┼┼
                    ┼┼┼┼┼┼┼┼┼┼▀▀┼┼┼┼┼┼┼┼┼┼┼▀▀┼┼┼┼┼┼┼┼┼┼┼
                    ┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼
                    """)
                sys.exit()

    def handle_help():
        """List available commands and explain navigation."""
        print("\nAvailable commands:")
        print("- look around         : See what's in the corridor and where you can go.")
        print("- go <room name>      : Move to another room. Example: go classroom2015")
        print("- ?                   : Show this help message.")
        print("- wallet              : Show how many coins you have.")
        print("- quit                : Quit the game.")

    def handle_go(room_name):
        """Move to a listed room."""
        room = room_name.lower()
        if room in available_rooms:
            print(f"You walk toward the door to {room}.")
            state["previous_room"] = "corridor"
            return room
        else:
            print(f"❌ '{room_name}' is not a valid exit. Use 'look around' to see available options.")
            return None

    # --- Main corridor command loop ---
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

        elif command == "wallet":
            from .utils import show_wallet
            show_wallet(state)

        elif command == "quit":
            print("👋 You leave the school and the adventure comes to an end. Game over.")
            sys.exit()

        else:
            print("❓ Unknown command. Type '?' to see available commands.")
