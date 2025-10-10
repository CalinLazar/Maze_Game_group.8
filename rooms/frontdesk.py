# -----------------------------------------------------------------------------
# File: frontdesk.py
# ACS School Project - Simple Maze Example
# Organization: THUAS (The Hague University of Applied Sciences)
# Location: Delft
# Date: October 2025
# -----------------------------------------------------------------------------

import sys
import threading
import time

def enterFrontDesk(state):
    """
    Front Desk Room - Time-limited stealth mini-game.
    First failure → Equinox
    Second failure → Correction Room
    """

    print("\n🛎️ You quietly approach the school's Front Desk.")
    print("The receptionist is away, but could return at any moment...")
    print("Your goal: steal the calculator before time runs out.")
    print("You can 'search <place>' to look around.")

    state.setdefault("frontdesk_failures", 0)

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
    time_limit = 60 if state["frontdesk_failures"] == 0 else 90
    t = threading.Thread(target=countdown, args=(time_limit,), daemon=True)
    t.start()

    searchable_places = {
        "under chair": "You crouch down and peek under the chair… just dust and gum.",
        "drawer": "You quietly slide open the drawer…",  # ✅ added for consistency
        "shelf": "You shuffle through the supply shelf… only paper stacks and staplers.",
        "desk": "You search around the messy desk.\nYou flip over folders but find nothing.",
        "folders": "You go through the folders. Nothing useful.",
        "behind picture": "You check behind the big picture and find 5 coins!"
    }

    searched_places = set()
    calculator_found = False

    def handle_look():
        print("\nYou scan the reception area.")
        print("Places to search:", ", ".join(searchable_places.keys()))
        print("- Possible exits: corridor")
        print("- Your inventory:", state["inventory"])

    def handle_search(place):
        nonlocal calculator_found
        # ✅ if timer expired, trigger failure right away
        if timer_expired["done"]:
            return handle_failure()
        place = place.lower()
        if place in searched_places:
            print(f"You already searched the {place}.")
            return
        searched_places.add(place)

        if place == "drawer":
            print(searchable_places[place])
            print("Among pens and sticky notes, you spot a shiny calculator!")
            calculator_found = True
        elif place == "behind picture":
            print(searchable_places[place])
            state["coins"] += 5
        elif place in searchable_places:
            print(searchable_places[place])
        else:
            print("❌ Invalid search spot.")

    def handle_take(item):
        nonlocal calculator_found
        if timer_expired["done"]:
            return handle_failure()
        if item == "calculator":
            if calculator_found:
                if "calculator" not in state["inventory"]:
                    print("You snatch the calculator and slip it into your backpack.")
                    state["inventory"].append("calculator")
                    state["visited"]["frontdesk"] = True
                    timer_active["running"] = False
                    return "corridor"  # ✅ auto-leave after theft
                else:
                    print("You already took the calculator.")
            else:
                print("You haven't found the calculator yet.")
        else:
            print(f"There is no '{item}' here to take.")

    def handle_go(destination):
        timer_active["running"] = False
        dest = destination.lower()
        if dest == "corridor":
            print("You quickly leave the front desk and step back into the corridor.")
            return "corridor"
        elif dest in ("projectroom3", "back"):
            return "projectroom3"
        elif dest == "projectroom1":
            return "projectroom1"
        else:
            print(f"You can't go to '{destination}' from here.")
            return None

    def handle_failure():
        """centralized failure logic if timer expires mid-action"""
        timer_active["running"] = False
        state["frontdesk_failures"] += 1
        if state["frontdesk_failures"] == 1:
            print("\nToo late! The receptionist walks back in and catches you red-handed.")
            print("You’re escorted to the Equinox Room and fined 10 coins.")
            state["coins"] = max(0, state["coins"] - 10)
            state["visited"]["frontdesk"] = False
            return "equinox"
        else:
            print("\nThe receptionist shakes their head in disappointment...")
            print("🚪 You’re being escorted to the Correction Room for a mandatory session.")
            state["visited"]["frontdesk"] = False
            return "correctionroom"

    # --- Main loop ---
    while True:
        if timer_expired["done"]:
            return handle_failure()

        command = input("\n> ").strip().lower()
        if not command:
            continue
        elif command == "look around":
            handle_look()
        elif command.startswith("search "):
            result = handle_search(command[7:].strip())
            if result:
                return result
        elif command.startswith("take "):
            result = handle_take(command[5:].strip())
            if result:
                return result
        elif command.startswith("go "):
            destination = command[3:].strip()
            result = handle_go(destination)
            if result:
                return result
        elif command == "quit":
            print("👋 You abandon your mission and walk out of the school.")
            timer_active["running"] = False
            sys.exit()
        else:
            print("❓ Unknown command. Type '?' to see available commands.")
