from sys import exit
from os.path import abspath, isdir, isfile, getsize
from platform import system
import argparse
from . import __version__

def cli():
    if system() != 'Windows':
        from signal import signal, SIGTSTP
        def handle_ctrl_z(signum, frame):
            print('"Ctrl + z" was pressed, closing AES-GCM File-Crypter...')
            exit()
        signal(SIGTSTP, handle_ctrl_z)
    PARSER = argparse.ArgumentParser(
        prog='aes_gcm_file_crypter'
    )
    SUB_PARSER = PARSER.add_subparsers(dest='COMMAND')
    PARSER.add_argument(
        '-v', '--version',
        action='version',
        version=f'AES-GCM File-Crypter {__version__}'
    )
    ENCRYPT_FOLDER = SUB_PARSER.add_parser(
        'encrypt_folder', 
        help='Encrypt a folder',
        epilog=f'Example: python -m aes_gcm_file_crypter encrypt_folder {abspath('/path/to/folder')} 256 Password'
    )
    KEY_SIZE_LIST = [128, 192, 256]
    ENCRYPT_FOLDER.add_argument('folder_path', help='The folder path to encrypt.')
    ENCRYPT_FOLDER.add_argument('key_size', help='An integer representing the bit size of the random key created with the user-entered password. The options are 128 (Least drive-space used), 192, or 256 (Most secure).', type=int, choices=KEY_SIZE_LIST)
    ENCRYPT_FOLDER.add_argument('password', help='A user-entered password for encryption.')
    ENCRYPT_FOLDER.add_argument('kdf_iterations', help='An optional KDF iterations integer representing the amount of times the KDF hashes the password while creating a key.', type=int, default=None, nargs='?')
    ENCRYPT_FOLDER.add_argument('block_size', help='An optional block size integer representing the amount of bytes to be read for each file chunk (Higher is faster but requires more RAM).', type=int, default=None, nargs='?')
    DECRYPT_FOLDER = SUB_PARSER.add_parser(
        'decrypt_folder', 
        help='Decrypt a folder',
        epilog=f'Example: python -m aes_gcm_file_crypter decrypt_folder {abspath('/path/to/folder')} Password'
    )
    DECRYPT_FOLDER.add_argument('folder_path', help='The folder path to decrypt.')
    DECRYPT_FOLDER.add_argument('password', help='The same user-entered password used to encrypt the folder.')
    DECRYPT_FOLDER.add_argument('kdf_iterations', help='An optional KDF iterations integer representing the amount of times the KDF hashes the password while creating a key.', type=int, default=None, nargs='?')
    DECRYPT_FOLDER.add_argument('block_size', help='An optional block size integer representing the amount of bytes to be read for each file chunk (Higher is faster but requires more RAM).', type=int, default=None, nargs='?')
    ENCRYPT_FILE = SUB_PARSER.add_parser(
        'encrypt_file', 
        help='Encrypt a file',
        epilog=f'Example: python -m aes_gcm_file_crypter encrypt_file {abspath('/path/to/file.ext')} 256 Password'
    )
    ENCRYPT_FILE.add_argument('file_path', help='The file path to encrypt.')
    ENCRYPT_FILE.add_argument('key_size', help='An integer representing the bit size of the random key created with the user-entered password, the options are 128 (Least drive-space used), 192, or 256 (Most secure).', type=int, choices=KEY_SIZE_LIST)
    ENCRYPT_FILE.add_argument('password', help='A user-chosen password for encryption.')
    ENCRYPT_FILE.add_argument('kdf_iterations', help='An optional KDF iterations integer representing the amount of times the KDF hashes the password while creating a key.', type=int, default=None, nargs='?')
    ENCRYPT_FILE.add_argument('block_size', help='An optional block size integer representing the amount of bytes to be read for each file chunk (Higher is faster but requires more RAM).', type=int, default=None, nargs='?')
    DECRYPT_FILE = SUB_PARSER.add_parser(
        'decrypt_file',
        help='Decrypt a file',
        epilog=f'Example: python -m aes_gcm_file_crypter decrypt_file {abspath('/path/to/file.ext')} Password'
    )
    DECRYPT_FILE.add_argument('file_path', help='The file path to decrypt.')
    DECRYPT_FILE.add_argument('password', help='The same user-entered password used to encrypt the file.')
    DECRYPT_FILE.add_argument('kdf_iterations', help='An optional KDF iterations integer representing the amount of times the KDF hashes the password while creating a key.', type=int, default=None, nargs='?')
    DECRYPT_FILE.add_argument('block_size', help='An optional block size integer representing the amount of bytes to be read for each file chunk (Higher is faster but requires more RAM).', type=int, default=None, nargs='?')
    ARGUMENTS = PARSER.parse_args()
    try:
        if ARGUMENTS.COMMAND == 'encrypt_folder':
            if not all([isinstance(ARGUMENTS.folder_path, str), isabs(ARGUMENTS.folder_path), isdir(ARGUMENTS.folder_path)]):
                return [f'FOLDER_PATH_DOES_NOT_EXIST!\nThe folder path parameter must be an absolute folder path string to an existing folder.\nFolder path: {ARGUMENTS.folder_path}']
            from .src.aes_gcm_crypt import recursive_files_and_bytes_total, convert_bytes, aes_gcm_encrypt_folder
            CONVERTED_BYTES_TOTAL = convert_bytes(recursive_files_and_bytes_total(ARGUMENTS.folder_path)[2])
            print(f'AES-GCM-{ARGUMENTS.key_size} encrypting a total of {CONVERTED_BYTES_TOTAL} in the folder: "{ARGUMENTS.folder_path}"\nplease wait...')
            ENCRYPT_RESULT = aes_gcm_encrypt_folder(ARGUMENTS.folder_path, ARGUMENTS.key_size, bytearray(ARGUMENTS.password, 'ascii'), ARGUMENTS.kdf_iterations, ARGUMENTS.block_size, True)
            return ENCRYPT_RESULT[1].strip()
        elif ARGUMENTS.COMMAND == 'decrypt_folder':
            if not all([isinstance(ARGUMENTS.folder_path, str), isabs(ARGUMENTS.folder_path), isdir(ARGUMENTS.folder_path)]):
                return [f'FOLDER_PATH_DOES_NOT_EXIST!\nThe folder path parameter must be an absolute folder path string to an existing folder.\nFolder path: {ARGUMENTS.folder_path}']
            from .src.aes_gcm_crypt import recursive_files_and_bytes_total, convert_bytes, aes_gcm_decrypt_folder
            CONVERTED_BYTES_TOTAL = convert_bytes(recursive_files_and_bytes_total(ARGUMENTS.folder_path)[2])
            print(f'AES-GCM decrypting a total of {CONVERTED_BYTES_TOTAL} in the folder: "{ARGUMENTS.folder_path}"\nplease wait...')
            DECRYPT_RESULT = aes_gcm_decrypt_folder(ARGUMENTS.folder_path, bytearray(ARGUMENTS.password, 'ascii'), ARGUMENTS.kdf_iterations, ARGUMENTS.block_size, True)
            return DECRYPT_RESULT[1].strip()
        elif ARGUMENTS.COMMAND == 'encrypt_file':
            if not all([isinstance(ARGUMENTS.file_path, str), isabs(ARGUMENTS.file_path), isfile(ARGUMENTS.file_path)]):
                return [f'FOLDER_PATH_DOES_NOT_EXIST!\nThe file path parameter must be an absolute file path string to an existing file.\nFile path: {ARGUMENTS.file_path}']
            from .src.aes_gcm_crypt import convert_bytes, aes_gcm_encrypt_file
            print(f'AES-GCM-{ARGUMENTS.key_size} encrypting a total of {convert_bytes(getsize(ARGUMENTS.file_path))} of data in the file: "{ARGUMENTS.file_path}"\nplease wait...')
            ENCRYPT_RESULT = aes_gcm_encrypt_file(ARGUMENTS.file_path, ARGUMENTS.key_size, bytearray(ARGUMENTS.password, 'ascii'), ARGUMENTS.kdf_iterations, ARGUMENTS.block_size)
            return ENCRYPT_RESULT[1].strip()
        elif ARGUMENTS.COMMAND == 'decrypt_file':
            if not all([isinstance(ARGUMENTS.file_path, str), isabs(ARGUMENTS.file_path), isfile(ARGUMENTS.file_path)]):
                return [f'FOLDER_PATH_DOES_NOT_EXIST!\nThe file path parameter must be an absolute file path string to an existing file.\nFile path: {ARGUMENTS.file_path}']
            from .src.aes_gcm_crypt import convert_bytes, aes_gcm_decrypt_file
            print(f'AES-GCM decrypting a total of {convert_bytes(getsize(ARGUMENTS.file_path))} of data in the file: "{ARGUMENTS.file_path}"\nplease wait...')
            DECRYPT_RESULT = aes_gcm_decrypt_file(ARGUMENTS.file_path, bytearray(ARGUMENTS.password, 'ascii'), ARGUMENTS.kdf_iterations, ARGUMENTS.block_size)
            return DECRYPT_RESULT[1].strip()
    except KeyboardInterrupt:
        return '"Ctrl + c" was pressed, closing AES-GCM File-Crypter...'
    except Exception as ERROR:
        return f'{ERROR}, closing AES-GCM File-Crypter...'

    from .aes_gcm_file_crypter import main
    main()

if __name__ == '__main__':
    CLI_RESULT = cli()
    if CLI_RESULT:
        print(CLI_RESULT)
    exit()
