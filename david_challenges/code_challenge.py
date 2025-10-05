import traceback
import random
import os
import subprocess
import psycopg2

#["ID", "Description", "Prompt1", "Prompt2"]

def get_answer(prob_id, username):
    # Gets code answer from database
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM answers WHERE problem_id = %s AND username != %s;", (prob_id[0], username))
            challenges = cur.fetchall()
    return challenges

def get_challenges():
    # Get list of challenges from database
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM challenges;")
            challenges = cur.fetchall()
    return challenges

#challenges = get_challenges()  # Assume this function provides a list of challenges from the database


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

challenge_script = os.path.join(os.path.dirname(__file__), 'challenge.sh')

def get_user_code(user, prompt: str) -> str:
    print(f"{prompt}")
    subprocess.run(["bash", challenge_script])


def store_answer(username, answer, challenge_selected) -> None:
    # Store the user's answer in the database
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO answers (username, answer, problem_id) VALUES (%s, %s, %s);
    """, (username, answer, challenge_selected[0]))  # Assuming problem_id is 1 for simplicity
    conn.commit()
    cur.close()
    conn.close()


def execute_user_code(user_code) -> bool:
    # Try to execute user code and handle errors
    try:
        exec(user_code)
        print("\n✅ Code executed successfully!")
        return True
    except Exception as e:
        print("\n❌ Error during code execution:")
        print(traceback.format_exc())
        return False


def code_challenge(user1, user2):
    """
    Gets code snippets from two users and attempts to execute them
    """

    # Temporary player selection for testing
    player = input("Enter player number (1 or 2): ")

    # Select challenge
    #challenge_selected = random.choice(challenges) # randomly selects a challenge from the challenges list
    #print(f"Challenge: {challenge_selected[0][1]}") # prints the description of the challenge
    #print(f"Challenge: {challenge_selected[0][1]}") # prints the description of the challenge
    challenges = get_challenges()
    challenge_selected = random.choice(challenges) # randomly selects a challenge from the challenges list
    print(f"\nChallenge: {challenge_selected[1]}") # prints the description of the challenge
    if(input(f"Do you accept the challenge? (y/n): ").lower() == 'y'):
        prompt1 = challenge_selected[2] # gets the prompt for user1 for the selected challenge
        prompt2 = challenge_selected[3] # gets the prompt for user2 for the selected challenge
        print(f"{prompt1}\n{prompt2}")
    
        ## Challenges Branches ##
        #if challenge_selected == challenges[0]: # If the selected challenge is the first one (change to switch for more challenges)
        if True: # Placeholder for challenge branch   
            # Get user1 code input
            if player == "1":
                get_user_code(user1, prompt1)
                input("Press Enter when done...") # Wait for user to finish editing
                with open('challenge.py', 'r') as file:
                    user1_code = file.read()
                
                # Store user1 code in database
                store_answer(user1, user1_code, challenge_selected)

                # Get user2's answer from database
                user2_code = get_answer(challenge_selected, user2)
            
            if player == "2":
                # Get user2 code input
                get_user_code(user2, prompt2)
                input("Press Enter when done...") # Wait for user to finish editing
                with open('challenge.py', 'r') as file:
                    user2_code = file.read()

                # Store user2 code in database
                store_answer(user2, user2_code, challenge_selected)

                # Get user1's answer from database
                user1_code = get_answer(challenge_selected, user1)


            # Combine user responses and test code
            combined_code = f"#{user1}'s code \n{user1_code} \n#{user2}'s code \n{user2_code}"

            # Try to execute user code
            if(execute_user_code(combined_code)):
                print(f"\nCoding challenge PASSED! Both codes executed successfully!")
            else:
                print(f"\nCoding challenge FAILED! The combined code failed to execute :(")
            
            #print(f"\nCombined Code:\n{combined_code}") # For testing purposes, print the combined code

    
    else: # challenge not accepted
        print(f"\nChallenge not accepted.")
        return
    