# -----------------------------------------------------------------------------
# File: projectroom3.py
# ACS School Project - Simple Maze Example
# Organization: THUAS (The Hague University of Applied Sciences)
# Location: Delft
# Date: July 2025
# -----------------------------------------------------------------------------

import sys
from .utils import chooseNextRoom

def enterProjectRoom3(state):
    print("\n🏗️ You enter Project Room 3.")
    print("Several tables are pushed together, covered in papers, laptops, and half-eaten snacks.")

    def handle_look():
        if not state["visited"]["projectroom3"]:
            print("You see laptops, snacks, sticky notes, and the riddle on the whiteboard:\n"
                  "The riddle writes...:\n")
            attempts = 0
            max_attempts = 5
            while attempts < max_attempts:
                print("I have keys but open no locks,\n"
                      "I have space but have no room,\n"
                      "You can enter but can't go outside.\n")

                user_riddle_response = input("What am I?\n").strip().lower()

                if user_riddle_response in ["keyboard", "a keyboard"] \
                        and "calculator" not in state["inventory"]:
                    print("✅ Correct! The riddle answer is 'keyboard'. The room lights up as if acknowledging your success.\n")
                    print("🎁 Your prize is the best calculator on the market!!!\n")
                    state["inventory"].append("calculator")
                    state["visited"]["projectroom3"] = True
                    break
                else:
                    attempts += 1
                    if attempts < max_attempts:
                        print(f"❌ Wrong answer. You have {max_attempts - attempts} attempts left.\n")
                    else:
                        print("😢 You’ve used all your attempts. The riddle remains unsolved.\n")
                        state["visited"]["projectroom3"] = True
                        print("Maybe you can find the calculator in a new room..\n")
        else:
            print("Everyone has left. Only empty wrappers and a few notebooks remain.\n")
            print("Return to the corridor and continue your adventure..\n")
            print("- Your current inventory:", state["inventory"])


    def handle_help():
        """List available commands."""
        print("\nAvailable commands:")
        print("- look around         : Examine the room for clues.")
        print("- go corridor / back  : Leave the room and return to the corridor.")
        print("- ?                   : Show this help message.")
        print("- quit                : Quit the game completely.")

    def handle_go(destination):
        if destination in ["corridor", "back"]:
            print("You step away from the room and return to the corridor.\n")
            return "corridor"
        elif destination == "frontdesk":
            return "frontdesk"
        elif destination == "back" or destination == "projectroom1":
            return "projectroom1"
        else:
            print(f"❌ You can't go to '{destination}' from here. Try returning to the corridor first!\n")
            return None


    # --- Main command loop ---
    while True:
        command = input("\n> ").strip().lower()

        if command == "look around":
            handle_look()

        elif command == "?":
            handle_help()

        elif command.startswith("go "):
            destination = command[3:].strip()
            result = handle_go(destination)
            if result:
                return result

        elif command.startswith("answer "):
            print("You do not need to use the answer command to solve the riddle, you can just type th solution.\n")

        elif command == "quit":
            print("👋 You close your notebook and leave the project behind. Game over.")
            sys.exit()

        else:
            print("❓ Unknown command. Type '?' to see available commands.")
