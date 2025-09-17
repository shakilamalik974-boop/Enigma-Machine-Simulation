# Enigma Machine Simulation in Python
print("Welcome To Enigma Machine")

import string
from dataclasses import dataclass
from colorama import Fore, Style, init
init(autoreset=True)

# Letters A-Z
ALPHABET = string.ascii_uppercase
A_INDEX = {c: i for i, c in enumerate(ALPHABET)}

def char_to_index(c):
    return A_INDEX[c]

def index_to_char(i):
    return ALPHABET[i % 26]

# Plugboard (used to swap letters before and after rotors)
@dataclass
class Plugboard:
    wiring: dict
    @classmethod
    def from_pairs(cls, pairs):
        # pairs are like ["AV","BS"] etc
        wiring = {c: c for c in ALPHABET}
        for p in pairs:
            a, b = p[0], p[1]
            wiring[a] = b
            wiring[b] = a
        return cls(wiring)
    def swap(self, c):
        return self.wiring.get(c, c)

# Rotor (each rotor has wiring, notch and position)
@dataclass
class Rotor:
    wiring: str
    notch: str
    position: int = 0
    ring_setting: int = 0
    def step(self):
        # rotor moves one step
        self.position = (self.position + 1) % 26
    def at_notch(self):
        # check if rotor is at notch position
        return index_to_char(self.position) in self.notch
    def forward(self, c):
        # pass letter forward (right to left)
        i = (char_to_index(c) + self.position - self.ring_setting) % 26
        mapped_char = self.wiring[i]
        j = (char_to_index(mapped_char) - self.position + self.ring_setting) % 26
        return index_to_char(j)
    def backward(self, c):
        # pass letter backward (left to right)
        i = (char_to_index(c) + self.position - self.ring_setting) % 26
        target = index_to_char(i)
        k = self.wiring.index(target)
        j = (k - self.position + self.ring_setting) % 26
        return index_to_char(j)

# Reflector (fixed mapping, same both ways)
@dataclass
class Reflector:
    wiring: str
    def reflect(self, c):
        return self.wiring[char_to_index(c)]

# Main Enigma Machine
class EnigmaMachine:
    def __init__(self, rotors, reflector, plugboard):
        self.rotors = rotors   # left to right
        self.reflector = reflector
        self.plugboard = plugboard

    def step_rotors(self):
        # implement rotor stepping (double stepping)
        left, middle, right = self.rotors
        left_turn = middle.at_notch()
        mid_turn = right.at_notch()
        if left_turn:
            left.step()
        if mid_turn or left_turn:
            middle.step()
        right.step()

    def process_char(self, ch):
        if ch not in ALPHABET:
            return ch
        # rotors step before processing
        self.step_rotors()
        # plugboard first
        c = self.plugboard.swap(ch)
        # go forward through rotors
        for rotor in reversed(self.rotors):
            c = rotor.forward(c)
        # reflector
        c = self.reflector.reflect(c)
        # back through rotors
        for rotor in self.rotors:
            c = rotor.backward(c)
        # plugboard again
        c = self.plugboard.swap(c)
        return c

    def encrypt(self, text):
        text = text.upper()
        out = []
        for ch in text:
            if ch == ' ':
                out.append(' ')
            else:
                out.append(self.process_char(ch))
        return ''.join(out)

    def set_positions(self, positions):
        # set starting positions for rotors
        p = ''.join(positions.split()).upper()
        for rotor, pos_char in zip(self.rotors, p):
            rotor.position = char_to_index(pos_char)

# Rotor wirings and reflectors (Enigma I)
ROTOR_SPECS = {
    'I':   ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
    'II':  ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
    'III': ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),
    'IV':  ("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"),
    'V':   ("VZBRGITYUPSDNHLXAWMJQOFECK", "Z"),
}
REFLECTORS = {
    'B': "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    'C': "FVPJIAOYEDRZXWGCTKUQSBNMHL",
}

# function to build machine with given settings
def build_example_enigma(left='I', middle='II', right='III', reflector='B', plug_pairs=None, ring_settings=(0,0,0), start_positions="AAA"):
    if plug_pairs is None:
        plug_pairs = ["AV","BS","CG","DL","FU","HZ","IN","KM","OW","RX"]
    rL = Rotor(wiring=ROTOR_SPECS[left][0], notch=ROTOR_SPECS[left][1])
    rM = Rotor(wiring=ROTOR_SPECS[middle][0], notch=ROTOR_SPECS[middle][1])
    rR = Rotor(wiring=ROTOR_SPECS[right][0], notch=ROTOR_SPECS[right][1])
    plug = Plugboard.from_pairs(plug_pairs)
    refl = Reflector(wiring=REFLECTORS[reflector])
    enigma = EnigmaMachine(rotors=[rL, rM, rR], reflector=refl, plugboard=plug)
    enigma.set_positions(start_positions)
    return enigma



# Example run
enigma = build_example_enigma(start_positions="AAA")
plaintext = "SHAKILA MALIK"
cipher = enigma.encrypt(plaintext)
enigma_dec = build_example_enigma(start_positions="AAA")
decrypted = enigma_dec.encrypt(cipher)

print(Fore.GREEN + "Plaintext : " + plaintext)
print(Fore.RED   + "Ciphertext: " + cipher)
print(Fore.CYAN  + "Decrypted : " + decrypted)