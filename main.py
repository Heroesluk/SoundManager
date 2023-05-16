import random

import speech_recognition as sr
from playsound import playsound, PlaysoundException
from speech_recognition import UnknownValueError


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
        self.no_hint = "09_out_of_hints_intel.wav"
        self.incorrect_request = "02_speak_more_clearly.wav"

    def match(self, data, checkpoint):
        data = flatten(data)
        for hint in self.hints:
            if hint.requirements == checkpoint:
                for phrase in hint.keywords:
                    if phrase.lower() in data.lower():
                        return hint.hint_path

                return self.incorrect_request


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
        print("Wait, dont say anything microphone is adjusting noise levels ")
        recognizer.adjust_for_ambient_noise(source)
        print("Now say what you need, i.e 'give me a hint'  ")
        audio = recognizer.listen(source, timeout=3, phrase_time_limit=6)

    return recognizer.recognize_google(audio, language="pl-PL")


# just a simple simulation
# for presentation first say "i need a hint" then "give me another hint"
def game():
    # assume this is the first hint in game
    hint1 = Hint(["Give", "Hint", "help", "how do we", "what should we"], 0, "04_hint_forensics.wav")

    hint2 = Hint(["Give", "Hint", "help", "how do we", "what should we"], 1, "05_hint_date.wav")
    hint3 = Hint(["Give", "Hint", "help", "how do we", "what should we"], 2, "06_hint_lock.wav")

    hint_lvl = 0

    matcher = HintMatcher([hint1, hint2, hint3])
    while True:
        input("Press enter to activate microphone")
        try:
            text = call_microphone()
        except (UnknownValueError or PlaysoundException) as e:
            print("Couldn't recognize what you said")
            play_hint("Renders/02_speak_more_clearly.wav")
            continue

        hint_path = matcher.match(text, hint_lvl)
        play_hint(hint_path)
        hint_lvl += 1


game()
