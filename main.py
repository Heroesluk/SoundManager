import speech_recognition as sr




class Matcher():

    def __init__(self):
        self.hints = [Hint()]

    def match(self, data, checkpoint):
        data = self.flatten(data)
        for hint in self.hints:
            for key_word in hint.keywords:
                if key_word in data:
                    if checkpoint >= max(hint.requirements):
                        return True

        return False

    def flatten(self, data):
        protected = ['ą', 'ę', 'ż', 'ź', 'ć', 'ś']
        replaced = ['a', 'e', 'z', 'z', 'c', 's']
        fixed = ""
        for chr in data:
            if chr in protected:
                fixed += replaced[protected.index(chr)]
            else:

                fixed += chr

        return fixed


class Hint():
    def __init__(self, keywords=None, requirements=None):
        if not keywords:
            self.keywords = ["podpowiedz", "wskazówke", "pomoc", "nie wiem"]
        if not requirements:
            self.requirements = [1, 2]




m1 = Matcher()

r = sr.Recognizer()

mic = sr.Microphone()
with mic as source:
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source, timeout=3, phrase_time_limit=6)

output = r.recognize_google(audio, language="pl-PL")


print(m1.match(output,3))
