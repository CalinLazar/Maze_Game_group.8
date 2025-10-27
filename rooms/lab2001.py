# -----------------------------------------------------------------------------
# File: lab2001.py
# ACS School Project - Simple Maze Example
# Organization: THUAS (The Hague University of Applied Sciences)
# Location: Delft
# Date: July 2025
# -----------------------------------------------------------------------------
import sys
from .utils import chooseNextRoom
import threading
import time

# Room lab2.001 done by Vladimir


def enterLab2001(state):
   # --- Check if the player has the key to enter ---

   timer_expired = {"done": False}
   timer_active = {"running": True}

   def countdown(limit=60):
       reminders = {30: "Only 30 seconds remain!", 10: "10 seconds left!", 5: "Just 5 seconds! Hurry!"}
       total = limit
       while total > 0:
           time.sleep(1)
           if not timer_active["running"]:
               return
           total -= 1
           if total in reminders:
               print(f"\n{reminders[total]}")
       if timer_active["running"]:
           timer_expired["done"] = True

   # 60s first time, 90s after
   time_limit = 60 if not state["visited"]["lab2001"] else 9999
   t = threading.Thread(target=countdown, args=(time_limit,), daemon=True)
   t.start()

   if not state["visited"]["lab2001"]:
       if "key" not in state["inventory"]:
           print("\n You do have access to Lab2.001 try going somewhere else first")
           return "corridor"

       else:
           print("\n You insert the key into the lock and turn it with a satisfying click.")
           print("The door creaks open to reveal a bright and lively workspace.")
           print("\nYou enter Lab2.001.")
           print("Room is mostly empty now with chairs everywhere and some remains of notes people were making.")
           print("Maybe you could look around to find a useful note.")
           print("But be fast you can hear that some students are about to come in")

   else:
       print("You enter the lab2.001 again.")
       print("While you open the door you see that its no longer empty.")
       print("Some of the students look at you while other continue their work.")
       print("It will be hard for you to search for anything with all the people around.")
       print("Someone approaches you asking what do you want, \nbut before you could explained he cuts you off asking you to get out")
       print("- You might be able to get them to let you in if you give them a couple of coins")
       print("Do you want to try giving him 50 coins? \n -Yes \n -No(You will exit the room)")
       respose = input(">").strip().lower()
       if(respose == "yes"):
           if(state["coins"] > 50):
               state["coins"] -= 50
               print("He looks around before taking the coins")
               print("\"Be quick\" They turn around leaving you be")
               print("You are now in the lab2.001 there are a lot of students around working, but they dont seem to mind you")
               print("You can search the room again")


           else:
               print("You take out of your pocket what coins you have")
               print("You both look down at your pawn only for him to laugh")
               print("Embarrassed you quickly exit the room")
               print("- Try earning more coins before coming back")
               return "corridor"
       elif (respose == "no"):
           print("You decide it's not wort it and exit the room")
           return "corridor"
       else:
           print("You look stunted before turning around and leaving")
           return "corridor"

   # --- Room entry description ---

   state["visited"]["lab2001"] = True

   # --- Command handlers ---


   def handle_look():
       """Describe the room and give clues."""
       print("\nYou scan the room.")
       print("The walls are covered in sticky notes, whiteboards are full of pseudocode and diagrams.")
       print("It seems to be a mess of notes everywhere, it will be hard to find the right one")
       print("You see different locations full of notes that could potentially be it")
       print("There notes under the desk in the corner, some are stuck to the ceiling somehow, other sticking out of notebooks")
       print("- Possible locations to search: under desk, ceiling, red notebook, blue notebook, green notebook, whiteboard "
             "\n floor, central table, column"
             "enter 'search' and the location.\n")
       print("- Possible exits: corridor")
       print("- Your current inventory:", state["inventory"])
       state["visited"]["lab2001"] = True


   def handle_help():
       """List available commands."""
       print("\nAvailable commands:")
       print("- look around         : Examine the room for clues.")
       print("- search \"location \"  : To search for notes" )
       print("- go corridor / back  : Leave the room and return to the corridor.")
       print("- ?                   : Show this help message.")
       print("- quit                : Quit the game completely.")


   def handle_go(destination):
       """Handle movement out of the room."""
       if destination in ["corridor", "back"]:
           print("You step away from the room and return to the corridor.")
           return "corridor"
       elif destination == "back":
           return "classroom2015"
       elif destination == "projectroom1":
           return "projectroom1"
       else:
           print(f"❌ You can't go to '{destination}' from here.")
           return None

   def handle_answer(answer):
       normalized = answer.strip().lower()
       if normalized == "central table":
           state["inventory"].append("Note")
           return True
       else:
           print("You can't find it here, quickly try looking somewhere else.")
           return False

   def handle_failure():
        timer_active["running"] = False
        print("Oh no you were too slow")
        print("Students start coming in quickly filling up the room making it hard to search")
        print("As more people enter you quietly exit the room")
        return "corridor"

   # --- Main command loop ---
   while True:
       command = input("\n> ").strip().lower()

       if timer_expired["done"]:
           return handle_failure()

       if command == "look around":
           handle_look()


       elif command == "?":
           handle_help()


       elif command.startswith("go "):
           destination = command[3:].strip()
           result = handle_go(destination)
           if result:
               return result


       elif command.startswith("search "):
           guess = command[6:].strip()
           result = handle_answer(guess)
           if result:
               print("Good job you found it.")
               print("It reads \"Super secret technique \" surely some body will know what that means")
               print("- Note is been added to your inventory")
               print("You exit the room not wanting to cause disturbance")
               return "corridor"


       elif command == "quit":
           print("👋 You close your notebook and leave the project behind. Game over.")
           sys.exit()


       else:
           print("❓ Unknown command. Type '?' to see available commands.")
