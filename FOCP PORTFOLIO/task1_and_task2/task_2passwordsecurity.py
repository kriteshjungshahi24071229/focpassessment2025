# Password Security

import random
import sys

def run_security_check():
    # Step 1: Input
    secret_code = input("Enter your password: ")
    
    # Step 2: Length Check
    # Using a simple if-statement to check the requirements
    if len(secret_code) < 9:
        print("Password is too short.")
        return  # Function stops here

    # Step 3: Verify 3 characters
    attempts = 0
    while attempts < 3:
        # Using randint makes sure we stay within the password length
        spot = random.randint(1, len(secret_code))
        
        answer = input(f"Enter letter at position {spot}: ")
        
        # We subtract 1 because Python lists/strings start at 0
        correct_char = secret_code[spot - 1]
        
        if answer == correct_char:
            print("Correct")
            attempts += 1 # Only increase attempts if they got it right
        else:
            print("Security check failed.")
            sys.exit() # Requirement met: exit immediately on failure

    # Final step
    print("Security check passed.")

# This part starts the whole thing
if __name__ == "__main__":
    run_security_check()