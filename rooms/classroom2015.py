# -----------------------------------------------------------------------------
# File: classroom2015.py
# ACS School Project - Simple Maze Example
# Organization: THUAS (The Hague University of Applied Sciences)
# Location: Delft
# Date: July 2025
# -----------------------------------------------------------------------------

import sys
import random
from .utils import chooseNextRoom


# spin_wheel() and room integration into the main were coded by Lazar Calin
# handle_look() and handle_go() were coded by Badrishvili Anastasia

def enterClassroom2015(state):
    print("\n🏫 You step into Classroom 2.015.")
    print("The classroom is filled with students.")
    print("The door creaks shut behind you. Everyone is looking at you; it's completely silent.")

    def print_key():
        key_print = r'''
                                         ###:::###         
                                     #:  ::===::  :#      
                                   #: :===========: :#    
                                  #.:===#       #===: #   
                                 #::===           #== :=  
                                 =====             #==    
                                 ==::#             #::==# 
                                 ===::             #::==  
                                  ==:::           #::==#  
                                   ==:::##     ##:::==#   
                                 ::::==:::::::::::===#    
                               : ::===============##      
                             # ::====     #####           
                           #   ====#                      
                         # ::===-#                        
                       #  :====#                          
                     #: :====#                            
                   #: :====#                              
                 ## ::===#                                
               ## ::===#                                  
              # ::====                                    
            # ::====++                                    
          # ::====+++++#                                  
        #:::====# ++++++*#                                
        ::====+#   #+++#                                  
    #: : ====+++##   #                                    
      #====+++++++#                                       
        #    ++++#                                        
              ##                                          '''
        print(key_print)

    spin_count = 0
        # --- Wheelspin helper ---

    def spin_wheel():
        nonlocal spin_count
        spin_count += 1
        print(f"\nWheel spin #{spin_count}...")
        if spin_count <= 3:
            reward = random.randint(20, 40)
            state["coins"] += reward
            print(f"You win {reward} coins! Total coins: {state['coins']}\n")
        elif spin_count == 4:
            if "key" not in state["inventory"]:
                print("Very well! You found the WHEELSPIN KEY!\n")
                print_key()
                state["inventory"].append("key")
            else:
                print("The wheel clicks... but you already have the wheelspin key.\n")
        else:
            print("The wheel doesn't seem to give any more rewards.\n")

    # --- Helperfuncties voor commandoverwerking ---

    def handle_look():
        """Classroom 2015 with spin-the-wheel challenge."""
        if 'key' not in state['inventory']:
            if 'Access Pass' in state['inventory']:
                print("\nThe air is thick with tension...\n")
                print("At the center stands a massive, glittering wheel.")
                print("Mr. Smith turns at you, adjusts his tie, grins mischievously, and declares:")
                print("\"Ah, forget boring lessons! Today, your destiny rests on...\"")
                print("SPIN THE WHEEL!!!!!!")
                print("\"Spin it, and fortune may allow you to unlock the next room...\"")
                print("\"Or perhaps the wheel will mock you, leaving you empty-handed!\"")

                choice = input('\nDo you dare to spin the wheel? (yes/no): ').strip().lower()

                if choice == "yes":
                    print("Mr. Smith rubs his hands together. \"Excellent!\"")
                    spin_wheel()  # call function
                    print("Hmm, no key yet..\n")
                    spin_choice = str(input("Enter 'spin' to spin again.\n"))
                    if spin_choice == "spin":
                        spin_wheel()
                    print("I think you should try again..\n")
                    spin_choice = str(input("Enter 'spin' to spin again.\n"))
                    if spin_choice == "spin":
                        spin_wheel()
                    print("You do not want to give up now.. do you?\n")
                    spin_choice = str(input("Enter 'spin' to spin again.\n"))
                    if spin_choice == "spin":
                        spin_wheel()
                    print(
                        "\n\"Very well.\" Mr. Smith bows with a flourish. \"The wheel has spoken! Now, onward with your adventure.\"\n")
                    state["visited"]["classroom2015"] = True
                else:
                    print("\nMr. Smith sighs and shakes his head.")
                    print("\"No spin, no glory!\"")
                    return
            else:
                print("Where is your access pass?\n "
                      "You need it to stay in this classroom..\n"
                      "Return to the front desk and find it!\n")

        else:
            print("\nYou already have the wheelspin key!\n.")
            print("You can spin another 10 times if you want to earn more coins!\n")
            spin_times = 0
            for spin_times in range(10):
                user_spin_again = input(("Enter 'spin' to spin again else enter 'stop'.\n"))
                if user_spin_again == "spin":
                    spin_wheel()
                    spin_times += 1
                else:
                    print("Alright, good luck!\n")
                    break

    def handle_help():
        print("\nAvailable commands:")
        print("- look around         : Examine the room and its contents.")
        if not state["visited"]["classroom2015"]:
            print("- spin wheel          : Spin the wheel once (4 spins needed for the wheelspin key).")
        if state["visited"]["classroom2015"] and "key" not in state["inventory"]:
            print("- take key            : Pick up the key once it's revealed.")
        print("- go corridor / back  : Leave the room and return to the corridor.")
        print("- ?                   : Show this help message.")
        print("- wallet              : Show how many coins you have.")
        print("- quit                : Quit the game entirely.")

    def handle_take(item):
        if item == "key":
            if "key" in state["inventory"]:
                print("🗝️ You already have the mysterious key you won from the Wheel of Mysteries.")
            else:
                print("❌ There's no key lying around here. Perhaps fortune from the wheel will grant it to you.")
        else:
            print(f"There is no '{item}' here to take.")

    def handle_go(destination):
        if destination in ["corridor", "back"]:
            print("🚪 You open the door and step back into the corridor.")
            return "corridor"
        elif destination.lower() == "lab2001":
            if "key" in state["inventory"]:
                return "lab2001"
            else:
                print(
                    "❌ The door to LAB2001 is locked tight. You’ll need a key — perhaps the Wheel of Mysteries can help.")
                return None
        else:
            print(f"❌ You can't go to '{destination}' from here.")
            return None

    def handle_answer(answer):
        # The old riddle is gone; this room now uses the Wheel of Mysteries
        print("❌ There are no riddles to answer in this room.")
        print("Mr. Smith chuckles: \"Your fate lies with the Wheel, not with silly answers.\"")
        return None

    # --- Commandoloop ---
    while True:
        command = input("\n> ").strip().lower()

        if command == "look around":
            handle_look()

        elif command == "?":
            handle_help()

        elif command == "spin wheel":
            spin_wheel()

        elif command.startswith("take "):
            item = command[5:].strip()
            handle_take(item)

        elif command.startswith("go "):
            destination = command[3:].strip()
            result = handle_go(destination)
            if result:
                return result

        elif command.startswith("answer "):
            answer = command[7:].strip()
            result = handle_answer(answer)
            if result:
                return result

        elif command == "wallet":
            from .utils import show_wallet

            show_wallet(state)

        elif command == "quit":
            print("👋 You drop your backpack, leave the maze behind, and step back into the real world.")
            sys.exit()

        else:
            print("❓ Unknown command. Type '?' to see available commands.")
