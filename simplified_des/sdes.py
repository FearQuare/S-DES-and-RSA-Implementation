# S-DES KEY GENERATION:
def P10(input_key):
    """
    Applies the P10 permutation to the input 10-bit key.
    :param input_key:
    :return: permuted string according to P10 permutation given in the S-DES.pdf.
    """
    p10_perm = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    return ''.join(input_key[i - 1] for i in p10_perm)


# Uncomment below to see "1010000010" is permuted to "1000001100"
secret_key = "1010000010"
permuted_key_10 = P10(secret_key)
print("The result of the P10 when the input_key = 1010000010 |", permuted_key_10)


def LS_1(key_half):
    """
    Performs a circular left shift by 1 position on a 5-bit key half.
    :param key_half:
    :return: left shifted output of the half of the main key
    """
    return key_half[1:] + key_half[:1]


# Uncomment below to see "10000", "01100" -> "00001", "11000"
first_half = permuted_key_10[:5]
second_half = permuted_key_10[5:]
print("\nFirst half of the key:", first_half, "\nSecond half of the key:", second_half)
ls_first_half = LS_1(first_half)
ls_second_half = LS_1(second_half)
print("\nLeft shifted first half:", ls_first_half, "\nLeft shifted second half:", ls_second_half)


def P8(key):
    """
    Applies the P8 permutation to produce an 8-bit subkey from a 10-bit key.
    :param key:
    :return: permuted string according to P8 permutation given in the S-DES.pdf.
    """
    p8_perm = [6, 3, 7, 4, 8, 5, 10, 9]
    return ''.join(key[i - 1] for i in p8_perm)


concatenated_halves = ls_first_half + ls_second_half
key1 = P8(concatenated_halves)
print("\n8 bit permutation of the concatenated left shifted halves is (aka key 1):", key1)

# To produce key 2
ls_first_left = LS_1(ls_first_half)
ls_second_left = LS_1(ls_first_left)

ls_first_right = LS_1(ls_second_half)
ls_second_right = LS_1(ls_first_right)

print("\nThe left shifted halves were '00001' and '11000'. After we left shifted them two times "
      "more they are:", "\nFirst half:", ls_second_left, "\nSecond half:", ls_second_right)

concatenated_halves_second = ls_second_left + ls_second_right
key2 = P8(concatenated_halves_second)
print("\nThe second key is:", key2)


# Now let's put them into a key generating function:

def generate_subkeys(master_key):
    # Apply P10 permutation
    permuted_key = P10(master_key)
    # Split the key and perform circular left shift
    left_half, right_half = permuted_key[:5], permuted_key[5:]
    left_half = LS_1(left_half)
    right_half = LS_1(right_half)
    # Combine halves and apply P8 to get K1
    k1 = P8(left_half + right_half)
    # Perform another round of shifts for K2
    left_half = LS_1(left_half)
    left_half = LS_1(left_half)
    right_half = LS_1(right_half)
    right_half = LS_1(right_half)
    k2 = P8(left_half + right_half)

    return k1, k2


# So this function must give the same output shown above
print("\nSo the generate_subkeys function should return the same k1 and k2 displayed above:",
      generate_subkeys("1010000010"))


# S-DES ENCRYPTION:
def IP(plaintext):
    """
    Applies the initial permutation (IP) on the 8-bit plaintext.
    :param plaintext:
    :return: permuted string according to initial permutation given in the S-DES.pdf.
    """
    ip_perm = [2, 6, 3, 1, 4, 8, 5, 7]
    return ''.join(plaintext[i - 1] for i in ip_perm)


def inverse_IP(ciphertext):
    """
    Applies the inverse initial permutation (IP-1) on the 8-bit ciphertext.
    :param ciphertext: permuted string according to inverse permutation given in the S-DES.pdf.
    :return:
    """
    inverse_ip_perm = [4, 1, 3, 5, 7, 2, 8, 6]
    return ''.join(ciphertext[i - 1] for i in inverse_ip_perm)


# Let's see if they are really the inverses of them by putting key 1:
print("initial permutation:", IP("101001000"), "\ninverse permutation:", inverse_IP(IP("101001000")))


def expand_and_permute(right_half):
    """
    Expands and permutes the right half (4 bits) of the data to 5 bits using E/P.
    :param right_half:
    :return:
    """
    e_p_perm = [4, 1, 2, 3, 2, 3, 4, 1]
    return ''.join(right_half[i - 1] for i in e_p_perm)


def xor(bits1, bits2):
    """
    Performs a bit-wise XOR operation between two bit strings.
    :param bits1:
    :param bits2:
    :return:
    """
    return ''.join(str(int(b1) ^ int(b2)) for b1, b2 in zip(bits1, bits2))


def S_box(input_bits, S_box):
    """
    Applies an S-box substitution on 4-bit input.
    :param input_bits:
    :param S_box:
    :return:
    """
    row = int(input_bits[0] + input_bits[3], 2)
    col = int(input_bits[1] + input_bits[2], 2)
    return format(S_box[row][col], '02b')


def F(right_half, subkey):
    """
    The complex function F used in the fK operation, involving expansion/permutation,
    substitution, and a permutation P4.
    :param right_half:
    :param subkey:
    :return:
    """
    # Expand and permute
    expanded_right = expand_and_permute(right_half)
    # XOR with the subkey
    xor_result = xor(expanded_right, subkey)
    # Split for S-boxes
    left_bits, right_bits = xor_result[:4], xor_result[4:]
    # Define S-boxes
    S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
    S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]
    # Apply S-boxes
    sbox_output = S_box(left_bits, S0) + S_box(right_bits, S1)
    # P4 permutation
    p4_perm = [2, 4, 3, 1]
    f_result = ''.join(sbox_output[i - 1] for i in p4_perm)
    return f_result


def fK(bits, subkey):
    """
    The function fK, which is a combination of permutation and substitution functions.
    :param bits:
    :param subkey:
    :return:
    """
    left_half, right_half = bits[:4], bits[4:]
    # Apply the F function
    f_result = F(right_half, subkey)
    # XOR the result with the left half and concatenate with the right half
    left_result = xor(left_half, f_result)
    return left_result + right_half


def SW(bits):
    """
    The switch function (SW) which swaps the left and right halves of the data.
    :param bits:
    :return:
    """
    return bits[4:] + bits[:4]


def encrypt(plaintext, key):
    """
    Encrypts an 8-bit plaintext using the S-DES encryption algorithm.
    :param plaintext:
    :param key:
    :return:
    """
    K1, K2 = generate_subkeys(key)
    # Initial permutation
    initial_permuted = IP(plaintext)
    # First round of fK with K1
    after_fK1 = fK(initial_permuted, K1)
    # Switch function
    after_switch = SW(after_fK1)
    # Second round of fK with K2
    after_fK2 = fK(after_switch, K2)
    # Inverse initial permutation
    ciphertext = inverse_IP(after_fK2)
    return ciphertext


def decrypt(ciphertext, key):
    """
    Decrypts an 8-bit ciphertext using the S-DES decryption algorithm.
    """
    # Generate subkeys
    K1, K2 = generate_subkeys(key)
    # Initial permutation
    initial_permuted = IP(ciphertext)
    # First round of fK with K2 (note the reverse order compared to encryption)
    after_fK1 = fK(initial_permuted, K2)
    # Switch function
    after_switch = SW(after_fK1)
    # Second round of fK with K1
    after_fK2 = fK(after_switch, K1)
    # Inverse initial permutation to get the plaintext
    plaintext = inverse_IP(after_fK2)
    return plaintext


# Example usage for both encryption and decryption
if __name__ == "__main__":
    plaintext = "10111101"  # Example 8-bit plaintext
    master_key = "1010000010"  # Example 10-bit key
    print("Original plaintext:", plaintext)

    # Encrypt
    ciphertext = encrypt(plaintext, master_key)
    print(f"Ciphertext: {ciphertext}")

    # Decrypt
    decrypted_text = decrypt(ciphertext, master_key)
    print(f"Decrypted text: {decrypted_text}")
