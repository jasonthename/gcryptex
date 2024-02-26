import os
import sys

def run_command(command):
    result = os.system(command)
    if result != 0:
        print("Error executing the command.")
        sys.exit(1)

def openssl_generate_keys():
    key_length = input("Enter key length (e.g., 2048, 4096): ")
    run_command(f"openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:{key_length}")
    run_command("openssl rsa -pubout -in private_key.pem -out public_key.pem")
    print("\nRSA Keys generated successfully.")

def openssl_encrypt_text():
    public_key_file = input("Enter the path to the public key file: ")
    message = input("Enter the message to encrypt: ")
    with open("message.txt", "w") as file:
        file.write(message)
    run_command(f"openssl pkeyutl -encrypt -inkey {public_key_file} -pubin -in message.txt -out message.enc")
    os.remove("message.txt")
    print("\nMessage encrypted successfully.")

def openssl_decrypt_text():
    private_key_file = input("Enter the path to the private key file: ")
    encrypted_file = input("Enter the path to the encrypted file: ")
    run_command(f"openssl pkeyutl -decrypt -inkey {private_key_file} -in {encrypted_file} -out decrypted_message.txt")
    with open("decrypted_message.txt", "r") as file:
        print("\nDecrypted Message:")
        print(file.read())

def openssl_symmetric_encrypt():
    algorithm = input("Enter the symmetric algorithm (e.g., aes-256-cbc): ")
    secret_key = os.environ.get("SYMMETRIC_KEY")
    if not secret_key:
        print("Symmetric key not set in environment. Please set the SYMMETRIC_KEY environment variable.")
        sys.exit(1)
    message = input("Enter the message to encrypt: ")
    with open("message.txt", "w") as file:
        file.write(message)
    iv = os.urandom(16)
    with open("iv.bin", "wb") as iv_file:
        iv_file.write(iv)
    run_command(f"openssl enc -{algorithm} -in message.txt -out message.enc -pbkdf2 -pass pass:{secret_key} -iv {iv.hex()}")
    os.remove("message.txt")
    print("\nMessage encrypted successfully. IV stored in iv.bin.")

def openssl_symmetric_decrypt():
    algorithm = input("Enter the symmetric algorithm (e.g., aes-256-cbc): ")
    secret_key = os.environ.get("SYMMETRIC_KEY")
    if not secret_key:
        print("Symmetric key not set in environment. Please set the SYMMETRIC_KEY environment variable.")
        sys.exit(1)
    encrypted_file = input("Enter the path to the encrypted file: ")
    with open("iv.bin", "rb") as iv_file:
        iv = iv_file.read()
    run_command(f"openssl enc -d -{algorithm} -in {encrypted_file} -out decrypted_message.txt -pbkdf2 -pass pass:{secret_key} -iv {iv.hex()}")
    with open("decrypted_message.txt", "r") as file:
        print("\nDecrypted Message:")
        print(file.read())

def main():
    print("""
 ██████╗  ██████╗██████╗ ██╗   ██╗██████╗ ████████╗███████╗██╗  ██╗
██╔════╝ ██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝
██║  ███╗██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   █████╗   ╚███╔╝ 
██║   ██║██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██╔══╝   ██╔██╗ 
╚██████╔╝╚██████╗██║  ██║   ██║   ██║        ██║   ███████╗██╔╝ ██╗
 ╚═════╝  ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝   ╚══════╝╚═╝  ╚═╝
                                                                    """)
    print("Made with <3 by @jasonthename (GitHub)")
    while True:
        print("\nMenu:")
        print("1. Generate RSA Key Pair")
        print("2. RSA Encrypt Text")
        print("3. RSA Decrypt Text")
        print("4. Symmetric Encrypt Text")
        print("5. Symmetric Decrypt Text")
        print("6. Exit")
        option = input("Enter your choice: ")

        if option == '1':
            openssl_generate_keys()
        elif option == '2':
            openssl_encrypt_text()
        elif option == '3':
            openssl_decrypt_text()
        elif option == '4':
            openssl_symmetric_encrypt()
        elif option == '5':
            openssl_symmetric_decrypt()
        elif option == '6':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()