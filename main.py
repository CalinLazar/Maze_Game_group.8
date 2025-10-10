# -----------------------------------------------------------------------------
# File: main.py
# ACS School Project - Simple Maze Example
# Organization: THUAS (The Hague University of Applied Sciences)
# Location: Delft
# Date: July 2025
# -----------------------------------------------------------------------------

from rooms import (enterCorridor, enterTeachersRoom1, enterClassroom2015, enterProjectRoom3,
                   enterLab2001, enterProjectRoom1, enterFrontDesk, enterEquinox, enterCorrectionRoom)


def print_ascii_banner():
    banner = r"""
 ________                 _____ ______   ________  ________  _______                  ___  ________   ________                 ________  _______   ___       ________ _________   
|\   __  \               |\   _ \  _   \|\   __  \|\_____  \|\  ___ \                |\  \|\   ___  \|\   ____\               |\   ___ \|\  ___ \ |\  \     |\  _____\\___   ___\ 
\ \  \|\  \  ____________\ \  \\\__\ \  \ \  \|\  \\|___/  /\ \   __/|   ____________\ \  \ \  \\ \  \ \  \___|   ____________\ \  \_|\ \ \   __/|\ \  \    \ \  \__/\|___ \  \_| 
 \ \   __  \|\____________\ \  \\|__| \  \ \   __  \   /  / /\ \  \_|/__|\____________\ \  \ \  \\ \  \ \  \  ___|\____________\ \  \ \\ \ \  \_|/_\ \  \    \ \   __\    \ \  \  
  \ \  \ \  \|____________|\ \  \    \ \  \ \  \ \  \ /  /_/__\ \  \_|\ \|____________|\ \  \ \  \\ \  \ \  \|\  \|____________|\ \  \_\\ \ \  \_|\ \ \  \____\ \  \_|     \ \  \ 
   \ \__\ \__\              \ \__\    \ \__\ \__\ \__\\________\ \_______\              \ \__\ \__\\ \__\ \_______\              \ \_______\ \_______\ \_______\ \__\       \ \__\
    \|__|\|__|               \|__|     \|__|\|__|\|__|\|_______|\|_______|               \|__|\|__| \|__|\|_______|               \|_______|\|_______|\|_______|\|__|        \|__|
"""
    print(banner)


print_ascii_banner()

print("****************************************************************************")
print("*                      Welcome to the School Maze!                         *")
print("*        Your goal is to explore all important rooms in the school.        *")
print("*    You may need to solve challenges to collect items and unlock rooms.   *")
print("*               Once you've visited all rooms, you win!                    *")
print("****************************************************************************")

state = {
    "current_room": "corridor",
    "previous_room": "corridor",
    "visited": {
        "classroom2015": False,
        "teachersroom1": False,
        "lab2001": False,
        "projectroom1": False,
        "projectroom3": False,
        "frontdesk": False,
        "equinox": False,
        "correctionroom": False
    },

    "inventory": [],
    "coins": 50,
    "frontdesk_failures": 0,
}

# Changed "studylandscape" to "teachersroom1" and "enterStudylandscape" to "enterTeachersRoom1"
while True:
    current = state["current_room"]

    if current == "corridor":
        state["current_room"] = enterCorridor(state)

    elif current == "teachersroom1":
        state["current_room"] = enterTeachersRoom1(state)

    elif current == "classroom2015":
        state["current_room"] = enterClassroom2015(state)

    elif current == "projectroom3":
        state["current_room"] = enterProjectRoom3(state)

    elif current == "lab2001":
        state["current_room"] = enterLab2001(state)

    elif current == "projectroom1":
        state["current_room"] = enterProjectRoom1(state)

    elif current == "frontdesk":
        state["current_room"] = enterFrontDesk(state)

    elif current == "equinox":
        state["current_room"] = enterEquinox(state)

    elif current == "correctionroom":
        state["current_room"] = enterCorrectionRoom(state)


    else:
        print("Unknown room. Exiting game.")
        break
