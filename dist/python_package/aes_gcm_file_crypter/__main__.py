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
        epilog=r'Example: python -m aes_gcm_file_crypter encrypt_folder /path/to/folder 256 Password'
    )
    ENCRYPT_FOLDER.add_argument('folder_path', help='The folder path to encrypt')
    ENCRYPT_FOLDER.add_argument('key_size', type=int, help='Must be: 128 (Least drive-space used), 192, or 256 (Most secure)')
    ENCRYPT_FOLDER.add_argument('password', help='A user-chosen password used for encryption')
    DECRYPT_FOLDER = SUB_PARSER.add_parser(
        'decrypt_folder', 
        help='Decrypt a folder',
        epilog=r'Example: python -m aes_gcm_file_crypter decrypt_folder /path/to/folder Password'
    )
    DECRYPT_FOLDER.add_argument('folder_path', help='The folder path to decrypt')
    DECRYPT_FOLDER.add_argument('password', help='The same password used to encrypt the folder')
    ENCRYPT_FILE = SUB_PARSER.add_parser(
        'encrypt_file', 
        help='Encrypt a file',
        epilog=r'Example: python -m aes_gcm_file_crypter encrypt_file /path/to/file.ext 256 Password'
    )
    ENCRYPT_FILE.add_argument('file_path', help='The file path to encrypt')
    ENCRYPT_FILE.add_argument('key_size', type=int, help='Must be: 128 (Least drive-space used), 192, or 256 (Most secure)')
    ENCRYPT_FILE.add_argument('password', help='A user-chosen password used for encryption')
    DECRYPT_FILE = SUB_PARSER.add_parser(
        'decrypt_file',
        help='Decrypt a file',
        epilog=r'Example: python -m aes_gcm_file_crypter decrypt_file /path/to/file.ext Password'
    )
    DECRYPT_FILE.add_argument('file_path', help='The file path to decrypt')
    DECRYPT_FILE.add_argument('password', help='The same password used to encrypt the file')
    ARGUMENTS = PARSER.parse_args()
    if ARGUMENTS.COMMAND == 'encrypt_folder':
        from .src.aes_gcm_crypt import aes_gcm_encrypt_folder
        print(f'AES-GCM-{ARGUMENTS.key_size} encrypting the folder: "{ARGUMENTS.folder_path}",\nplease wait...')
        ENCRYPT_RESULT = aes_gcm_encrypt_folder(ARGUMENTS.folder_path, ARGUMENTS.key_size, ARGUMENTS.password)
        print(ENCRYPT_RESULT[1])
        return
    elif ARGUMENTS.COMMAND == 'decrypt_folder':
        from .src.aes_gcm_crypt import aes_gcm_decrypt_folder
        print(f'Decrypting the folder: "{ARGUMENTS.folder_path}",\nplease wait...')
        DECRYPT_RESULT = aes_gcm_decrypt_folder(ARGUMENTS.folder_path, ARGUMENTS.password)
        print(DECRYPT_RESULT[1])
        return
    elif ARGUMENTS.COMMAND == 'encrypt_file':
        from .src.aes_gcm_crypt import aes_gcm_encrypt_file
        print(f'AES-GCM-{ARGUMENTS.key_size} encrypting the file: "{ARGUMENTS.file_path}",\nplease wait...')
        ENCRYPT_RESULT = aes_gcm_encrypt_file(ARGUMENTS.file_path, ARGUMENTS.key_size, ARGUMENTS.password)
        print(ENCRYPT_RESULT[1])
        return
    elif ARGUMENTS.COMMAND == 'decrypt_file':
        from .src.aes_gcm_crypt import aes_gcm_decrypt_file
        print(f'Decrypting the file: "{ARGUMENTS.file_path}",\nplease wait...')
        DECRYPT_RESULT = aes_gcm_decrypt_file(ARGUMENTS.file_path, ARGUMENTS.password)
        print(DECRYPT_RESULT[1])
        return

    from .aes_gcm_file_crypter import main
    main()

if __name__ == '__main__':
    cli()
