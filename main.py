MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.',
    ',': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.',
    '-': '-....-', '(': '-.--.', ')': '-.--.-'
}

def text_to_morse(text):
    morse_result = []
    for char in text.upper():
        if char in MORSE_CODE_DICT:
            morse_result.append(MORSE_CODE_DICT[char])
        elif char == " ":
            morse_result.append("/")
        else:
            morse_result.append("?")
    return " ".join(morse_result)

print("Text to morse code converter")
user_input = input("Go ahead and write a text!:")
morse = text_to_morse(user_input)
print("\nMorse code version:")
print(morse)
