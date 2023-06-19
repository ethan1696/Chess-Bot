def find_lsb(n):
    if n == 0:
        return None  # No bits are set

    bit_position = 0

    powers_of_2 = [32, 16, 8, 4, 2, 1]
    masks = [0xFFFFFFFF, 0xFFFF, 0xFF, 0xF, 0x3, 0x1]

    for i in range(6):
        if (n & masks[i]) == 0:
            n >>= powers_of_2[i]
            bit_position += powers_of_2[i]

    return bit_position

print(find_lsb(0b1000))