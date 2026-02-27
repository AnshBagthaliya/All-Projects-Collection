import random
from datetime import datetime

# Subjects, Actions, Places/Things, Emojis
subjects = [
    "Shahrukh Khan", "Virat Kohli", "Nirmala Sitharaman",
    "Ms Dhoni", "Prime Minister Modi", "Rikshaw Driver", "Monkeys",
]

actions = [
    "launches", "cancels", "dances with donkey", "eats",
    "declares war", "orders", "celebrates",
]

places_things = [
    "at Red Fort", "above India Gate", "at Chai Ki Tapri",
    "in Local Train", "inside White House", "in Animal Park",
    "during IPL Match",
]

emojis = ["🔥", "🤣", "🗞️", "😲", "🇮🇳", "🐒", "🚀", "⚡"]

# Headline history
headline_log = []
count = 1

while True:
    # Generate one fake headline
    subject = random.choice(subjects)
    action = random.choice(actions)
    place_thing = random.choice(places_things)
    emoji = random.choice(emojis)

    headline = f"{count}. BREAKING NEWS: {subject} {action} {place_thing} {emoji}"
    print("\n" + "="*60)
    print(headline)
    print("="*60)

    # Store and increment
    headline_log.append(headline)
    count += 1

    # Menu options
    print("\nOptions:")
    print("1. Generate another headline")
    print("2. View all headlines")
    print("3. Save and exit")

    user_input = input("Enter your choice (1/2/3): ").strip()

    if user_input == '1':
        continue
    elif user_input == '2':
        print("\n--- All Generated Headlines ---")
        for line in headline_log:
            print(line)
    elif user_input == '3':
        filename = f"fake_news_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                for line in headline_log:
                    file.write(line + '\n')
            print(f"\n✅ All headlines saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving file: {e}")
        break
    else:
        print("\n❌ Invalid input. Please enter 1, 2, or 3.")

# Exit message
print("\n📰 Thank you for using the Fake News Generator! Have a hilarious day! 😄")
