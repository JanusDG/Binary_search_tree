import copy
import time
import random
import sys

from linkedbst import LinkedBST

def read_words(path):
    with open(path, "r") as file:
        words = [item.strip() for item in file.readlines()]
    return words[:10000]

def test_list(words):
    start = time.time()
    for i in range(10000):
        random.choice(words) in words

    return time.time() - start

def test_sorted_tree(words):
    tree = LinkedBST(words)
    start = time.time()
    for i in range(10000):
        random.choice(words) in tree

    return time.time() - start
    

def test_random_tree(words):
    random.shuffle(words)
    tree = LinkedBST(words)
    start = time.time()
    for i in range(10000):
        random.choice(words) in tree
    return time.time() - start


def test_balanced_tree(words):
    tree = LinkedBST()
    words_in_tree = copy.deepcopy(words)
    while words_in_tree:
        i = len(words_in_tree)//2
        tree.add(words_in_tree[i])
        del words_in_tree[i]
    
    start = time.time()
    for i in range(10000):
        random.choice(words) in tree
    return time.time() - start


if __name__ == "__main__":
    sys.setrecursionlimit(10**5)
    words = read_words("words.txt")
    print(test_list(words))
    print(test_sorted_tree(words))
    print(test_random_tree(words))
    print(test_balanced_tree(words))