from simplified_des.sdes import encrypt, decrypt


def test_sdes_correctness():
    # Assuming the S-DES key is predefined for simplicity; typically, it's generated.
    master_key = "1010000010"  # A sample 10-bit key.

    # Define a list of plaintexts to test the S-DES implementation.
    test_plaintexts = [
        "10101010", "00110011", "11111111", "00000000", "11001100",
        "10011001", "01101101", "10100110", "01010101", "00111100"
    ]

    for plaintext in test_plaintexts:
        # Encrypt the plaintext.
        ciphertext = encrypt(plaintext, master_key)
        # Decrypt the ciphertext.
        decrypted_text = decrypt(ciphertext, master_key)

        # Check if the decrypted text matches the original plaintext.
        assert decrypted_text == plaintext, f"Decryption failed for plaintext {plaintext}. Decrypted as {decrypted_text}"

    print("S-DES Encryption-Decryption correctness test passed for all inputs.")


# Call the test function to verify correctness of S-DES implementation.
test_sdes_correctness()
