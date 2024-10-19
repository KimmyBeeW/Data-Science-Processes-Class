import numpy as np
from typing import List
import string

# 1
def euclid_dist(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    x1, y1 = p1
    x2, y2 = p2
    dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    if dist == int(dist):  # if the output is a whole number get rid of the decimal
        return int(dist)
    else:
        return dist


# 2
def sum_ns(n: int) -> int:
    return n + int(str(n)+str(n)) + int(str(n)+str(n)+str(n))


# 3
def perfect_square(n: int):
    x = np.sqrt(n)
    if x == int(x):  # if the output is a whole number return statement
        return f"{n} is a perfect square of {int(x)}"
    else:
        return False


# 4
def is_palindrome(s: str) -> bool:
    s = ''.join(s.split()) # remove whitespace
    if s == s[::-1]:
        return True
    else:
        return False


# 5
def count_letter_types(s: str) -> dict:
    counts = {'upper': 0, 'lower': 0, 'space': 0}
    for char in s:
        if char.isupper():
            counts['upper'] += 1
        elif char.islower():
            counts['lower'] += 1
        elif char == " ":
            counts['space'] += 1
    return counts


# 6
def count_word_lengths(s: str) -> dict:
    slst1 = s.split(" ")
    slst = sorted([s.strip(string.punctuation) for s in slst1], key=len)
    counts = {}
    for i in range(len(slst)):
        if len(slst[i]) not in counts:
            counts[len(slst[i])] = [slst[i]]
        else:
            counts[len(slst[i])].append(slst[i])
    return counts


# 7
def n_list(n: int):
    if n < 2 or n > 9 or (type(n) != int):
        return 'Invalid input: enter a number between 2 and 9'
    else:
        return [i for i in range(int(str(n)+"01")) if (i % n == 0 and str(n) in str(i))]


# 8
def evens_mean_max(nums: List[int]):
    evens = [n for n in nums if n % 2 == 0]
    print(f"The sum of the even numbers is {sum(evens)}.")
    count = 0
    for ele in evens:
        if (ele == max(evens)):
            count = count + 1
    print(f"The maximum of the even numbers is {max(evens)} and it appears {count} time(s) in the list.")
