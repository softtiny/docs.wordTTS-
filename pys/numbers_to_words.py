import unittest
import re

number_words = {
    # Basic numbers
    'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
    'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
    'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
    'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19,
    
    # Tens
    'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50,
    'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90,
    
    # Scales
    'hundred': 100,
    'thousand': 1000,
    'million': 1000000,
    # 'billion': 1000000000,
    # 'trillion': 1000000000000,
    
    # Special cases
    'dozen': 12,
    
    # Fractions
    'quarter': 0.25,

}


def word_split_numbers_and_letters(word:str)->list[str]:
    # Use regular expression to find sequences of digits and letters
    return re.findall(r'\d+|\D+', word)

def modify_long_text(ltxt:str) -> str:
    words = ltxt.split(" ")
    words = [x for sublist in words for x in sublist.split("\n") if x]
    modified_words = []
    idx=-1
    for word in words:
        idx+=1
        if word in number_words:
            count = number_words[word]
            modified_words.append(f"<mark>{word}</mark>~<b>{count}</b>")
        elif any(char.isdigit() for char in word):
            try:
                count = convert_str_number(word)
                english = numbers_to_words(count)
                modified_words.append(f"<mark>{english}</mark>~<b>{count}</b>")
            except ValueError:
                arr=word_split_numbers_and_letters(word)
                if len(arr)==2 and arr[1]=="%":
                    count = convert_str_number(arr[0])
                    english=numbers_to_words(count)
                    modified_words.append(f"<mark>{english} percent</mark>~<b>{count}%</b>")
                else:
                    for letter in reversed(arr):
                        words.insert(idx+1,letter)
        else:
            modified_words.append(word)
    return " ".join(modified_words)


def convert_str_number(data: str) -> int|float:
    try:
        # First try to convert to int
        return int(data)
    except ValueError:
        try:
            # If int conversion fails, try float
            return float(data)
        except ValueError:
            raise ValueError("Input string must be a valid number")
    

def numbers_to_words(number:int|float) -> str:
    # Dictionary mapping numbers to words
    ones = {
        0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four',
        5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine'
    }
    
    teens = {
        10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen',
        15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen'
    }
    
    tens = {
        2: 'twenty', 3: 'thirty', 4: 'forty', 5: 'fifty',
        6: 'sixty', 7: 'seventy', 8: 'eighty', 9: 'ninety'
    }
    
    # Handle negative numbers
    if number < 0:
        return f"negative {numbers_to_words(abs(number))}"
        
    # Handle decimal numbers
    if isinstance(number, float):
        int_part = int(number)
        decimal_part = str(number).split('.')[1]
        if int_part == 0:
            return f"zero point {' '.join(ones[int(d)] for d in decimal_part)}"
        return f"{numbers_to_words(int_part)} point {' '.join(ones[int(d)] for d in decimal_part)}"
    
    # Convert integer to string
    num_str = str(number)
    length = len(num_str)
    
    # Handle single digit numbers
    if length == 1:
        return ones[number]
        
    # Handle numbers from 10-19
    if length == 2 and number < 20:
        return teens[number]
        
    # Handle numbers from 20-99
    if length == 2:
        if num_str[1] == '0':
            return tens[int(num_str[0])]
        return f"{tens[int(num_str[0])]} {ones[int(num_str[1])]}"
        
    # Handle numbers from 100-999
    if length == 3:
        if number % 100 == 0:
            return f"{ones[int(num_str[0])]} hundred"
        return f"{ones[int(num_str[0])]} hundred {numbers_to_words(int(num_str[1:]))}"
        
    # Handle numbers from 1000-999999
    if length <= 6:
        if number % 1000 == 0:
            return f"{numbers_to_words(int(num_str[:-3]))} thousand"
        return f"{numbers_to_words(int(num_str[:-3]))} thousand {numbers_to_words(int(num_str[-3:]))}"
        
    return "number too large"

class TestNumbersToWords(unittest.TestCase):
    def test_single_digits(self):
        self.assertEqual(numbers_to_words(0), "zero")
        self.assertEqual(numbers_to_words(5), "five")
        self.assertEqual(numbers_to_words(9), "nine")

    def test_teens(self):
        self.assertEqual(numbers_to_words(10), "ten")
        self.assertEqual(numbers_to_words(13), "thirteen")
        self.assertEqual(numbers_to_words(19), "nineteen")

    def test_two_digits(self):
        self.assertEqual(numbers_to_words(20), "twenty")
        self.assertEqual(numbers_to_words(45), "forty five")
        self.assertEqual(numbers_to_words(99), "ninety nine")

    def test_three_digits(self):
        self.assertEqual(numbers_to_words(100), "one hundred")
        self.assertEqual(numbers_to_words(101), "one hundred one")
        self.assertEqual(numbers_to_words(999), "nine hundred ninety nine")

    def test_thousands(self):
        self.assertEqual(numbers_to_words(1000), "one thousand")
        self.assertEqual(numbers_to_words(1234), "one thousand two hundred thirty four")
        self.assertEqual(numbers_to_words(999999), "nine hundred ninety nine thousand nine hundred ninety nine")

    def test_negative_numbers(self):
        self.assertEqual(numbers_to_words(-5), "negative five")
        self.assertEqual(numbers_to_words(-100), "negative one hundred")

    def test_decimal_numbers(self):
        self.assertEqual(numbers_to_words(0.5), "zero point five")
        self.assertEqual(numbers_to_words(1.23), "one point two three")
        self.assertEqual(numbers_to_words(-1.1), "negative one point one")

    def test_large_numbers(self):
        self.assertEqual(numbers_to_words(1000000), "number too large")

if __name__ == '__main__':
    unittest.main()