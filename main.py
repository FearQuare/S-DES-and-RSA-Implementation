from rsa.rsa import generate_rsa_keys, encrypt as rsa_encrypt, decrypt as rsa_decrypt
from simplified_des.sdes import generate_master_key, generate_subkeys, encrypt_message as sdes_encrypt, decrypt_message as sdes_decrypt
from alice_and_bob import alice_bob_communication

def encode_message_to_binary(message):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    return binary_message

def main_menu():
    while True:
        print("\nCrypto Operations:")
        print("1 - Generate RSA key pair")
        print("2 - RSA Encrypt a message")
        print("3 - RSA Decrypt a message")
        print("4 - Generate S-DES key")
        print("5 - S-DES Encrypt a message")
        print("6 - S-DES Decrypt a message")
        print("7 - Simulate Alice and Bob communication scenario")
        print("0 - Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            public_key, private_key = generate_rsa_keys()
            print(f"Public Key: {public_key}\nPrivate Key: {private_key}")

        elif choice == "2":
            try:
                message = input("Enter the message to encrypt with RSA: ")
                rsa_encrypted_message = rsa_encrypt(public_key, message)
                print(f"Encrypted Message: {rsa_encrypted_message}")
            except UnboundLocalError:
                print("You need to generate the keys first!")
                continue

        elif choice == "3":
            try:
                decrypted_message = rsa_decrypt(private_key, rsa_encrypted_message)
                print(f"Decrypted Message: {decrypted_message}")
            except UnboundLocalError:
                print("You either didn't create the keys or haven't encrypted a message.")

        elif choice == "4":
            master_key = generate_master_key()
            print(master_key)
            sub_keys = generate_subkeys(master_key)
            print(f"S-DES Key 1: {sub_keys[0]}, S-DES Key 2: {sub_keys[1]}")

        elif choice == "5":
            try:
                message = input("Enter the message to encrypt with S-DES: ")
                message = encode_message_to_binary(message)
                print(message)
                encrypted_message = sdes_encrypt(message, master_key)
                print(f"Encrypted Message: {encrypted_message}")
            except UnboundLocalError:
                print("You need to generate the key first!")
                continue

        elif choice == "6":
            try:
                decrypted_message = sdes_decrypt(encrypted_message, master_key)

                padding = len(decrypted_message) % 8
                if padding != 0:
                    decrypted_message = '0' * (8 - padding) + decrypted_message

                # Convert the binary string to ASCII text
                ascii_text = ''.join(chr(int(decrypted_message[i:i + 8], 2)) for i in range(0, len(decrypted_message), 8))
                print(f"Decrypted Message: {ascii_text}")
            except UnboundLocalError:
                print("You either didn't create the keys or haven't encrypted a message.")

        elif choice == "7":
            alice_bob_communication()

        elif choice == "0":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()