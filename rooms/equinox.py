# -----------------------------------------------------------------------------
# File: equinox.py
# ACS School Project - Simple Maze Example
# Organization: THUAS (The Hague University of Applied Sciences)
# Location: Delft
# Date: October 2025
# coded by Calin Lazar
# -----------------------------------------------------------------------------
import sys
import time

def enterEquinox(state):
    print("\n🌑 You have been sent to the Equinox Student Society Waiting Room.")
    state["equinox_attempts"] = state.get("equinox_attempts", 0) + 1

    if state["equinox_attempts"] == 1:
        wait_time = 10
        print("⏳ You must wait here for 1 minute as a warning.")
        print("💡 Supervisor: 'Stealing or cheating is not tolerated!'")
    elif state["equinox_attempts"] == 2:
        wait_time = 20
        print("⚠️ This is your final warning!")
        print("⏳ You must stay here for 5 minutes.")
    else:
        print("\n🚫 You've been caught again for the third time!")
        print("The supervisor shakes their head and escorts you to the Correction Room.")
        return "correctionroom"

    print("\n⏳ Waiting...")
    for remaining in range(wait_time, 0, -1):
        mins = remaining // 60
        secs = remaining % 60
        print(f"\rTime left: {mins:02d}:{secs:02d}", end="", flush=True)
        time.sleep(1)
    print("\rTime left: 00:00")
    print("\n🔔 Time's up! You can now return to the Front Desk or the Corridor.")

    state["visited"]["equinox"] = True

    def handle_help():
        print("\nAvailable commands:")
        print("- look around         : Examine the room.")
        print("- go frontdesk/back   : Return to the front desk.")
        print("- go corridor         : Return to the corridor.")
        print("- ?                   : Show this help message.")
        print("- wallet              : Show your coins.")
        print("- inventory           : Show your inventory.")
        print("- quit                : Quit the game.")

    def handle_look():
        print("👀 You look around the waiting room. It’s plain and quiet — just a few chairs and the ticking of a clock.")

    def handle_go(destination):
        dest = destination.strip().lower()
        if dest in ("frontdesk", "back"):
            return "frontdesk"
        elif dest == "corridor":
            return "corridor"
        else:
            print(f"❌ You can't go to '{dest}' from here.")
            return None

    def handle_take(item):
        print(f"There is no '{item}' here to take.")

    def handle_answer(answer):
        print("❌ There are no riddles to answer in this room.")
        return None

    while True:
        command = input("\n> ").strip().lower()
        if command == "look around":
            handle_look()
        elif command == "?":
            handle_help()
        elif command.startswith("take "):
            handle_take(command[5:].strip())
        elif command.startswith("go "):
            dest = handle_go(command[3:].strip())
            if dest:
                return dest
        elif command.startswith("answer "):
            handle_answer(command[7:].strip())
        elif command == "inventory":
            if state["inventory"]:
                print("🎒 Your inventory:", ", ".join(state["inventory"]))
            else:
                print("🎒 Your inventory is empty.")
        elif command == "wallet":
            from .utils import show_wallet
            show_wallet(state)
        elif command == "quit":
            print("👋 You leave the maze.")
            sys.exit()
        elif command == "":
            continue
        else:
            print("❓ Unknown command. Type '?' to see available commands.")
