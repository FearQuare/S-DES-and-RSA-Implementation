from simplified_des.sdes import generate_subkeys, encrypt, decrypt

import time


def measure_sdes_performance(plaintext):
    key_gen_times = []
    encryption_times = []
    decryption_times = []
    master_key = "1010000010"  # Example key for S-DES

    for _ in range(10):
        start_time = time.time()
        K1, K2 = generate_subkeys(master_key)
        key_gen_times.append(time.time() - start_time)

        start_time = time.time()
        ciphertext = encrypt(plaintext, master_key)
        encryption_times.append(time.time() - start_time)

        start_time = time.time()
        decrypted_message = decrypt(ciphertext, master_key)
        decryption_times.append(time.time() - start_time)

    avg_key_gen_time = sum(key_gen_times) / len(key_gen_times)
    avg_encryption_time = sum(encryption_times) / len(encryption_times)
    avg_decryption_time = sum(decryption_times) / len(decryption_times)

    print(f"S-DES Key Generation Avg Time: {avg_key_gen_time} seconds")
    print(f"S-DES Encryption Avg Time: {avg_encryption_time} seconds")
    print(f"S-DES Decryption Avg Time: {avg_decryption_time} seconds")


# Example usage for S-DES
measure_sdes_performance("10111101")
