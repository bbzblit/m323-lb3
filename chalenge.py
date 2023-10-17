import math

START = 2256
MOD = 3565

def is_palindrome(num):
    return str(num) == str(num)[::-1]

if __name__ == "__main__":
    while not (not is_palindrome(START) and is_palindrome(math.sqrt(START))):
        START += MOD
    print("Found ", START)
        