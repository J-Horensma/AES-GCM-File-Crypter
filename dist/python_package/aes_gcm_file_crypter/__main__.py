from os.path import abspath
import argparse
from . import __version__

def cli():
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
    ENCRYPT_FOLDER.add_argument('folder_path', help='The folder path to encrypt.')
    ENCRYPT_FOLDER.add_argument('key_size', help='An integer representing the bit size of the random key, created with the user-chosen password, the options are 128 (Least drive-space used), 192, or 256 (Most secure).', type=int)
    ENCRYPT_FOLDER.add_argument('password', help='A user-chosen password for encryption.')
    ENCRYPT_FOLDER.add_argument('block_size', help='An optional block size integer representing the amount of bytes for each file chunk to be read (Higher is faster, but requires more RAM). The default is 65536 (Can cause errors if used incorrectly).', type=int, nargs='?', default=65536)
    DECRYPT_FOLDER = SUB_PARSER.add_parser(
        'decrypt_folder', 
        help='Decrypt a folder',
        epilog=f'Example: python -m aes_gcm_file_crypter decrypt_folder {abspath('/path/to/folder')} Password'
    )
    DECRYPT_FOLDER.add_argument('folder_path', help='The folder path to decrypt.')
    DECRYPT_FOLDER.add_argument('password', help='The same password used to encrypt the folder.')
    DECRYPT_FOLDER.add_argument('block_size', help='An optional block size integer representing the amount of bytes for each file chunk to be read (Higher is faster, but requires more RAM). The default is 65536 (Can cause errors if used incorrectly).', type=int, nargs='?', default=65536)
    ENCRYPT_FILE = SUB_PARSER.add_parser(
        'encrypt_file', 
        help='Encrypt a file',
        epilog=f'Example: python -m aes_gcm_file_crypter encrypt_file {abspath('/path/to/file.ext')} 256 Password'
    )
    ENCRYPT_FILE.add_argument('file_path', help='The file path to encrypt.')
    ENCRYPT_FILE.add_argument('key_size', help='An integer representing the bit size of the random key, created with the user-chosen password, the options are 128 (Least drive-space used), 192, or 256 (Most secure).', type=int)
    ENCRYPT_FILE.add_argument('password', help='A user-chosen password for encryption.')
    ENCRYPT_FILE.add_argument('block_size', help='An optional block size integer representing the amount of bytes for each file chunk to be read (Higher is faster, but requires more RAM). The default is 65536 (Can cause errors if used incorrectly).', type=int, nargs='?', default=65536)
    DECRYPT_FILE = SUB_PARSER.add_parser(
        'decrypt_file',
        help='Decrypt a file',
        epilog=f'Example: python -m aes_gcm_file_crypter decrypt_file {abspath('/path/to/file.ext')} Password'
    )
    DECRYPT_FILE.add_argument('file_path', help='The file path to decrypt.')
    DECRYPT_FILE.add_argument('password', help='The same password used to encrypt the file.')
    DECRYPT_FILE.add_argument('block_size', help='An optional block size integer representing the amount of bytes for each file chunk to be read (Higher is faster, but requires more RAM). The default is 65536 (Can cause errors if used incorrectly).', type=int, nargs='?', default=65536)
    ARGUMENTS = PARSER.parse_args()
    try:
        if ARGUMENTS.COMMAND == 'encrypt_folder':
            from .src.aes_gcm_crypt import aes_gcm_encrypt_folder
            print(f'AES-GCM-{ARGUMENTS.key_size} encrypting the folder: "{ARGUMENTS.folder_path}",\nplease wait...')
            ENCRYPT_RESULT = aes_gcm_encrypt_folder(ARGUMENTS.folder_path, ARGUMENTS.key_size, ARGUMENTS.password, ARGUMENTS.block_size)
            print(ENCRYPT_RESULT[1])
            return
        elif ARGUMENTS.COMMAND == 'decrypt_folder':
            from .src.aes_gcm_crypt import aes_gcm_decrypt_folder
            print(f'Decrypting the folder: "{ARGUMENTS.folder_path}",\nplease wait...')
            DECRYPT_RESULT = aes_gcm_decrypt_folder(ARGUMENTS.folder_path, ARGUMENTS.password, ARGUMENTS.block_size)
            print(DECRYPT_RESULT[1])
            return
        elif ARGUMENTS.COMMAND == 'encrypt_file':
            from .src.aes_gcm_crypt import aes_gcm_encrypt_file
            print(f'AES-GCM-{ARGUMENTS.key_size} encrypting the file: "{ARGUMENTS.file_path}",\nplease wait...')
            ENCRYPT_RESULT = aes_gcm_encrypt_file(ARGUMENTS.file_path, ARGUMENTS.key_size, ARGUMENTS.password, ARGUMENTS.block_size)
            print(ENCRYPT_RESULT[1])
            return
        elif ARGUMENTS.COMMAND == 'decrypt_file':
            from .src.aes_gcm_crypt import aes_gcm_decrypt_file
            print(f'Decrypting the file: "{ARGUMENTS.file_path}",\nplease wait...')
            DECRYPT_RESULT = aes_gcm_decrypt_file(ARGUMENTS.file_path, ARGUMENTS.password, ARGUMENTS.block_size)
            print(DECRYPT_RESULT[1])
            return
    except BaseException as ERROR:
        print(ERROR)
        return

    from .aes_gcm_file_crypter import main
    main()

if __name__ == '__main__':
    cli()
