# -----------------------------------------------------------------------------
# File: projectroom1.py
# ACS School Project - Simple Maze Example
# Organization: THUAS (The Hague University of Applied Sciences)
# Location: Delft
# Date: July 2025
# -----------------------------------------------------------------------------

import sys
from .utils import chooseNextRoom
def enterProjectRoom1(state):
    print("\nYou walk into Project Room 1...")


    def handle_look():
        print("You scan the room...\n")
        print("The walls are covered in sticky notes, whiteboards are full of pseudocode and diagrams.")
        if not state["visited"]["projectroom3"]:
            print("Two of your classmates are sitting at a desk, frowning at their notes.")
            print("They are struggling to solve a problem and can’t continue their project.")
            if 'Note' in state["inventory"]:
                print("You remember—you have the solution in the note you put on your inventory.")
                user_note_choice = str(input("Would you like to hand the note to your classmates?(yes/no)\n"))
                if user_note_choice.strip().lower() == 'yes':
                    print("You are a good classmate!!!\n")
                    del state['inventory'][2]
                    print("They thank you for sharing it and say:")
                    print("\"If only we had a calculator, we could finish the problem much faster!\"")
                    print("They tell you that if you can find a calculator and bring it to them,"
                          "you’ll be rewarded with many coins.. and of course a very valuable badge..\n"
                          "The badge will be proven very.. very useful to your last challenge.\n")
                    print("You hear that to find it.. you need to first go through Project Room 3.\n")
                    state["visited"]["projectroom1"] = True
                    print("Enter 'go projectroom3' and find out.\n")
                else:
                    print("I think you should reconsider saying yes to that..\n")
                    return
            elif 'Note' not in state["inventory"]:
                print("You can help them..\n"
                      "There is a note hidden in Lab2001.\n"
                      "Find your way to the lab and return with the note...\n")

        elif state['visited']['projectroom3'] and "calculator" in state["inventory"]:
            print("Your classmates turn to you..")
            user_calc_response = str(input("'Do you have the calculator????' (yes/no)\n"))
            if user_calc_response.strip().lower() == 'yes':
                user_calc_give = str(input("Your classmates faces light up with joy!\n"
                                            "Would you like to hand it over to them? (yes/no)\n"))
                if user_calc_give.strip().lower() == 'yes':
                    print("\nYou hand the calculator to your classmates...")
                    print("\"Thank you so much! You’re a real lifesaver.\"")
                    print("You gain the *Good Classmate* Badge!")
                    if "Good Classmate Badge" not in state["inventory"]:
                        state["inventory"].append("Good Classmate Badge")
                        print("\n*** Badge added to inventory ***")
                        print("Time for your final challenge...")
                        print("Head back to the corridor and find the exit to the maze!")
                        state["visited"]["teachersroom1"] = True
                        state["visited"]["classroom2015"] = True
                        state["visited"]["lab2001"] = True
                        state["visited"]["projectroom1"] = True
                        state["visited"]["projectroom3"] = True
                        state["visited"]["frontdesk"] = True
                    else:
                        print("Oh.. the badge is already in your inventory...\n")
                else:
                    print("Well that is too bad.. you have to give it in order to get out of here.\n")
                    return
            else:
                print("Then you need to find it!\n"
                      "Visit project room 3 to look for the calculator!\n")

        elif state['visited']['projectroom3'] and "calculator" not in state["inventory"]:
                print("Oh.. looks like you did not find the calculator yet..!\n"
                      "How do you expect to find the exit of the maze?\n"
                      "Try to find it again.\n")

        elif "Good Classmate Badge" in state["inventory"]:
            print("\nYou have already gained the Good Classmate Badge!!!\n"
                  "Your classmates already solved the problem and went home..\n")

    def handle_help():
        """List available commands."""
        print("\nAvailable commands:")
        print("- look around         : Examine the room for clues.")
        print("- go corridor         : Return to the corridor.")
        print("- ?                   : Show this help message.")
        print("- quit                : Quit the game completely.")

    def handle_go(destination):
        """Handle movement out of the room."""
        if destination in ["corridor", "back"]:
            print("You step away from the project room and return to the corridor.")
            return "corridor"
        elif destination == "projectroom3":
                return "projectroom3"
        elif destination == "lab2001":
            return "lab2001"
        else:
            print(f"❌ You can't go to '{destination}' from here.")
            return None

    def handle_answer(answer):
        if "Good Classmate Badge" not in state["inventory"]:
            print("There are no riddles in this room, you do not have to use the answer command!!!\n")
        elif "Good Classmate Badge" in state["inventory"]:
            print("✅ You've already completed this room.")
            return None

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
            guess = command[7:].strip()
            result = handle_answer(guess)
            if result:
                return result

        elif command == "quit":
            print("👋 You close your notebook and leave the project behind. Game over.")
            sys.exit()

        else:
            print("❓ Unknown command. Type '?' to see available commands.")