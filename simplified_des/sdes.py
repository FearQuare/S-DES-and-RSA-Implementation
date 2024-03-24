# S-DES KEY GENERATION:
def P10(input_key):
    """
    Applies the P10 permutation to the input 10-bit key.
    :param input_key:
    :return: permuted string according to P10 permutation given in the S-DES.pdf.
    """
    p10_perm = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    return ''.join(input_key[i-1] for i in p10_perm)

# Uncomment below to see "1010000010" is permuted to "1000001100"
print("The result of the P10 when the input_key = 1010000010 |",P10("1010000010"))