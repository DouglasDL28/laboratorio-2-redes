# Hammming Code
# Reference: https://www.geeksforgeeks.org/hamming-code-implementation-in-python/
# Changed to implement bitarray instead of list

from bitarray import bitarray


def is_power_of_two(x):
    return (x != 0) and ((x & (x - 1)) == 0)


def r_bits(m):
    """ Find the number r, that satisfies (m + r + 1) ≤ 2^r """

    for r in range(m):
        if(2**r >= m + r + 1):
            return r


def pos_r_bits(data:bitarray, r:int):
    """ Create Hamming code w/o parity """

    m = len(data)

    res = bitarray()

    # If position is power of 2 then insert '0'
    # Else append the data
    for i in range(1, m+r+1):
        if is_power_of_two(i):
            res.insert(0, 0)
        else:
            res.insert(0, data.pop())

    return res


def rm_r_bits(data:bitarray):
    """ Remove redundant bits. """

    n = len(data)

    res = bitarray()

    # If position is power of 2 skip redundant bit
    # Else append the data
    for i in range(1, n+1):
        if not is_power_of_two(i):
            res.insert(0, data.pop())
        else:
            data.pop()

    return res

def calc_parity_bits(arr, r):
    """ Calculates parity value in redundant values' positions. """

    n = len(arr)

    # For finding rth parity bit, iterate over 0 to r - 1
    for i in range(r):
        val = 0
        for j in range(1, n + 1):
            # If position has 1 in ith significant
            # position then Bitwise OR the array value
            # to find parity bit value.
            if(j & (2**i) == (2**i)):
                val = val ^ int(arr[-1 * j])

        # Add parity value in correct position
        # (0 to n - 2^r) + parity bit + (n - 2^r + 1 to n)
        arr = arr[:n-(2**i)] + str(val) + arr[n-(2**i)+1:]
        
    return arr


def detect_error(arr, r):
    n = len(arr)
    res = 0

    # Calculate parity bits again
    for i in range(r):
        val = 0
        for j in range(1, n+1):
            if(j & (2**i) == (2**i)):
                val = val ^ int(arr[-1 * j])

        # Create a binary no by appending parity bits together.

        res = res + val*(10**i)

    # Convert binary to decimal
    return int(str(res), 2)

def hamming_test():

    # Enter the data to be transmitted
    data = bitarray('1011001')
    print(data)

    # Calculate the no of Redundant Bits Required
    m = len(data)
    r = r_bits(m)
    print("redundant bits needed:", r)


    # Determine the positions of Redundant Bits
    arr = pos_r_bits(data, r)
    print(arr)

    # Determine the parity bits
    arr = calc_parity_bits(arr, r)

    # Data to be transferred
    print("Data transferred is ", arr) 

    # Stimulate error in transmission by changing a bit value.
    # 10101001110 -> 11101001110, error in 10th position.

    arr = bitarray('10101001110')
    arr = bitarray('11101001110')
    print("Error Data is:", arr)
    correction = detect_error(arr, r)

    if correction:
        print("The position of error is:", str(correction))

        arr.invert(-1*(correction))

        print(rm_r_bits(arr))
    else:
        print("No error")
        print(rm_r_bits(arr))


if __name__ == "__main__":
    hamming_test()