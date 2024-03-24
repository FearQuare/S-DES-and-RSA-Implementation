from rsa.rsa import generate_rsa_keys, encrypt, decrypt


def test_rsa_correctness():
    public_key, private_key = generate_rsa_keys(1024)  # Using 1024-bit keys for example
    test_messages = ["Hello, RSA!", "Cryptography", "Network Security", "Encryption Test",
                     "Decryption", "OpenAI", "Python Programming", "RSA Algorithm",
                     "Simplified DES", "Test Message"]

    for message in test_messages:
        ciphertext = encrypt(public_key, message)
        decrypted_message = decrypt(private_key, ciphertext)
        assert message == decrypted_message, f"Failed on message: {message}"
    print("RSA Encryption-Decryption correctness test passed for all inputs.")


# Example usage
test_rsa_correctness()
