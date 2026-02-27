# 1- Import The randome modul
import random

# 2- Create subjects
subjects = [
    "Shahrukh Khan",
    "Virat Kohli",
    "Nirmala Sitharaman",
    "Ms Dhoni",
    "Prime Minister Modi",
    "Rikshow Driver",
    "Monkeys",
]

actions = [
    "launches",
    "cancels",
    "dances with donkey",
    "eats",
    "declares War",
    "orders",
    "celebrates",
]

places_things = [
    "at Red Fort",
    "above India Gate",
    "Chai Ki Tapri",
    "Local Train",
    "inside White House",
    "in Animal Park",
    "during IPL Match",
]

# 3- start the headline generation loop
while True:
    subject = random.choice(subjects)
    action = random.choice(actions)
    place_things = random.choice(places_things)

    headline = f"BREAKING NEWS:{subject} {action} {place_things}"
    print('\n' + headline)

    user_input = input("\n Do you want another headline? (yes/no)").strip()
    if user_input == 'no':
        break

# Print good bye message
print('\n Thank for using Fake News Generator. Have Fun Day')
