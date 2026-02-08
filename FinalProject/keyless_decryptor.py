import os
import crypto_engine  # Using the engine from the previous step


def recover_key_from_files(encrypted_path, original_path, key_length=64):
    """
    Recovers the XOR key by comparing an encrypted file to its original.
    Logic: Ciphertext ^ Plaintext = Key
    """
    try:
        with open(encrypted_path, 'rb') as f:
            cipher_data = f.read()
        with open(original_path, 'rb') as f:
            plain_data = f.read()

        # We only need enough bytes to cover the length of the key
        recovered_key = ""
        for i in range(key_length):
            # XOR the ciphertext byte with the original plaintext byte
            key_byte = cipher_data[i] ^ plain_data[i]
            recovered_key += chr(key_byte)

        return recovered_key
    except Exception as e:
        print(f"Error during key recovery: {e}")
        return None


# --- DEMONSTRATION FLOW ---
def run_defender_demo():
    print("--- Defender Recovery Tool ---")

    # 1. User points to an encrypted file and its original backup
    enc_file = input("Path to an ENCRYPTED file: ").strip()
    orig_file = input("Path to the ORIGINAL (backup) of that file: ").strip()

    print("Attempting to crack key via XOR Analysis...")
    cracked_key = recover_key_from_files(enc_file, orig_file)

    if cracked_key:
        print(f"\n[!] SUCCESS! Key Recovered: {cracked_key}")

        confirm = input("\nUse this key to decrypt the 'Ransomware_Test_Folder'? (y/n): ")
        if confirm.lower() == 'y':
            files = crypto_engine.get_target_files()
            for f in files:
                print(f"Recovering: {os.path.basename(f)}")
                crypto_engine.process_file_in_memory(f, cracked_key)
            print("\n[+] All files have been recovered without paying the ransom.")
    else:
        print("[-] Recovery failed. Ensure you have the correct original file.")


if __name__ == "__main__":
    run_defender_demo()