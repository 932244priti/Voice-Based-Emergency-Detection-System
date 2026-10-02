import pandas as pd
import random

# -----------------------------------------
# Emergency sentences
# -----------------------------------------

emergency_templates = [
    "Help me",
    "Please help me",
    "I need help",
    "I need immediate help",
    "Someone is following me",
    "Someone is chasing me",
    "Someone is attacking me",
    "I am being attacked",
    "Someone is trying to hurt me",
    "I am in danger",
    "I am scared please help me",
    "Please save me",
    "Call the police",
    "Call someone immediately",
    "I need help right now",
    "I am trapped",
    "I cannot get away",
    "Someone is threatening me",
    "Please call for help",
    "Emergency please help",
    "I am afraid",
    "I am not safe",
    "There is someone outside",
    "Someone is trying to enter",
    "I need emergency assistance",
    "Please send help",
    "I am in trouble",
    "Something bad is happening",
    "I feel unsafe",
    "Please contact the police"
]

# -----------------------------------------
# Normal sentences
# -----------------------------------------

normal_templates = [
    "Hello",
    "Hi",
    "How are you",
    "Good morning",
    "Good evening",
    "I am fine",
    "Everything is fine",
    "I am safe",
    "I am going home",
    "I am going to college",
    "I am going to school",
    "I am studying",
    "I am doing my homework",
    "I am watching television",
    "I am watching a movie",
    "I am listening to music",
    "I am cooking food",
    "I am having dinner",
    "I am having lunch",
    "I am going shopping",
    "I am at the market",
    "I am meeting my friend",
    "I am travelling",
    "I am waiting for my friend",
    "I will call you later",
    "I will reach home soon",
    "Please call me tomorrow",
    "I am working",
    "I am using my laptop",
    "I am going to sleep"
]

# -----------------------------------------
# Generate variations
# -----------------------------------------

emergency_variations = [
    "Please {}",
    "{} please",
    "{} right now",
    "{} immediately",
    "I really need help, {}",
    "Please listen, {}",
    "Emergency, {}",
    "{} help me",
    "Please help, {}",
    "{} please help"
]

normal_variations = [
    "{}",
    "I just want to say {}",
    "Today {}",
    "Right now {}",
    "I am okay, {}",
    "Everything is okay, {}",
    "{} thank you",
    "{} today"
]

data = []

# Add emergency samples
for sentence in emergency_templates:

    data.append({
        "text": sentence,
        "label": "emergency"
    })

    for template in emergency_variations:

        variation = template.format(sentence)

        data.append({
            "text": variation,
            "label": "emergency"
        })


# Add normal samples
for sentence in normal_templates:

    data.append({
        "text": sentence,
        "label": "normal"
    })

    for template in normal_variations:

        variation = template.format(sentence)

        data.append({
            "text": variation,
            "label": "normal"
        })


# Shuffle dataset
random.shuffle(data)

# Create dataframe
df = pd.DataFrame(data)

# Remove duplicate sentences
df = df.drop_duplicates()

# Save dataset
df.to_csv(
    "emergency_voice_dataset.csv",
    index=False
)

print("====================================")
print("DATASET CREATED SUCCESSFULLY")
print("====================================")

print("Total samples:", len(df))

print("\nClass distribution:")
print(df["label"].value_counts())

print("\nFirst 10 samples:")
print(df.head(10))

print("\nSaved as:")
print("emergency_voice_dataset.csv")