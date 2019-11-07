import random
import sys
import select

def get_user_input(max_score, timeout):

    print("\n  ####! Type an integer from 1 to 5 and press ENTER to evaluate the quality of this song: "
          #"\n        ...you have " + str(timeout) + " seconds..."
        )

    i, o, e = select.select([sys.stdin], [], [], 3)

    if i:
        input_value = sys.stdin.readline().strip()
    else:
        print("\nSorry, your time has expired. :( A random choice was made for you.\n")
        input_value = None

    if input_value is not None \
            and input_value.isdigit()\
            and 5 >= float(input_value) >= 1\
            and input_value != '':

        score = float(input_value)
    else:
        score = random.choice(range(1, max_score + 1))

    return score
