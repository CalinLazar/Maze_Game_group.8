# -----------------------------------------------------------------------------
# File: correctionroom.py
# ACS School Project - Simple Maze Example
# Organization: THUAS (The Hague University of Applied Sciences)
# Location: Delft
# Date: October 2025
# coded by Calin Lazar
# -----------------------------------------------------------------------------
import random

def enterCorrectionRoom(state):
    """
    Correction Room:
    - Biology teacher asks 3 anatomy questions.
    - 3 correct → no penalty
    - 2 correct → -30 coins
    - 0 or 1 correct → 2 easy questions picked randomly from pool;
        - if both correct → no penalty
        - else → -20 coins
    Always returns to frontdesk.
    """

    print("\n🧠 You are escorted into the Correction Room.")
    print("The door shuts behind you. A strict biology teacher greets you.")
    print("\"You're here again? Let's see if you can handle some anatomy questions.\"")
    print("She crosses her arms: \"Three questions. Answer carefully.\"")

    questions = [
        {"q": "1️⃣ What is the largest organ in the human body?", "a": ["skin"]},
        {"q": "2️⃣ How many chambers does the human heart have?", "a": ["4", "four"]},
        {"q": "3️⃣ Which organ is responsible for filtering blood?", "a": ["kidney", "kidneys"]}
    ]

    correct_count = 0
    for item in questions:
        while True:
            answer = input(f"\n{item['q']}\n> ").strip().lower()
            if answer == "":
                print("Please type something.")
                continue
            break
        if answer in item["a"]:
            print("✅ Correct!")
            correct_count += 1
        else:
            print(f"❌ Wrong. The correct answer was: {item['a'][0].title()}")

    print(f"\n📊 You answered {correct_count} out of 3 questions correctly.")

    if correct_count == 3:
        print("\n👏 \"Excellent work. You may go.\"")

    elif correct_count == 2:
        penalty = 30
        print("\n😐 \"Close... but not perfect. There will be consequences.\"")
        state["coins"] = max(0, state["coins"] - penalty)
        print(f"You lose {penalty} coins. You now have {state['coins']} coins.")

    else:
        # Redemption: pick 2 easy questions randomly
        easy_pool = [
            {"q": "🦴 How many eyes do humans normally have?", "a": ["2", "two"]},
            {"q": "👃 What body part is used for smelling?", "a": ["nose"]},
            {"q": "🖐️ How many fingers does a typical human hand have?", "a": ["5", "five"]},
            {"q": "👂 Which body part is used for hearing?", "a": ["ear", "ears"]}
        ]
        easy_questions = random.sample(easy_pool, 2)

        print("\n🤨 \"That's not enough. Let's see if you can at least handle the basics.\"")

        easy_correct = 0
        for item in easy_questions:
            while True:
                answer = input(f"\n{item['q']}\n> ").strip().lower()
                if answer == "":
                    print("Please type something.")
                    continue
                break
            if answer in item["a"]:
                print("✅ Correct!")
                easy_correct += 1
            else:
                print(f"❌ Wrong. The correct answer was: {item['a'][0].title()}")

        if easy_correct == 2:
            print("\n👏 \"Good. At least you know the basics. You may leave.\"")
        else:
            penalty = 20
            print("\n😡 \"Even the easy ones? Disappointing.\"")
            state["coins"] = max(0, state["coins"] - penalty)
            print(f"You lose {penalty} coins. You now have {state['coins']} coins.")

    print("\n🚪 The teacher opens the door and escorts you out.")
    print("\"I'm taking you back where you belong...\" she says.")
    print("You are escorted directly back to the 🛎️ Front Desk.\n")

    state["visited"]["correctionroom"] = True
    return "frontdesk"
