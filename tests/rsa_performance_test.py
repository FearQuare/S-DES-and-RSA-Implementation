import time

from rsa.rsa import generate_rsa_keys, decrypt, encrypt

def measure_rsa_performance(key_size, plaintext):
    key_gen_times = []
    encryption_times = []
    decryption_times = []

    for _ in range(10):
        start_time = time.time()
        public_key, private_key = generate_rsa_keys(key_size)
        key_gen_times.append(time.time() - start_time)

        ciphertext = None
        start_time = time.time()
        ciphertext = encrypt(public_key, plaintext)
        encryption_times.append(time.time() - start_time)

        start_time = time.time()
        decrypted_message = decrypt(private_key, ciphertext)
        decryption_times.append(time.time() - start_time)

    avg_key_gen_time = sum(key_gen_times) / len(key_gen_times)
    avg_encryption_time = sum(encryption_times) / len(encryption_times)
    avg_decryption_time = sum(decryption_times) / len(decryption_times)

    print(f"RSA {key_size}-bit Key Generation Avg Time: {avg_key_gen_time} seconds")
    print(f"RSA {key_size}-bit Encryption Avg Time: {avg_encryption_time} seconds")
    print(f"RSA {key_size}-bit Decryption Avg Time: {avg_decryption_time} seconds")


# Example usage
measure_rsa_performance(1024, "Hello, RSA!")
measure_rsa_performance(512, "Hello, RSA!")
measure_rsa_performance(2048, "Hello, RSA!")
