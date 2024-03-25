from rsa.rsa import generate_rsa_keys, encrypt as rsa_encrypt, decrypt as rsa_decrypt
from simplified_des.sdes import encrypt_message as sdes_encrypt, decrypt_message as sdes_decrypt, generate_subkeys

# Step 1: RSA Key Pair Generation
alice_rsa_public, alice_rsa_private = generate_rsa_keys(1024)
bob_rsa_public, bob_rsa_private = generate_rsa_keys(1024)

# Step 2: Public Key Exchange (Simulated by having access to each other's public keys)

# Step 3: S-DES Secret Key Generation and Exchange
# Alice generates a secret key for S-DES (10 bits for simplicity)
alice_sdes_key = "1010000010"
# Alice encrypts this secret key using Bob's RSA public key
encrypted_sdes_key = rsa_encrypt(bob_rsa_public, alice_sdes_key)
# Bob decrypts the received key using his RSA private key
bob_decrypted_sdes_key = rsa_decrypt(bob_rsa_private, encrypted_sdes_key)

assert alice_sdes_key == bob_decrypted_sdes_key, "S-DES Key exchange failed"

def encode_messages_to_binary(messages):
    """
    Encodes a list of text messages to their binary representation.
    :param messages: List of strings to be encoded.
    :return: List of messages in binary (as strings of '0's and '1's).
    """
    binary_messages = []
    for message in messages:
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        binary_messages.append(binary_message)
    return binary_messages

# Step 4: Secyre Communication
messages_to_send = ["Hello Bob!", "How are you?", "I'm so tired because it's 3 am in the morning and I'm still writing this code :(."]
messages_to_send = encode_messages_to_binary(messages_to_send)
encrypted_messages = []
decrypted_messages = []

print("Alice sends encrypted messages to Bob:")
for message in messages_to_send:
    # Alice encrypts messages using the S-DES key
    encrypted_message = ''.join(sdes_encrypt(message, alice_sdes_key))
    encrypted_messages.append(encrypted_message)
    print(encrypted_message)

print("\nBob receives and decrypts the messages:")
for encrypted_message in encrypted_messages:
    # Bob decrypts the messages using the S-DES key
    decrypted_message = sdes_decrypt(encrypted_message, bob_decrypted_sdes_key)
    decrypted_messages.append(decrypted_message)

    # Ensure the binary string has full 8-bit blocks and pad if necessary
    padding = len(decrypted_message) % 8
    if padding != 0:
        decrypted_message = '0' * (8 - padding) + decrypted_message

    # Convert the binary string to ASCII text
    ascii_text = ''.join(chr(int(decrypted_message[i:i + 8], 2)) for i in range(0, len(decrypted_message), 8))
    print(ascii_text)
