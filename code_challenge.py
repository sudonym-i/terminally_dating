import traceback
import random
import os
import subprocess
import sqlite3
import psycopg2

#["ID", "Description", "Prompt1", "Prompt2"]

def get_challenges():
    # Get list of challenges from database
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Challenge;")
    challenges = cur.fetchall()
    cur.close()
    conn.close()
    return challenges

challenges = get_challenges()  # Assume this function provides a list of challenges from the database


def get_conn():
    # Update with your server details
    conn = psycopg2.connect(
        host="192.168.137.50",  # e.g., "localhost" or IP address
        database="mydatabase",
        user="terminally",
        password="dating",
        port=5432  # default PostgreSQL port
    )
    return conn


def get_user_code(user, prompt: str) -> str:
    subprocess.run(['cmd', '/c', 'challenge.sh'])


def store_answer(username, answer) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO Answer VALUES (%s);
    """, (username, answer))
    conn.commit()
    cur.close()
    conn.close()


def code_challenge(user1, user2, challenges):
    """
    Gets code snippets from two users and attempts to execute them
    """

    # Select challenge
    challenge_selected = random.choice(challenges) # randomly selects a challenge from the challenges list
    print(f"Challenge: {challenge_selected[0][1]}") # prints the description of the challenge
    if(input.lower(f"Do you accept the challenge? (y/n): ") == 'y'):
        prompt1 = challenge_selected[0][2] # gets the prompt for user1 for the selected challenge
        prompt2 = challenge_selected[0][3] # gets the prompt for user2 for the selected challenge
    
        ## Challenges Branches ##
        if challenge_selected == challenges[0]: # If the selected challenge is the first one (change to switch for more challenges)
            
            # Get user1 code input
            get_user_code(user1, prompt1)
            with open('challenge.py', 'r') as file:
                user1_code = file.read()
            
            # Store user1 code in database
            store_answer(user1, user1_code)
            
            # Get user2 code input
            get_user_code(user2, prompt2)
            with open('challenge.py', 'r') as file:
                user2_code = file.read()

            # Store user2 code in database
            store_answer(user2, user2_code)

            # Combine user responses and test code
            combined_code = user1_code + user2_code

            # Try to execute user code
            execute_user_code(combined_code)

            


         
    
    
    else: # challenge not accepted
        print(f"\nChallenge not accepted.")
        return
        




### Example functions from gpt ###


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


