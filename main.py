import random

import speech_recognition as sr
from playsound import playsound


def flatten(data):
    protected = ['ą', 'ę', 'ż', 'ź', 'ć', 'ś']
    replaced = ['a', 'e', 'z', 'z', 'c', 's']
    fixed = ""
    for chr in data:
        if chr in protected:
            fixed += replaced[protected.index(chr)]
        else:

            fixed += chr

    return fixed


class HintMatcher():

    def __init__(self, hints):
        self.hints = hints
        self.no_hint = random.choice(["10_out_of_hints_on_your_own_pitch.wav", "09_out_of_hints_intel.wav"])

    def match(self, data, checkpoint):
        data = flatten(data)
        for hint in self.hints:
            if hint.requirements == checkpoint:
                for phrase in hint.keywords:
                    if phrase.lower() in data.lower():
                        return hint.hint_path



        return self.no_hint


class Hint():
    def __init__(self, keywords=None, requirements=None, hint=None):
        self.keywords = keywords
        self.requirements = requirements
        self.hint_path = hint


def play_hint(filename):
    playsound("Renders/{}".format(filename))



def call_microphone():
    recognizer = sr.Recognizer()

    mic = sr.Microphone()
    with mic as source:
        # wait 1 second before providing sound input
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=3, phrase_time_limit=6)

    return recognizer.recognize_google(audio, language="pl-PL")


# just a simple simulation
def game():
    # assume this is the first hint in game
    hint1 = Hint(["Give us", "Hint", "we need help", "how do we", "what should we"], 0, "04_hint_forensics.wav")

    hint2 = Hint(["Give us", "Hint", "we need help", "how do we", "what should we"], 1, "05_hint_date.wav.wav")
    hint3 = Hint(["Give us", "Hint", "we need help", "how do we", "what should we"], 2, "06_hint_lock.wav.wav")

    hint_lvl = 0

    matcher = HintMatcher([hint1, hint2])

    input()

    hint_lvl += 1
    text = call_microphone()
    hint_path = matcher.match(text, hint_lvl)
    play_hint(hint_path)

    input()

    hint_lvl += 1
    text = call_microphone()
    hint_path = matcher.match(text, hint_lvl)
    play_hint(hint_path)



game()
