# -----------------------------------------------------------------------------
# File: teachersroom1.py
# ACS School Project - Simple Maze Example
# Organization: THUAS (The Hague University of Applied Sciences)
# Location: Delft
# Date: October 2025
# coded by Badrishvili Anastasia
# -----------------------------------------------------------------------------
import sys
from .utils import chooseNextRoom  # (kept import in case other code relies on it)

def enterTeachersRoom1(state):
    print("\nYou go inside the teachers room.")

    quiz_state = {
        "active": False,        # is a quiz currently running?
        "mode": None,           # "first" (2 qs, 2 attempts each) or "training" (endless math quiz)
        "qnum": 0,              # current question num
        "correct": 0,           # number correct in first-time gate
        "attempts_left": 0,     # attempts left for the current question (only in firsttime mode)
        "true_val": None,       # current question's correct answer
    }


    def gen_question():
# function that generated random math questions, only addition and subtraction
        import random, operator
        ops = {'+': operator.add, '-': operator.sub}
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        op = random.choice(list(ops))
        val = ops[op](a, b)
        return a, op, b, val
# val is the actual correct answer, the function returns (42, '+', 7, 49)

    def pose_question():
    # generates vew questions
        a, op, b, val = gen_question()
        quiz_state["true_val"] = val
        quiz_state["attempts_left"] = 2 if quiz_state["mode"] == "first" else 1
        if quiz_state["mode"] == "first":
            shown_qnum = quiz_state["qnum"] + 1
            print(f"\nQ{shown_qnum} — 🔢 What is {a} {op} {b}? (you have 2 attempts)")
        else:
            print(f"\n🔢 What is {a} {op} {b}? (type 'answer <number>' or 'stop')")
        print("→ Use: answer <number>   e.g.,  answer 10")

    def start_quiz(mode):
    # marks quiz session as active
        """Initialize quiz mode and ask the first question."""
        quiz_state["active"] = True
        quiz_state["mode"] = mode # records the quiz (either 'first' or 'training')
        quiz_state["qnum"] = 0 # resets counter
        quiz_state["correct"] = 0 # resets counter
        pose_question() # calls function to ask question

    def finish_first_time_quiz():
    # Evaluate result of the 2-question gate and wrap up (room visited, AP appended to inventory, player name, end)
        if quiz_state["correct"] == 2:
            print("\n🏆 \"Incredible! You’ve passed my test! You gain an access pass to Classroom 2.015.\"")
            state["visited"]["teachersroom1"] = True
            if "Access Pass" not in state["inventory"]:
                state["inventory"].append("Access Pass")
            player_name = input("Mr. Smith squints at you. \"And what should I call the great champion?\" \n> ")
            print(f"\"{player_name.title()}... I shall remember that name. Proceed to Classroom 2.015. I will meet you there.\"")
            # Mark as passed so future entries are always training mode
            quiz_state["active"] = False
            print("\nMr. Smith waves you toward the door. \"You've done well enough. Off you go... for now.\"")
        else:
            print("\nMr. Smith sighs dramatically and shakes his head.")
            print("\"Game over. Back to preschool math for you! I suggest the book: "
                  "‘Kindergarten Math Activity Workbook:\n"
                  "Basic Mathematics Learning Book for Preschool and 1st Grade Children\"\n")
            sys.exit()


    def handle_look():
    # room dialogue depending on the visited state
        print("\nYou step into the teachers' room. The smell of old coffee and chalk dust hangs in the air.")

        if not state["visited"]["teachersroom1"]:
            print("Suddenly, Mr. Smith swivels around in his chair, adjusting his glasses dramatically.")
            print("\"Ah... a brave student enters my domain!\" he says with a sly grin.")
            print("\"Welcome to the maze. If you wish to continue, you must first prove your worth in...\"")
            print("✨ THE GREAT MATH QUIZ OF DOOM ✨\n")
            print("\"Two questions stand between you and freedom. Fail, and... forget about finding your way out..\"")
            print("Type 'start' to begin. Each question allows two attempts. Earn 5 coins per correct answer.")
            print("Answer format:  answer <number>\n")
        if state["visited"]["teachersroom1"]:
            print("\"Welcome back! Training never ends — answer as many questions as you like.\"")
            print("Each correct answer earns 10 coins. Type 'start' to begin, and 'stop' anytime.")
            print("Answer format:  answer <number>\n")

    def handle_help():
        print("\nAvailable commands:")
        print("- look around         : See the room intro and instructions.")
        print("- start               : Begin the quiz (first-time gate or training).")
        print("- answer <number>     : Answer the current math question.")
        print("- stop                : End the training quiz (re-entry only).")
        print("- go corridor / back  : Return to the main corridor.")
        print("- go classroom2015    : Try to enter Classroom 2.015 (requires Access Pass).")
        print("- wallet              : Check your coins.")
        print("- ?                   : Show this help message.")
        print("- quit                : Quit the game.")

    def handle_start():
    # prevents starting if quiz active, sets mode depending on visited
        if quiz_state["active"]:
            print("A question is already in progress. Use 'answer <number>' or 'stop'.")
            return
        if not state["visited"]["teachersroom1"]:
            print("\n******* Welcome, Challenger! *******\n")
            print("Mr. Smith slams a dusty book shut and points at you dramatically.")
            print("\"Answer wisely! Two correct answers and you may pass. Fail, and your adventure ends here...\"")
            start_quiz(mode="first")
        else:
            print("\nTraining mode engaged. Each correct answer earns you 10 coins.")
            print("Type 'stop' anytime to end training.")
            state["visited"]["teachersroom1"] = True
            start_quiz(mode="training")

    def handle_answer(arg):
        if not quiz_state["active"]:
            print("There is no active question. Type 'start' to begin the quiz.")
            return
        raw = arg.strip()
        try:
            guess = int(raw)
        except ValueError:
            print("❌ That's not a number. Use: answer <number>")
            return

        correct_val = quiz_state["true_val"]
        mode = quiz_state["mode"]

        if guess == correct_val:
            if mode == "first":
                print("\"Correct!\" You earn 5 shiny coins!\n")
                state["coins"] += 5
                quiz_state["correct"] += 1
                quiz_state["qnum"] += 1
                if quiz_state["qnum"] >= 2:
                    finish_first_time_quiz()
                else:
                    pose_question()
            else:
                print("🎉 \"Correct!\" You earn 10 coins!")
                state["coins"] += 10
                # Immediately pose next question
                pose_question()
        else:
            if mode == "first":
                quiz_state["attempts_left"] -= 1
                if quiz_state["attempts_left"] > 0:
                    print("❌ \"Wrong! Try once more...\"  (use: answer <number>)")
                else:
                    print("❌ \"Wrong! Even my cat could do better...\"")
                    print("the cat:", r""" 
                                        ▄   ▄
                                        █▀█▀█  ??
                                        █▄█▄█
                                         ███  ▄▄
                                         ████▐█ █
                                         ████   █
                                         ▀▀▀▀▀▀▀
                                          """)
                    print("Game over. I suggest the book ‘Kindergarten Math Activity Workbook:\n"
                          "Basic Mathematics Learning Book for Preschool and 1st Grade Children'.\n"
                          "You can come back after and try again.\n")
                    sys.exit()
            else:
                # training: one attempt per question, then move on to next question
                print("❌ \"Wrong! Keep practicing.\"")
                pose_question()

    def handle_stop():
    # this is for user to have the option to stop anytime when quiz is in training mode
        if quiz_state["active"] and quiz_state["mode"] == "training":
            quiz_state["active"] = False
            print("\nMr. Smith nods. \"Discipline is knowing when to rest. See you next time.\"")
            state["visited"]["teachersroom1"] = True
        elif quiz_state["active"]:
            print("You can’t stop the first-time gate mid-test. Finish both questions.")
        else:
            print("There’s no active training to stop.")

    def handle_go(destination):
        if destination in ["corridor", "back"]:
            if quiz_state["active"] and quiz_state["mode"] == "first":
                print("Finish the two-question test before leaving!")
                return None
            print("You leave the teachers' room and head back into the corridor.")
            state["previous_room"] = "teachersroom1"
            return "corridor"
        elif destination == "classroom2015":
            if "Access Pass" in state["inventory"]:
                print("📜 You flash your Access Pass. The door to Classroom 2.015 unlocks!")
                return "classroom2015"
            else:
                print("❌ The door to Classroom 2.015 is locked. You’ll need an Access Pass from the quiz first.")
                return None
        else:
            print(f"❌ You can't go to '{destination}' from here.")
            return None


    while True:
        command = input("\n> ").strip().lower()

        if command == "look around":
            handle_look()

        elif command == "?":
            handle_help()

        elif command == "start":
            handle_start()

        elif command.startswith("answer "):
            handle_answer(command[len("answer "):])

        elif command == "stop":
            handle_stop()

        elif command.startswith("go "):
            destination = command[3:].strip()
            result = handle_go(destination)
            if result:
                return result

        elif command == "wallet":
            print(state["coins"])


        elif command == "quit":
            print("👋 You sit back in the softest chair, close your eyes, and exit the adventure. Game over.")
            sys.exit()

        else:
            print("❓ Unknown command. Type '?' to see available commands.")