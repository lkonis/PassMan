import filecmp
import hashlib
import os.path
import pickle
import random

import numpy.random
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def getIV(password):
    initVector = hashlib.sha256(password).digest()[:16]
    return initVector

def encrypt_file(input_file_path, output_file_path, key):
    # Generate a random initialization vector (IV).
    iv = get_random_bytes(AES.block_size)
    # Initialize the AES cipher with Cipher Block Chaining (CBC) mode.
    cipher = AES.new(key, AES.MODE_CBC, iv)

    with open(output_file_path, 'wb') as out_file:
        # write the key in the first 16 bytes
        out_file.write(iv)
        # write file size in bytes in the next 16 bytes
        file_size = os.path.getsize(input_file_path)
        chunk = file_size.to_bytes(16,byteorder='big')
        encrypted_chunk = cipher.encrypt(chunk)
        out_file.write(encrypted_chunk)
        # write tag for validation
        chunk = b'feedbeef'
        padded_chunk=pad(chunk, AES.block_size)
        encrypted_chunk = cipher.encrypt(padded_chunk)
        out_file.write(encrypted_chunk)

        # Encrypt the file chunk by chunk.
        with open(input_file_path, 'rb') as in_file:
            padding=0
            while True:
                chunk = in_file.read(16)  # Read 16 bytes at a time.
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    # Pad the last chunk if it's not a multiple of 16.
                    padding = (16 - len(chunk) % 16)
                    chunk += b' ' * padding

                encrypted_chunk = cipher.encrypt(chunk)
                out_file.write(encrypted_chunk)
        return padding

def show_message_box(text):
    # Create a QMessageBox
    msg_box = QMessageBox()

    # Set the properties of the message box
    msg_box.setWindowTitle('Information')
    msg_box.setText(text)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setStandardButtons(QMessageBox.Ok)

    # Show the message box and wait for the user's response
    response = msg_box.exec_()

    # You can handle the user's response if needed
    if response == QMessageBox.Ok:
        print('User clicked Ok')


def decrypt_file(input_file_path, output_file_path, key):
    # open and process the encrypted data file
    with open(input_file_path, 'rb') as in_file:
        # Read the IV from the beginning of the input file.
        iv = in_file.read(AES.block_size)

        # Initialize the decryption with the IV.
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # read file size
        chunk = in_file.read(16)
        decrypted_chunk = cipher.decrypt(chunk)
        filesize = int.from_bytes(decrypted_chunk, byteorder='big')

        # read the validation tag
        chunk = in_file.read(16)
        decrypted_chunk = cipher.decrypt(chunk)
        chunk = b'feedbeef'
        padded_chunk=pad(chunk, AES.block_size)

        if not decrypted_chunk==padded_chunk:
            return False

        # Create a flag to indicate if we have reached the last chunk.
        last_chunk = False
        byte_cnt = 0
        # Decrypt the file chunk by chunk.
        with open(output_file_path, 'wb') as out_file:
            while True:
                chunk = in_file.read(16)  # Read 16 bytes at a time.
                if len(chunk) == 0:
                    break
                elif len(chunk) < 16:
                    last_chunk = True

                decrypted_chunk = cipher.decrypt(chunk)

                byte_cnt += 16
                if last_chunk or byte_cnt>=filesize:
                    # Remove the padding if it's the last chunk.
                    decrypted_chunk = decrypted_chunk.rstrip(b' ')
                out_file.write(decrypted_chunk)
        return True
def compare_files(file1, file2):

    result = filecmp.cmp(file1, file2)

    if result:
        print("Files are identical.")
    else:
        print(f"{file1}, {file2}: Files are different.")

if __name__ == "__main__":
    # Generate a random encryption key (make sure to store it securely).
    encryption_key = get_random_bytes(32)

    # Paths for input, encrypted, and decrypted files.
    input_file_path = 'my_data.pkl'          # Replace with your input file path.
    encrypted_file_path = 'encrypted.bin'  # Replace with your desired encrypted file path.
    decrypted_file_path = 'decrypted.txt'  # Replace with your desired decrypted file path.

    # create random table
    in_data = numpy.random.randint(1,3, size=(2,3))
    in_data = numpy.char.mod("a%d",in_data)
    # 1. pickle data in file
    pickle.dump(in_data, open(input_file_path, "wb"))
    # 2. Encrypt the input file.
    encrypt_file(input_file_path, encrypted_file_path, encryption_key)
    print("File encrypted successfully!")

    # 3. Decrypt the encrypted file.
    decrypt_file(encrypted_file_path, decrypted_file_path, encryption_key)
    print("File decrypted successfully!")

    compare_files(input_file_path, decrypted_file_path)
    # 4. load the pickle
    unpickled = pickle.load(open(input_file_path,"rb"))
    print("input data:\n",unpickled)
    unpickled = pickle.load(open(decrypted_file_path, "rb"))
    print("input data after encryption->decryption:\n",unpickled)

