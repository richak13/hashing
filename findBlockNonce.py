#!/bin/python
import hashlib
import os
import random


def mine_block(k, prev_hash, rand_lines):
    """
        k - Number of trailing zeros in the binary representation (integer)
        prev_hash - the hash of the previous block (bytes)
        rand_lines - a set of "transactions," i.e., data to be included in this block (list of strings)

        This function finds a nonce such that sha256(prev_hash + rand_lines + nonce)
        has k trailing zeros in its *binary* representation
    """
    # Prepare the data by concatenating prev_hash and all transactions as bytes
    data = prev_hash + ''.join(rand_lines).encode('utf-8')

    nonce = 0  # Start nonce at zero and increment until a valid one is found
    target_zeros = '0' * k  # Target k trailing zeros in the binary representation

    while True:
        # Convert nonce to bytes
        nonce_bytes = nonce.to_bytes((nonce.bit_length() + 7) // 8, byteorder='big')
        
        # Calculate SHA256 hash of the data concatenated with nonce
        hash_result = hashlib.sha256(data + nonce_bytes).hexdigest()
        
        # Convert hash to binary and check the last k bits
        if bin(int(hash_result, 16))[-k:] == target_zeros:
            return nonce_bytes
        
        # Increment nonce and try again
        nonce += 1


def get_random_lines(filename, quantity):
    """
    This is a helper function to get the quantity of lines ("transactions")
    as a list from the filename given. 
    Do not modify this function
    """
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line.strip())

    random_lines = []
    for x in range(quantity):
        random_lines.append(lines[random.randint(0, quantity - 1)])
    return random_lines


if __name__ == '__main__':
    # This code will be helpful for your testing
    filename = "bitcoin_text.txt"
    num_lines = 10  # The number of "transactions" included in the block

    # The "difficulty" level. For our blocks this is the number of Least Significant Bits
    # that are 0s. For example, if diff = 5 then the last 5 bits of a valid block hash would be zeros
    # The grader will not exceed 20 bits of "difficulty" because larger values take to long
    diff = 20

    rand_lines = get_random_lines(filename, num_lines)
    nonce = mine_block(diff, rand_lines)
    print(nonce)
