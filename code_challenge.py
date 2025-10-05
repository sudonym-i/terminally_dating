import traceback
import random
import os
import subprocess
import sqlite3
import psycopg2

#["ID", "Description", "Prompt"]
"""db syntax:
with getdb(args.db) as conn:
    conn.execute("
    INSERT INTO Answer VALUES (?);", (answer);)

"""

challenges = get_challenges()  # Assume this function provides a list of challenges from the database

def code_challenge(user1, user2, challenges):
    """
    Gets code snippets from two users and attempts to execute them
    """

    # Select challenge
    challenge_selected = random.choice(challenges) # randomly selects a challenge from the challenges list
    print(f"Challenge: {challenge_selected[0][1]}") # prints the description of the challenge
    if(input.lower(f"Do you accept the challenge? (y/n): ") == 'y'):
        prompt = challenge_selected[0][2] # gets the prompt for the selected challenge
    
        ## Challenges Branches ##
        if challenge_selected == challenges[0]: # If the selected challenge is the first one (change to switch for more challenges)
            
            # Get user1 code input
            get_user_code(user1, prompt)
            with open('challenge.py', 'r') as file:
                user1_code = file.read()
            
            # Store user1 code in database
            conn = sqlite3.connect('database.db')
            with getdb(args.db) as conn:
                conn.execute("""
                INSERT INTO Answer VALUES (?);
                """, (user1_code))

            
    
    
    else: # challenge not accepted
        return
        

    

        

  

    # Execute user code (assuming code is safe to execute) - isaac will make a script for this
    exec(user1_code)
    exec(user2_code)
    
    pass

def get_user_code(user, prompt: str) -> str:
    subprocess.run(['cmd', '/c', 'challenge.sh'])

# old 
def get_user_code(user, prompt: str) -> str:
    # Prompts for code input
    user1_code = input(f"{prompt} {user1}'s function {function_name}:\n")
    user2_code = input(f"Implement :\n")



### Example functions from gpt


def get_user_code(user, required_func, dependent_func, prompt: str) -> str:
    print(f"""\n--- User {user}'s turn ---
        Define a function called '{required_func}(x)'
        You can assume a function '{dependent_func}(x)' exists, but you cannot see its code.
        Enter your code below (type END on a new line to finish):""")

    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines)


def execute_user_code(user_code, user_globals):
    try:
        exec(user_code, user_globals)
        return True, ""
    except Exception as e:
        return False, traceback.format_exc()


def run_combined_test(user1_globals, user2_globals):
    try:
        # Link both sets of globals so they can access each other's functions
        combined_globals = {}
        combined_globals.update(user1_globals)
        combined_globals.update(user2_globals)

        print("\n--- Executing test: user1_func(5) ---")
        result = eval("user1_func(5)", combined_globals)
        print(f"✅ Success! Result: {result}")
    except Exception as e:
        print("❌ Error during execution:")
        print(traceback.format_exc())


def main():
    print("=== Welcome to the Blind Function Collaboration Challenge ===")

    # Get user codes
    user1_code = get_user_code(1, "user1_func", "user2_func")
    user2_code = get_user_code(2, "user2_func", "user1_func")

    # Isolated execution scopes
    user1_globals = {}
    user2_globals = {}

    # Execute User 1
    success1, err1 = execute_user_code(user1_code, user1_globals)
    if not success1:
        print("\n Error in User 1's code:")
        print(err1)
        return

    # Execute User 2
    success2, err2 = execute_user_code(user2_code, user2_globals)
    if not success2:
        print("\n Error in User 2's code:")
        print(err2)
        return

    # Run combined test
    run_combined_test(user1_globals, user2_globals)

if __name__ == "__main__":
    main()


