'''
Custom License With Redistribution Limitations
----------------------------------------------

"aes_gcm_crypt" Copyright © 2026 Joel Horensma

For clarity:
"Software" means the source code, in this file.
"Personal" means any use not intended for financial gain.
"Commercial" means use with product(s) and/or service(s) intended for financial gain.

This Software may be used, modified, and/or incorporated into projects for personal use.

Commercial use of this Software is allowed when:
1.) Substantial modifications and/or additions have first been incorporated into the Software (More than minor cosmetic and/or structural changes).
2.) The Software changes must be reasonably demonstratable, in the behavior, functionality, and/or structure of the running Software(s) and/or service(s).

Redistribution of the unmodified Software or a substantially unchanged copy of it, with Commercial intent and without prior written permission, is prohibited.

This copyright notice and license must be retained, precisely as-is, in all copies of the Software.
'''

from threading import local
from sys import stdout
from time import time
from io import IOBase
from os import walk, access, R_OK, W_OK, X_OK, replace, remove, fsync
from os.path import isabs, abspath, join, isdir, isfile, getsize
from functools import wraps
from platform import system
from shutil import get_terminal_size
from stat import S_ISDIR, S_ISREG
from pathlib import Path
from struct import pack, unpack
from secrets import token_bytes
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.exceptions import InvalidTag
from tkinter import ttk, Toplevel, Label

if system() == 'Windows':
    #IF USING WINDOWS, ENSURE ANSI ESCAPE CODES ARE ENABLED, IN THE TERMINAL
    from colorama import just_fix_windows_console
    just_fix_windows_console()

#ANSI ESCAPE SEQUENCES CLASS:
class ansi():
    HIDE_TERMINAL_CURSOR = '\033[?25l'
    SHOW_TERMINAL_CURSOR = '\033[?25h'
    @staticmethod
    def hide_terminal_cursor():
        stdout.write(ansi.HIDE_TERMINAL_CURSOR)
        stdout.flush()
    @staticmethod
    def show_terminal_cursor():
        stdout.write(ansi.SHOW_TERMINAL_CURSOR)
        stdout.flush()

#THIS FUNCTION:
#1.) IS A DECORATOR TO WRAP THE FUNCTIONS OF THIS LIBRARY
#AND CATCH THEIR EXCEPTIONS, SO A NEWLINE CAN BE ADDED, 
#BEFORE ERROR OUTPUT, AND THE TERMINAL CURSOR IS MADE VISIBLE AGAIN
#2.) WRAPS ANY FUNCTION WITH "@error_safe_python_progressbar_decorator" PLACED ABOVE IT
#3.) CATCHES ANY RAISED ERRORS THAT ARE NOT CAUGHT OR ARE RE-RAISED
_PROGRESSBAR_STATE = local()
def error_safe_python_progressbar_decorator(FUNCTION):
    @wraps(FUNCTION)
    def wrapper(*args, **kwargs):
        global _PROGRESSBAR_STATE
        if getattr(_PROGRESSBAR_STATE, 'active', False):
            return FUNCTION(*args, **kwargs)
        _PROGRESSBAR_STATE.active = True
        try:
            return FUNCTION(*args, **kwargs)
        except Exception as ERROR:
            _PROGRESSBAR_STATE.active = False
            if stdout is not None:
                stdout.write(f'{ERROR}')
                ansi.show_terminal_cursor()
        finally:
            #WHEN THE PYTHON PROGRESSBAR IS RUNNING AND THE OUTERMOST FUNCTION FINISHES,
            #TURN OFF THE PYTHON PROGRESSBAR AND SHOW THE TERMINAL CURSOR AGAIN
            _PROGRESSBAR_STATE.active = False
            if stdout is not None:
                ansi.show_terminal_cursor()
    return wrapper

#THIS FUNCTION:
#1.) REQUIRES:
    #A.) A FILE PATH STRING
    #B.) AN ERROR STRING
#2.) REMOVES ANY EXISTING TEMP FILE FOR THAT FILE, IN THE SAME PATH
#3.) RE-RAISES THE ERROR TO BE CAUGHT BY THE "error_safe_python_progressbar_decorator" WRAPPER
#IF THE PYTHON PROGRESSBAR IS RUNNING
@error_safe_python_progressbar_decorator
def file_processing_exception_cleanup(FILE_PATH, ERROR):
    if not isinstance(FILE_PATH, str):
        raise TypeError('[TypeError]\nFunction: "file_processing_exception_cleanup()"\nThe file path parameter must be a string type.')
    elif not isinstance(ERROR, str):
        raise TypeError('[TypeError]\nFunction: "file_processing_exception_cleanup()"\nThe error parameter must be a string type.')
    if isfile(FILE_PATH + '.tmp'): remove(FILE_PATH + '.tmp')
    if getattr(_PROGRESSBAR_STATE, 'active', False): raise ERROR

#THIS FUNCTION:
#1.) REQUIRES:
    #A.) A FILE PATH STRING
#2.) OPTIONALLY ACCEPTS:
    #A.) A BLOCK SIZE INTEGER
#3.) OVERWRITES THE FILE'S CONTENTS ON THE DISK WITH RANDOM BYTES AND
#REDUCES PLAINTEXT CHUNK DATA LEFT, IN THE RAM, WHILE DOING SO
@error_safe_python_progressbar_decorator
def wipe_file_contents(FILE_PATH, BLOCK_SIZE=None):
    if not isinstance(FILE_PATH, str):
        raise TypeError('[TypeError]\nFunction: "wipe_file_contents()"\nThe file path parameter must be a string type.')
    elif not isinstance(FILE_PATH, int):
        raise TypeError('[TypeError]\nFunction: "wipe_file_contents()"\nThe block size parameter must be an integer type.')
    try:
        FILE_PATH = abspath(FILE_PATH)
        BLOCK_SIZE = 65536 if BLOCK_SIZE is None else BLOCK_SIZE
        with open(FILE_PATH, 'r+b') as OVERWRITE_FILE:
            while True:
                #LOAD EACH PLAINTEXT CHUNK OF THE FILE BEING WIPED, AS A BYTEARRAY, 
                #SO THE PLAINTEXT CHUNK VARIABLE BUFFER CAN BE ZEROED, AFTER PROCESSING, 
                #TO REDUCE PLAINTEXT DATA REMAINING, IN THE RAM
                PLAINTEXT_CHUNK = bytearray(OVERWRITE_FILE.read(BLOCK_SIZE))
                if not PLAINTEXT_CHUNK:
                    break
                OVERWRITE_FILE.seek(-len(PLAINTEXT_CHUNK), 1)
                #RANDOM BYTES OVERWRITE EACH PLAINTEXT CHUNK OF THE FILE
                OVERWRITE_FILE.write(token_bytes(len(PLAINTEXT_CHUNK)))
                #OVERWRITE THE PLAINTEXT CHUNK VARIABLE BUFFER CONTENTS, IN THE RAM, 
                #TO ZEROED BYTES, TO PREVENT REMAINING PLAINTEXT FILE CONTENTS, IN THE RAM
                PLAINTEXT_CHUNK[:] = b'\x00' * len(PLAINTEXT_CHUNK)
                #REMOVE THE PLAINTEXT CHUNK VARIABLE BUFFER REFERENCE FROM THE RAM
                del PLAINTEXT_CHUNK
            OVERWRITE_FILE.flush()
            fsync(OVERWRITE_FILE.fileno())
    except Exception as ERROR:
        raise type(ERROR)(f'[{type(ERROR)}]\nFunction: "wipe_file_contents()"\n{ERROR if ERROR is not None and str(ERROR).strip() else 'An unknown error occurred!'}')

#THIS FUNCTION:
#1.) REQUIRES: 
    #A.) A KEY SIZE INTEGER
    #B.) A PASSWORD STRING, BYTES, OR BYTEARRAY
#2.) OPTIONALLY ACCEPTS:
    #A.) A 16 BYTE SALT BYTES
    #B.) KDF ITERATIONS INTEGER
#3.) IF A 16 BYTE SALT IS NOT SUPPLIED, ONE IS GENERATED
#4.) IF A KDF ITERATIONS INTEGER 600_000 OR HIGHER IS NOT SUPPLIED, ONE IS SET TO 600_000
#5.) A KDF-KEY IS GENERATED AS A KEY FOR AES CRYPTOGRAPHY
#6.) RETURNS A LIST CONTAINING:
    #A.) KEY BYTES
    #B.) SALT BYTES
@error_safe_python_progressbar_decorator
def get_aes_key_and_salt(KEY_SIZE, PASSWORD, SALT_BYTES=None, KDF_ITERATIONS=None):
    KEY_SIZE_LIST = [128, 192, 256]
    if not isinstance(PASSWORD, (str, bytes, bytearray)):
        raise TypeError('[TypeError]\nFunction: "get_aes_key_and_salt()"\nThe password parameter must be a string, bytes, or bytearray type.')
    elif SALT_BYTES and not isinstance(SALT_BYTES, bytes):
        raise TypeError('[TypeError]\nFunction: "get_aes_key_and_salt()"\nThe salt bytes parameter must be a bytes type.')
    elif KDF_ITERATIONS and not isinstance(KDF_ITERATIONS, int):
        raise TypeError('[TypeError]\nFunction: "get_aes_key_and_salt()"\nThe key derivation function iterations parameter must be an integer type.')
    elif KEY_SIZE not in KEY_SIZE_LIST:
        raise ValueError('[ValueError]\nFunction: "get_aes_key_and_salt()"\nThe key size parameter must be an integer type consisting of 128, 192, or 256.')
    elif SALT_BYTES and len(SALT_BYTES) != 16:
        raise ValueError('[ValueError]\nFunction: "get_aes_key_and_salt()"\nThe salt bytes parameter must be 16 bytes long.')
    elif KDF_ITERATIONS and KDF_ITERATIONS < 600_000:
        raise TypeError('[TypeError]\nFunction: "get_aes_key_and_salt()"\nThe key derivation function iterations parameter must be an integer consisting of 600000 or more.')
    else:
        try:
            KDF_ITERATIONS = 600_000 if KDF_ITERATIONS is None else KDF_ITERATIONS
            SALT_BYTES = token_bytes(16) if SALT_BYTES is None else SALT_BYTES
            #CREATE A KEY (1 BYTE = 8 BITS):
            #16 BYTES = 128 BIT, KEY LENGTH (AES-128)
            #24 BYTES = 192 BIT, KEY LENGTH (AES-192)
            #32 BYTES = 256 BIT, KEY LENGTH (AES-256)
            KEY_BYTES_LENGTH = (KEY_SIZE // 8)
            KEY_DERIVATION_FUNCTION = PBKDF2HMAC(
                algorithm=SHA256(),
                length=KEY_BYTES_LENGTH,
                salt=SALT_BYTES,
                iterations=KDF_ITERATIONS
            )
            ENCODED_PASSWORD = PASSWORD.encode() if not isinstance(PASSWORD, (bytes, bytearray)) else PASSWORD
            #THE "cryptography.hazmat.primitives.kdf.pbkdf2.PBKDF2HMAC.derive()" FUNCTION,
            #STORES THE RETURNED KEY BYTES OBJECT VALUE, IN C-SIDE BUFFERS, NOT THE RAM (MORE DIFFICULT TO INSPECT)
            KEY_BYTES = KEY_DERIVATION_FUNCTION.derive(ENCODED_PASSWORD)
            #OVERWRITE THE PASSWORD VARIABLE BUFFER CONTENTS, IN THE RAM, 
            #TO ZEROED BYTES, TO PREVENT THE PASSWORD FROM BEING STORED, IN THE RAM,
            #IF THE SUPPLIED PASSWORD IS A BYTEARRAY TYPE
            if isinstance(PASSWORD, bytearray):
                PASSWORD[:] = b'\x00' * len(PASSWORD)
            #REMOVE THE PASSWORD VARIABLE BUFFER REFERENCE FROM THE RAM
            del PASSWORD
            return [KEY_BYTES, SALT_BYTES]
        except Exception as ERROR:
            raise type(ERROR)(f'\n[{type(ERROR)}]\nFunction: "get_aes_key_and_salt()"\n{ERROR if ERROR is not None and str(ERROR).strip() else 'An unknown error occurred!'}')

#THIS FUNCTION:
#1.) REQUIRES A PATH STRING
#2.) CHECKS IF THE PATH IS A NORMAL PATH
#3.) RETURNS "True" OR "False"
@error_safe_python_progressbar_decorator
def is_normal(PATH):
    try:
        PATH = abspath(PATH)
        #CHECK IF THE PATH IS A FIFO, MOUNTPOINT, SOCKET, JUNCTION, SYMLINK, CLOUD-PLACEHOLDER, VIRTUALIZATION, DOOR, OR WHITEOUT
        PATH_STATUS = Path(PATH).lstat()
        PATH_MODE = PATH_STATUS.st_mode
        if not any([S_ISDIR(PATH_MODE), S_ISREG(PATH_MODE)]):
            return False
        elif system() == 'Windows':
            #CHECK IF THE PATH, IS A HIDDEN, SYSTEM, OR REPARSE-POINT PATH
            WINDOWS_FILE_ATTRIBUTE_HIDDEN = 0x2
            WINDOWS_FILE_ATTRIBUTE_SYSTEM = 0x4
            WINDOWS_FILE_ATTRIBUTE_REPARSE_POINT = 0x400
            WINDOWS_FILE_ATTRIBUTES = PATH_STATUS.st_file_attributes
            if WINDOWS_FILE_ATTRIBUTES & WINDOWS_FILE_ATTRIBUTE_SYSTEM:
                return False
            elif WINDOWS_FILE_ATTRIBUTES & WINDOWS_FILE_ATTRIBUTE_HIDDEN:
                return False
            elif WINDOWS_FILE_ATTRIBUTES & WINDOWS_FILE_ATTRIBUTE_REPARSE_POINT:
                return False
        return True
    except:
        return False

#THIS FUNCTION:
#1.) REQUIRES: 
    #A.) A PATH STRING
    #B.) A PERMISSION(S) STRING CONTAINING "R" (READ) "W" (WRITE) AND/OR "X" (EXECUTE)
#2.) CHECKS IF THE SUPPLIED PATH HAS THE REQUESTED PERMISSION(S)
#3.) RETURNS "True" OR "False"
@error_safe_python_progressbar_decorator
def has_permissions(PATH, PERMISSIONS):
    try:
        PATH = abspath(PATH)
        #ENSURE R, W, AND/OR X ARE INCLUDED, IN THE PERMISSIONS PARAMETER
        if not set(PERMISSIONS) <= {'R','W','X'}:
            return False
        #CHECK STATIC METADATA PERMISSIONS
        elif 'R' in PERMISSIONS and not access(PATH, R_OK):
            return False
        elif 'W' in PERMISSIONS and not access(PATH, W_OK):
            return False
        elif 'X' in PERMISSIONS and not access(PATH, X_OK):
            return False
        elif system() == 'Windows':
            #CHECK WINDOWS DYNAMIC METADATA PERMISSIONS
            from ctypes import wintypes, WinDLL
            GENERIC_READ  = 0x80000000
            FILE_SHARE_READ = 0x00000001
            FILE_SHARE_WRITE = 0x00000002
            FILE_SHARE_DELETE = 0x00000004
            OPEN_EXISTING = 3
            FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
            kernel32 = WinDLL('kernel32', use_last_error=True)
            CreateFileW = kernel32.CreateFileW
            CreateFileW.argtypes = [
                wintypes.LPCWSTR,
                wintypes.DWORD,
                wintypes.DWORD,
                wintypes.LPVOID,
                wintypes.DWORD,
                wintypes.DWORD,
                wintypes.HANDLE
            ]
            CreateFileW.restype = wintypes.HANDLE
            def can_access(PATH):
                HANDLE = CreateFileW(
                    PATH,
                    GENERIC_READ,
                    FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
                    None,
                    OPEN_EXISTING,
                    FILE_FLAG_BACKUP_SEMANTICS,
                    None
                )
                if HANDLE == wintypes.HANDLE(-1).value:
                    return False
                kernel32.CloseHandle(HANDLE)
                return True
            if not can_access(PATH):
                return False
        return True
    except:
        return False
        
#THIS FUNCTION:
#1.) REQUIRES A FOLDER PATH STRING
#2.) RECURSIVELY SCANS THE PATH
#3.) RETURNS A LIST CONTAINING:
    #A.) A FILE PATHS LIST WITH TUPLE VALUES CONTAINING: 
        #i.)"True" OR "False" FOR THE FILE PATH ACCESSABILITY STATUS
        #ii.) A FILE PATH STRING
    #B.) AN ACCESSABLE FILES TOTAL INTEGER
    #C.) AN ACCESSABLE FILES BYTES TOTAL INTEGER
@error_safe_python_progressbar_decorator
def recursive_files_and_bytes_total(FOLDER_PATH):
    if not isabs(FOLDER_PATH):
        raise ValueError('[ValueError]\nFunction: "recursive_files_and_bytes_total()"\nThe folder path parameter must be an absolute path.')
    elif not isdir(FOLDER_PATH):
        raise NotADirectoryError('[NotADirectoryError]\nFunction: "recursive_files_and_bytes_total()"\nThe folder path parameter must be a path to an existing folder.')
    try:
        FOLDER_PATH = abspath(FOLDER_PATH)
        FILES_TOTAL = 0
        BYTES_TOTAL = 0
        for ROOT, FOLDER_NAMES, FILE_NAMES in walk(FOLDER_PATH):
            FILE_PATHS = [
                (
                True if all([is_normal(join(ROOT, FILE_NAME)), has_permissions(join(ROOT, FILE_NAME), 'RW')]) else False,
                join(ROOT, FILE_NAME)
                ) 
                for FILE_NAME in FILE_NAMES
            ]
            for FILE_PATH in FILE_PATHS:
                if FILE_PATH[0]:
                    FILES_TOTAL += 1
                    BYTES_TOTAL += getsize(FILE_PATH[1])
        return FILE_PATHS, FILES_TOTAL, BYTES_TOTAL
    except Exception as ERROR:
        raise type(ERROR)(f'[{type(ERROR)}]\nFunction: "recursive_files_and_bytes_total()"\n{ERROR if ERROR is not None and str(ERROR).strip() else 'An unknown error occurred!'}')

#THIS FUNCTION:
#1.) REQUIRES:
    #A.) A BYTES NUMBER STRING OR INTEGER
#2.) CONVERTS THE SUPPLIED BYTES NUMBER
#3.) RETURNS THE CONVERTED BYTES AS A STRING
@error_safe_python_progressbar_decorator
def convert_bytes(BYTES_NUMBER):
    if not isinstance(BYTES_NUMBER, (str, int)):
        raise TypeError('[TypeError]\nFunction: "convert_bytes()"\nThe bytes number parameter must be a string or integer type.')
    try:
        BINARY_INCREMENT = 1024
        if BYTES_NUMBER < BINARY_INCREMENT:return f'{BYTES_NUMBER} Bytes'
        KILOBYTES = f'{round(BYTES_NUMBER/BINARY_INCREMENT, 2)}'
        if BYTES_NUMBER >= BINARY_INCREMENT and BYTES_NUMBER < (BINARY_INCREMENT ** 2):return f'{KILOBYTES} KB'
        MEGABYTES = round(BYTES_NUMBER/(BINARY_INCREMENT ** 2), 2)
        if BYTES_NUMBER >= (BINARY_INCREMENT ** 2) and BYTES_NUMBER < BINARY_INCREMENT ** 3:return f'{MEGABYTES} MB'
        GIGABYTES = round(BYTES_NUMBER/(BINARY_INCREMENT ** 3), 2)
        if BYTES_NUMBER >= (BINARY_INCREMENT ** 3) and BYTES_NUMBER < BINARY_INCREMENT ** 4:return f'{GIGABYTES} GB'
        TERABYTES = round(BYTES_NUMBER/(BINARY_INCREMENT ** 4), 2)
        if BYTES_NUMBER >= (BINARY_INCREMENT ** 4) and BYTES_NUMBER < BINARY_INCREMENT ** 5:return f'{TERABYTES} TB'
        PETABYTES = round(BYTES_NUMBER/(BINARY_INCREMENT ** 5), 2)
        if BYTES_NUMBER >= (BINARY_INCREMENT ** 5) and BYTES_NUMBER < BINARY_INCREMENT ** 6:return f'{PETABYTES} PB'
        EXABYTES = round(BYTES_NUMBER/(BINARY_INCREMENT ** 6), 2)
        if BYTES_NUMBER >= (BINARY_INCREMENT ** 6) and BYTES_NUMBER < BINARY_INCREMENT ** 7:return f'{EXABYTES} EB'
        ZETTABYTES = round(BYTES_NUMBER/(BINARY_INCREMENT ** 7), 2)
        if BYTES_NUMBER >= (BINARY_INCREMENT ** 7) and BYTES_NUMBER < BINARY_INCREMENT ** 8:return f'{ZETTABYTES} ZB'
    except Exception as ERROR:
        raise type(ERROR)(f'[{type(ERROR)}]\nFunction: "convert_bytes()"\n{ERROR if ERROR is not None and str(ERROR).strip() else 'An unknown error occurred!'}')

#THIS FUNCTION:
#1.) REQUIRES:
    #A.) A SECONDS INTEGER OR FLOAT
#2.) CONVERTS THE SUPPLIED SECONDS
#3.) RETURNS A CONVERTED SECONDS STRING
@error_safe_python_progressbar_decorator
def convert_seconds(SECONDS):
    if not isinstance(SECONDS, (int, float)):
        raise TypeError('[TypeError]\nFunction: "convert_seconds()"\nThe seconds parameter must be an integer or float type.')
    try:
        YEARS = f'{round((SECONDS // 31536000))}y:' if SECONDS // 31536000 > 0 else ''; REMAINDER_SECONDS = SECONDS % 31536000
        MONTHS = f'{round((REMAINDER_SECONDS // 2628000))}M:' if REMAINDER_SECONDS // 2628000 > 0 else ''; REMAINDER_SECONDS %= 2628000
        WEEKS = f'{round((REMAINDER_SECONDS // 604800))}w:' if REMAINDER_SECONDS // 604800 > 0 else ''; REMAINDER_SECONDS %= 604800
        DAYS = f'{round((REMAINDER_SECONDS // 86400))}d:' if REMAINDER_SECONDS // 86400 > 0 else ''; REMAINDER_SECONDS %= 86400
        HOURS = f'{round((REMAINDER_SECONDS // 3600))}h:' if REMAINDER_SECONDS // 3600 > 0 else ''; REMAINDER_SECONDS %= 3600
        MINUTES = f'{round((REMAINDER_SECONDS // 60))}m:' if REMAINDER_SECONDS // 60 > 0 else ''; REMAINDER_SECONDS %= 60
        SECONDS = f'{round((REMAINDER_SECONDS % 60))}s'
        CONVERTED_SECONDS = f'{YEARS}{MONTHS}{WEEKS}{DAYS}{HOURS}{MINUTES}{SECONDS}'
        return CONVERTED_SECONDS
    except Exception as ERROR:
        raise type(ERROR)(f'[{type(ERROR)}]\nFunction: "convert_seconds()"\n{ERROR if ERROR is not None and str(ERROR).strip() else 'An unknown error occurred!'}')

#THIS FUNCTION:
#1.) REQUIRES:
    #A.) A TOTAL INTEGER
    #B.) A START TIME FLOAT
    #C.) A PROCESSED INTEGER
#2.) DISPLAYS A PROGRESSBAR, IN THE TERMINAL, WITH THE SUPPLIED VALUES
@error_safe_python_progressbar_decorator
def python_progressbar(TOTAL, START_TIME, PROCESSED):
    if not isinstance(TOTAL, int):
        raise TypeError('[TypeError]\nFunction: "python_progressbar()"\nThe total parameter must be an integer type.')
    elif not isinstance(TOTAL, float):
        raise TypeError('[TypeError]\nFunction: "python_progressbar()"\nThe start time parameter must be a float type.')
    elif not isinstance(TOTAL, int):
        raise TypeError('[TypeError]\nFunction: "python_progressbar()"\nThe processed parameter must be an integer type.')
    PERCENT_COMPLETE = 0
    try:
        #CALCULATE PROGRESS
        TERMINAL_WIDTH = get_terminal_size((80, 20)).columns
        PROGRESSBAR_WIDTH = min(30, TERMINAL_WIDTH - 20)
        PERCENT_COMPLETE = (PROCESSED / TOTAL) * 100
        ELAPSED_SECONDS = max(time() - START_TIME, 0.001)
        PROCESSED_PER_SECOND = PROCESSED / ELAPSED_SECONDS
        REMAINING = TOTAL - PROCESSED
        ETA_SECONDS = REMAINING / PROCESSED_PER_SECOND
        PROGRESSBAR_FILLED = int(PROGRESSBAR_WIDTH * PROCESSED / TOTAL)
        PROGRESSBAR = '█' * PROGRESSBAR_FILLED + '-' * (PROGRESSBAR_WIDTH - PROGRESSBAR_FILLED)
        stdout.write(f'\r[{PROGRESSBAR}] {PERCENT_COMPLETE:1.0f}% ETA: {convert_seconds(ETA_SECONDS)}')
        stdout.flush()
    except Exception as ERROR:
        raise type(ERROR)(f'[{type(ERROR)}]\nFunction: "python_progressbar()"\n{ERROR if ERROR is not None and str(ERROR).strip() else 'An unknown error occurred!'}')
    finally:
        if PERCENT_COMPLETE >= 100:
            stdout.write('\n')
            ansi.show_terminal_cursor()

#THIS FUNCTION:
#1.) REQUIRES:
    #A.) A FILE OBJECT OPENED, IN BINARY READ MODE
#2.) CHECKS FOR AES-GCM HEADERS, IN THE FILE
#3.) RETURNS THE HEADERS AS A LIST OR "None" WITH ERROR INFORMATION
@error_safe_python_progressbar_decorator
def check_aes_gcm_headers(FILE):
    if not isinstance(FILE, IOBase) or 'r' not in FILE.mode or 'b' not in FILE.mode:
        raise TypeError('[TypeError]\nFunction: "check_aes_gcm_headers()"\nThe file parameter must be a file object, in binary read mode.')
    else:
        try:
            TOTAL_HEADERS_SIZE = 0
            #READ THE HEADER SIZE DATA (FIRST 4 BYTES OF EVERY AES-GCM ENCRYPTION HEADER, ENCODED INTO BIG ENDIAN BINARY BYTES)
            ALGORITHM_AND_MODE_HEADER_SIZE_DATA = FILE.read(4)
            #CHECK IF THE FILE IS EMPTY, BY CHECKING FOR THE FIRST AES-GCM ENCRYPTION HEADER'S SIZE DATA
            if len(ALGORITHM_AND_MODE_HEADER_SIZE_DATA) == 0:
                FILE.seek(0); return [None, 'FILE_EMPTY']
            #THE "aes_gcm_encrypt_file()" FUNCTION, WRITES HEADERS TO AES-GCM ENCRYPTED FILES, IN THE FORMAT: 
            #4 BYTES (CONTAINING BIG ENDIAN BINARY ENCODED HEADER SIZE DATA) + HEADER BYTES
            #LESS THAN 4 BYTES, MEANS THE HEADER SIZE DATA, IS TRUNCATED 
            if len(ALGORITHM_AND_MODE_HEADER_SIZE_DATA) != 4:
                FILE.seek(0); return [None, 'ALGORITHM_AND_MODE_HEADER_SIZE_TRUNCATED']
            #CONVERT THE HEADER SIZE DATA, FROM BIG ENDIAN BINARY ENCODED, TO AN INTEGER, REPRESENTING THE BYTES LENGTH OF THE HEADER
            (ALGORITHM_AND_MODE_HEADER_SIZE,) = unpack('>I', ALGORITHM_AND_MODE_HEADER_SIZE_DATA)
            #READ THE LENGTH OF THE HEADER
            ALGORITHM_AND_MODE_HEADER = FILE.read(ALGORITHM_AND_MODE_HEADER_SIZE)
            #CHECK IF THE FILE, IS AES-GCM ENCRYPTED
            if ALGORITHM_AND_MODE_HEADER != b'AES-GCM':
                FILE.seek(0); return [None, 'NOT_AES-GCM_ENCRYPTED']
            #CHECK IF THE HEADER, IS CORRUPTED
            elif ALGORITHM_AND_MODE_HEADER_SIZE != len(ALGORITHM_AND_MODE_HEADER):
                FILE.seek(0); return [None, 'ALGORITHM_AND_MODE_HEADER_CORRUPTED']
            #UPDATE THE TOTAL HEADERS SIZE VARIABLE, REPRESENTING THE TOTAL BYTES LENGTH OF ALL THE AES-GCM ENCRYPTION HEADERS
            TOTAL_HEADERS_SIZE += 4 + ALGORITHM_AND_MODE_HEADER_SIZE
            KEY_SIZE_HEADER_SIZE_DATA = FILE.read(4)
            if len(KEY_SIZE_HEADER_SIZE_DATA) != 4:
                FILE.seek(0); return [None, 'KEY_SIZE_HEADER_SIZE_TRUNCATED']
            (KEY_SIZE_HEADER_SIZE,) = unpack('>I', KEY_SIZE_HEADER_SIZE_DATA)
            KEY_SIZE_HEADER = FILE.read(KEY_SIZE_HEADER_SIZE)
            TOTAL_HEADERS_SIZE += 4 + KEY_SIZE_HEADER_SIZE
            NONCE_BYTES_HEADER_SIZE_DATA = FILE.read(4)
            if len(NONCE_BYTES_HEADER_SIZE_DATA) != 4:
                FILE.seek(0); return [None, 'NONCE_BYTES_HEADER_SIZE_TRUNCATED']
            (NONCE_BYTES_HEADER_SIZE,) = unpack('>I', NONCE_BYTES_HEADER_SIZE_DATA)
            NONCE_BYTES_HEADER = FILE.read(NONCE_BYTES_HEADER_SIZE)
            if NONCE_BYTES_HEADER_SIZE != len(NONCE_BYTES_HEADER) or len(NONCE_BYTES_HEADER) != 12:
                FILE.seek(0); return [None, 'NONCE_BYTES_HEADER_CORRUPTED']
            TOTAL_HEADERS_SIZE += 4 + NONCE_BYTES_HEADER_SIZE
            TAG_BYTES_HEADER_SIZE_DATA = FILE.read(4)
            if len(TAG_BYTES_HEADER_SIZE_DATA) != 4:
                FILE.seek(0); return [None, 'TAG_BYTES_HEADER_SIZE_TRUNCATED']
            (TAG_BYTES_HEADER_SIZE,) = unpack('>I', TAG_BYTES_HEADER_SIZE_DATA)
            TAG_BYTES_HEADER = FILE.read(TAG_BYTES_HEADER_SIZE)
            if TAG_BYTES_HEADER_SIZE != len(TAG_BYTES_HEADER) or len(TAG_BYTES_HEADER) != 16:
                FILE.seek(0); return [None, 'TAG_BYTES_HEADER_CORRUPTED']
            TOTAL_HEADERS_SIZE += 4 + TAG_BYTES_HEADER_SIZE
            SALT_BYTES_HEADER_SIZE_DATA = FILE.read(4)
            if len(SALT_BYTES_HEADER_SIZE_DATA) != 4:
                FILE.seek(0); return [None, 'SALT_BYTES_HEADER_SIZE_TRUNCATED']
            (SALT_BYTES_HEADER_SIZE,) = unpack('>I', SALT_BYTES_HEADER_SIZE_DATA)
            SALT_BYTES_HEADER = FILE.read(SALT_BYTES_HEADER_SIZE)
            if SALT_BYTES_HEADER_SIZE != len(SALT_BYTES_HEADER) or len(SALT_BYTES_HEADER) != 16:
                FILE.seek(0); return [None, 'SALT_BYTES_HEADER_CORRUPTED']
            TOTAL_HEADERS_SIZE += 4 + SALT_BYTES_HEADER_SIZE
            if TOTAL_HEADERS_SIZE != 74:
                FILE.seek(0); return [None, 'UNEXPECTED_TOTAL_HEADERS_SIZE']
            FILE.seek(0); return [ALGORITHM_AND_MODE_HEADER.decode(), int(KEY_SIZE_HEADER.decode()), NONCE_BYTES_HEADER, TAG_BYTES_HEADER, SALT_BYTES_HEADER, TOTAL_HEADERS_SIZE]
        except Exception as ERROR:
            raise type(ERROR)(f'[{type(ERROR)}]\nFunction: "check_aes_gcm_headers()"\n{ERROR if ERROR is not None and str(ERROR).strip() else 'An unknown error occurred!'}')
        
#THIS FUNCTION:
#1.) REQUIRES:
    #A.) A FOLDER PATH STRING
    #B.) A KEY SIZE INTEGER
    #C.) A PASSWORD STRING, BYTES, OR BYTEARRAY
#2.) OPTIONALLY ACCEPTS:
    #A.) A KDF ITERATIONS INTEGER
    #B.) A BLOCK SIZE INTEGER (DEFAULT IS 65536)
    #C.) A PYTHON PROGRESSBAR BOOL FOR DISPLAYING A PROGRESSBAR, IN A TERMINAL (DEFAULT IS "False")
    #D.) A "tkinter.Toplevel()" CLASS (FOR A GUI PROGRESSBAR WINDOW)
    #E.) A "tkinter.Label()" CLASS (FOR ETA, IN THE GUI PROGRESSBAR WINDOW)
    #F.) A "ttk.Progressbar()" CLASS (FOR THE PROGRESSBAR WINDOW, PROGRESSBAR)
    #G.) A "tkinter.Label()" CLASS (FOR PERCENTAGE, IN THE GUI PROGRESSBAR WINDOW)
#3.) RECURSIVELY AES-GCM ENCRYPTS ALL FILES, WITHIN THE FOLDER PATH (SECURELY, FOR ANY FILE TYPE)
#4.) RETURNS A LIST CONTAINING:
    #A.) "True" (SUCCESS) or "False" (ERROR)
    #B.) ANY INFO
@error_safe_python_progressbar_decorator
def aes_gcm_encrypt_folder(
        FOLDER_PATH, KEY_SIZE, PASSWORD, KDF_ITERATIONS=None, 
        BLOCK_SIZE=None, PYTHON_PROGRESSBAR=False, TKINTER_PROGRESSBAR_WINDOW=None, TKINTER_PROGRESSBAR_MESSAGE=None, 
        TKINTER_PROGRESSBAR=None, TKINTER_PROGRESSBAR_PERCENTAGE=None
    ):
    KEY_SIZE_LIST = [128, 192, 256]
    if not isinstance(FOLDER_PATH, str):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_folder()"\nThe folder path parameter must be a string type.')
    elif not isinstance(PASSWORD, (str, bytes, bytearray)):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_folder()"\nThe password parameter must be a string, bytes, or bytearray type.')
    elif KDF_ITERATIONS and not isinstance(KDF_ITERATIONS, int):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_folder()"\nThe key derivation function iterations parameter must be an integer type.')
    elif BLOCK_SIZE and not isinstance(BLOCK_SIZE, int):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_folder()"\nThe block size parameter must be an integer type.')
    elif PYTHON_PROGRESSBAR and not isinstance(PYTHON_PROGRESSBAR, bool):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_folder()"\nThe python progressbar parameter must be a bool type.')
    elif TKINTER_PROGRESSBAR_WINDOW and not isinstance(TKINTER_PROGRESSBAR_WINDOW, Toplevel):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_folder()"\nThe tkinter progressbar window parameter must be a "tkinter.Toplevel()" type.')
    elif TKINTER_PROGRESSBAR_MESSAGE and not isinstance(TKINTER_PROGRESSBAR_MESSAGE, Label):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_folder()"\nThe tkinter progressbar message parameter must be a "tkinter.Label()" type.')
    elif TKINTER_PROGRESSBAR and not isinstance(TKINTER_PROGRESSBAR, ttk.Progressbar):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_folder()"\nThe tkinter progressbar parameter must be a "ttk.Progressbar()" type.')
    elif TKINTER_PROGRESSBAR_PERCENTAGE and not isinstance(TKINTER_PROGRESSBAR_PERCENTAGE, Label):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_folder()"\nThe tkinter progressbar percentage parameter must be a "tkinter.Label()" type.')
    elif not isabs(FOLDER_PATH):
        raise ValueError('[ValueError]\nFunction: "aes_gcm_encrypt_folder()"\nThe folder path parameter must be an absolute path.')
    elif not isdir(FOLDER_PATH):
        raise NotADirectoryError('[NotADirectoryError]\nFunction: "aes_gcm_encrypt_folder()"\nThe folder path parameter must be a path to an existing folder.')
    elif KEY_SIZE not in KEY_SIZE_LIST:
        raise ValueError('[ValueError]\nFunction: "aes_gcm_encrypt_folder()"\nThe key size parameter must be an integer type consisting of 128, 192, or 256.')
    elif any([TKINTER_PROGRESSBAR_WINDOW, TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE]) and not all([TKINTER_PROGRESSBAR_WINDOW, TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE]):
        raise ValueError('[ValueError]\nFunction: "aes_gcm_encrypt_folder()"\nWhen using a tkinter progressbar with this function, all 4 optional tkinter classes must be supplied.')
    try:
        FOLDER_PATH = abspath(FOLDER_PATH)
        BLOCK_SIZE = 65536 if BLOCK_SIZE is None else BLOCK_SIZE
        ERRORS = []
        if PYTHON_PROGRESSBAR or all([TKINTER_PROGRESSBAR_WINDOW, TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE]):
            FILE_PATHS, FILES_TOTAL, BYTES_TOTAL = recursive_files_and_bytes_total(FOLDER_PATH)
            START_TIME = time()
            PROCESSED_FOLDER_BYTES_TOTAL = 0
        else:
            FILE_PATHS = recursive_files_and_bytes_total(FOLDER_PATH)[0]
            BYTES_TOTAL = None
            START_TIME = None
            PROCESSED_FOLDER_BYTES_TOTAL = None
        for FILE_PATH in FILE_PATHS:
            if FILE_PATH[0]:
                ENCRYPT_RESULT = aes_gcm_encrypt_file(FILE_PATH[1], KEY_SIZE, PASSWORD, KDF_ITERATIONS, BLOCK_SIZE, BYTES_TOTAL, START_TIME, PYTHON_PROGRESSBAR, TKINTER_PROGRESSBAR_WINDOW, TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE, PROCESSED_FOLDER_BYTES_TOTAL)
                if not ENCRYPT_RESULT[0]:
                    ERRORS += ENCRYPT_RESULT[1].splitlines()
                if PROCESSED_FOLDER_BYTES_TOTAL is not None:
                    PROCESSED_FOLDER_BYTES_TOTAL = ENCRYPT_RESULT[2]
        if ERRORS:
            ERRORS = '\n'.join(ERRORS) + '\n'
        #OVERWRITE THE PASSWORD VARIABLE BUFFER CONTENTS, IN THE RAM, 
        #TO ZEROED BYTES, TO PREVENT THE PASSWORD FROM BEING STORED, IN THE RAM,
        #IF THE SUPPLIED PASSWORD IS A BYTEARRAY TYPE
        if isinstance(PASSWORD, bytearray):
            PASSWORD[:] = b'\x00' * len(PASSWORD)
        #REMOVE THE PASSWORD VARIABLE BUFFER REFERENCE FROM THE RAM
        del PASSWORD
        if getattr(_PROGRESSBAR_STATE, 'active', False):
            stdout.write('\n')
            ansi.show_terminal_cursor()
        return [True if not ERRORS else False, f'{ERRORS if ERRORS else ''}\nAES-GCM-{KEY_SIZE}_FOLDER_ENCRYPTION_COMPLETE!\nFolder path: {FOLDER_PATH}']
    except Exception as ERROR:
        if getattr(_PROGRESSBAR_STATE, 'active', False): raise ERROR
        return [False, f'[{type(ERROR)}]\nFunction: "aes_gcm_encrypt_folder()"\n{ERROR if ERROR is not None and str(ERROR).strip() else 'An unknown error occurred!'}\nFolder path: {FOLDER_PATH}']

#THIS FUNCTION:
#1.) REQUIRES:
    #A.) A FOLDER PATH STRING
    #B.) A PASSWORD STRING, BYTES, OR BYTEARRAY
#2.) OPTIONALLY ACCEPTS:
    #A.) A KDF ITERATIONS INTEGER
    #B.) A BLOCK SIZE INTEGER (DEFAULT IS 65536)
    #C.) A PYTHON PROGRESSBAR BOOL FOR DISPLAYING A PROGRESSBAR, IN A TERMINAL (DEFAULT IS "False")
    #D.) A "tkinter.Toplevel()" CLASS (FOR A GUI PROGRESSBAR WINDOW)
    #E.) A "tkinter.Label()" CLASS (FOR ETA, IN THE GUI PROGRESSBAR WINDOW)
    #F.) A "ttk.Progressbar()" CLASS (FOR THE PROGRESSBAR WINDOW, PROGRESSBAR)
    #G.) A "tkinter.Label()" CLASS (FOR PERCENTAGE, IN THE GUI PROGRESSBAR WINDOW)
#3.) RECURSIVELY AES-GCM DECRYPTS ALL FILES, WITHIN THE FOLDER PATH (IF THE SUPPLIED PASSWORD IS CORRECT)
#4.) RETURNS A LIST CONTAINING:
    #A.) "True" (SUCCESS) or "False" (ERROR)
    #B.) ANY INFO
@error_safe_python_progressbar_decorator
def aes_gcm_decrypt_folder(
        FOLDER_PATH, PASSWORD, KDF_ITERATIONS=None, BLOCK_SIZE=None, 
        PYTHON_PROGRESSBAR=False, TKINTER_PROGRESSBAR_WINDOW=None, TKINTER_PROGRESSBAR_MESSAGE=None, TKINTER_PROGRESSBAR=None, 
        TKINTER_PROGRESSBAR_PERCENTAGE=None
    ):
    if not isinstance(FOLDER_PATH, str):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_folder()"\nThe folder path parameter must be a string type.')
    elif not isinstance(PASSWORD, (str, bytes, bytearray)):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_folder()"\nThe password parameter must be a string, bytes, or bytearray type.')
    elif KDF_ITERATIONS and not isinstance(KDF_ITERATIONS, int):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_folder()"\nThe key derivation function iterations parameter must be an integer type.')
    elif BLOCK_SIZE and not isinstance(BLOCK_SIZE, int):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_folder()"\nThe block size parameter must be an integer type.')
    elif PYTHON_PROGRESSBAR and not isinstance(PYTHON_PROGRESSBAR, bool):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_folder()"\nThe python progressbar parameter must be a bool type.')
    elif TKINTER_PROGRESSBAR_WINDOW and not isinstance(TKINTER_PROGRESSBAR_WINDOW, Toplevel):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_folder()"\nThe tkinter progressbar window parameter must be a "tkinter.Toplevel()" type.')
    elif TKINTER_PROGRESSBAR_MESSAGE and not isinstance(TKINTER_PROGRESSBAR_MESSAGE, Label):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_folder()"\nThe tkinter progressbar message parameter must be a "tkinter.Label()" type.')
    elif TKINTER_PROGRESSBAR and not isinstance(TKINTER_PROGRESSBAR, ttk.Progressbar):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_folder()"\nThe tkinter progressbar parameter must be a "ttk.Progressbar()" type.')
    elif TKINTER_PROGRESSBAR_PERCENTAGE and not isinstance(TKINTER_PROGRESSBAR_PERCENTAGE, Label):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_folder()"\nThe tkinter progressbar percentage parameter must be a "tkinter.Label()" type.')
    elif not isabs(FOLDER_PATH):
        raise ValueError('[ValueError]\nFunction: "aes_gcm_decrypt_folder()"\nThe folder path parameter must be an absolute path.')
    elif not isdir(FOLDER_PATH):
        raise NotADirectoryError('[NotADirectoryError]\nFunction: "aes_gcm_decrypt_folder()"\nThe folder path parameter must be a path to an existing folder.')
    elif any([TKINTER_PROGRESSBAR_WINDOW, TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE]) and not all([TKINTER_PROGRESSBAR_WINDOW, TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE]):
        raise ValueError('[ValueError]\nFunction: "aes_gcm_decrypt_folder()"\nWhen using a tkinter progressbar with this function, all 4 optional tkinter classes must be supplied.')
    try:
        FOLDER_PATH = abspath(FOLDER_PATH)
        BLOCK_SIZE = 65536 if BLOCK_SIZE is None else BLOCK_SIZE
        ERRORS = []
        if PYTHON_PROGRESSBAR or all([TKINTER_PROGRESSBAR_WINDOW, TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE]):
            FILE_PATHS, FILES_TOTAL, BYTES_TOTAL = recursive_files_and_bytes_total(FOLDER_PATH)
            START_TIME = time()
            PROCESSED_FOLDER_BYTES_TOTAL = 0
        else:
            FILE_PATHS = recursive_files_and_bytes_total(FOLDER_PATH)[0]
            BYTES_TOTAL = None
            START_TIME = None
            PROCESSED_FOLDER_BYTES_TOTAL = None
        for FILE_PATH in FILE_PATHS:
            if FILE_PATH[0]:
                DECRYPT_RESULT = aes_gcm_decrypt_file(FILE_PATH[1], PASSWORD, KDF_ITERATIONS, BLOCK_SIZE, BYTES_TOTAL, START_TIME, PYTHON_PROGRESSBAR, TKINTER_PROGRESSBAR_WINDOW, TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE, PROCESSED_FOLDER_BYTES_TOTAL)
                if not DECRYPT_RESULT[0]: 
                    ERRORS += DECRYPT_RESULT[1].splitlines()
                if PROCESSED_FOLDER_BYTES_TOTAL is not None:
                    PROCESSED_FOLDER_BYTES_TOTAL = DECRYPT_RESULT[2]
        if ERRORS:
            ERRORS = '\n'.join(ERRORS) + '\n'
        #OVERWRITE THE PASSWORD VARIABLE BUFFER CONTENTS, IN THE RAM, 
        #TO ZEROED BYTES, TO PREVENT THE PASSWORD FROM BEING STORED, IN THE RAM,
        #IF THE SUPPLIED PASSWORD IS A BYTEARRAY TYPE
        if isinstance(PASSWORD, bytearray):
            PASSWORD[:] = b'\x00' * len(PASSWORD)
        #REMOVE THE PASSWORD VARIABLE BUFFER REFERENCE FROM THE RAM
        del PASSWORD
        if getattr(_PROGRESSBAR_STATE, 'active', False):
            _PROGRESSBAR_STATE.active = False
            stdout.write('\n')
            ansi.show_terminal_cursor()
        return [True if not ERRORS else False, f'{ERRORS if ERRORS else ''}\nAES-GCM_FOLDER_DECRYPTION_COMPLETE!\nFolder path: {FOLDER_PATH}']
    except Exception as ERROR:
        if getattr(_PROGRESSBAR_STATE, 'active', False): raise ERROR
        return [False, f'[{type(ERROR)}]\nFunction: "aes_gcm_decrypt_folder()"\n{ERROR if ERROR is not None and str(ERROR).strip() else 'An unknown error occurred!'}\nFolder path: {FOLDER_PATH}']

#THIS FUNCTION:
#1.) REQUIRES:
    #A.) A FILE PATH STRING
    #B.) A KEY SIZE INTEGER
    #C.) A PASSWORD STRING, BYTES, OR BYTEARRAY
#2.) OPTIONALLY ACCEPTS: 
    #A.) A KDF ITERATIONS INTEGER
    #B.) A BLOCK SIZE INTEGER (DEFAULT IS 65536)
    #C.) A BYTES_TOTAL INTEGER (FOR CALCULATING ETA, IN THE PYTHON AND/OR GUI PROGRESSBAR OF THE "aes_gcm_encrypt_folder()" FUNCTION)
    #D.) A START TIME FLOAT (FOR CALCULATING ETA, IN THE PYTHON AND/OR GUI PROGRESSBAR OF THE "aes_gcm_encrypt_folder()" FUNCTION)
    #E.) A PYTHON PROGRESSBAR BOOL FOR DISPLAYING A PROGRESSBAR, IN A TERMINAL (DEFAULT IS "False")
    #F.) A "tkinter.Toplevel()" CLASS (FOR A GUI PROGRESSBAR WINDOW)
    #G.) A "tkinter.Label()" CLASS (FOR ETA, IN THE GUI PROGRESSBAR WINDOW)
    #H.) A "ttk.Progressbar()" CLASS (FOR THE PROGRESSBAR WINDOW, PROGRESSBAR)
    #I.) A "tkinter.Label()" CLASS (FOR PERCENTAGE, IN THE GUI PROGRESSBAR WINDOW)
    #J.) A PROCESSED FOLDER BYTES TOTAL INTEGER (FOR CALCULATING ETA, IN THE PYTHON AND/OR GUI PROGRESSBAR OF THE "aes_gcm_encrypt_folder()" FUNCTION)
#3.) AES-GCM ENCRYPTS THE FILE (SECURELY, FOR ANY FILE TYPE)
#4.) RETURNS A LIST CONTAINING:
    #A.) "True" (SUCCESS) or "False" (ERROR)
    #B.) ANY INFO
    #C.) A PROCESSED FOLDER BYTES TOTAL INTEGER (FOR CALCULATING ETA, IN A PROGRESSBAR, OF THE "aes_gcm_encrypt_folder()" FUNCTION)
@error_safe_python_progressbar_decorator
def aes_gcm_encrypt_file(
        FILE_PATH, KEY_SIZE, PASSWORD, KDF_ITERATIONS=None, 
        BLOCK_SIZE=None, BYTES_TOTAL=None, START_TIME=None, PYTHON_PROGRESSBAR=False, 
        TKINTER_PROGRESSBAR_WINDOW=None, TKINTER_PROGRESSBAR_MESSAGE=None, TKINTER_PROGRESSBAR=None, TKINTER_PROGRESSBAR_PERCENTAGE=None, 
        PROCESSED_FOLDER_BYTES_TOTAL=None
    ):
    KEY_SIZE_LIST = [128, 192, 256]
    if not isinstance(FILE_PATH, str):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_file()"\nThe file path parameter must be a string type.')
    elif not isinstance(PASSWORD, (str, bytes, bytearray)):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_file()"\nThe password parameter must be a string, bytes, or bytearray type.')
    elif KDF_ITERATIONS and not isinstance(KDF_ITERATIONS, int):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_file()"\nThe key derivation function iterations parameter must be an integer type.')
    elif BLOCK_SIZE and not isinstance(BLOCK_SIZE, int):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_file()"\nThe block size parameter must be an integer type.')
    elif BYTES_TOTAL and not isinstance(BYTES_TOTAL, int):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_file()"\nThe bytes total parameter must be an integer type.')
    elif START_TIME and not isinstance(START_TIME, float):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_file()"\nThe start time parameter must be a float type.')
    elif PYTHON_PROGRESSBAR and not isinstance(PYTHON_PROGRESSBAR, bool):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_file()"\nThe python progressbar parameter must be a bool type.')
    elif TKINTER_PROGRESSBAR_WINDOW and not isinstance(TKINTER_PROGRESSBAR_WINDOW, Toplevel):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_file()"\nThe tkinter progressbar window parameter must be a "tkinter.Toplevel()" type.')
    elif TKINTER_PROGRESSBAR_MESSAGE and not isinstance(TKINTER_PROGRESSBAR_MESSAGE, Label):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_file()"\nThe tkinter progressbar message parameter must be a "tkinter.Label()" type.')
    elif TKINTER_PROGRESSBAR and not isinstance(TKINTER_PROGRESSBAR, ttk.Progressbar):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_file()"\nThe tkinter progressbar parameter must be a "ttk.Progressbar()" type.')
    elif TKINTER_PROGRESSBAR_PERCENTAGE and not isinstance(TKINTER_PROGRESSBAR_PERCENTAGE, Label):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_file()"\nThe tkinter progressbar percentage parameter must be a "tkinter.Label()" type.')
    elif PROCESSED_FOLDER_BYTES_TOTAL and not isinstance(PROCESSED_FOLDER_BYTES_TOTAL, int):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_file()"\nThe processed folder bytes total parameter must be an integer type.')
    elif not isabs(FILE_PATH):
        raise ValueError('[ValueError]\nFunction: "aes_gcm_encrypt_file()"\nThe file path parameter must be an absolute path.')
    elif not isfile(FILE_PATH):
        raise FileNotFoundError('[FileNotFoundError]\nFunction: "aes_gcm_encrypt_file()"\nThe file path parameter must be a path to an existing file.')
    elif KEY_SIZE not in KEY_SIZE_LIST:
        raise ValueError('[ValueError]\nFunction: "aes_gcm_encrypt_file()"\nThe key size parameter must be an integer type consisting of 128, 192, or 256.')
    elif any([TKINTER_PROGRESSBAR_WINDOW, TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE]) and not all([TKINTER_PROGRESSBAR_WINDOW, TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE]):
        raise ValueError('[ValueError]\nFunction: "aes_gcm_encrypt_file()"\nWhen using a tkinter progressbar with this function, all 4 optional tkinter classes must be supplied.')
    try:
        if PYTHON_PROGRESSBAR and not PROCESSED_FOLDER_BYTES_TOTAL:
            ansi.hide_terminal_cursor()
        FILE_PATH = abspath(FILE_PATH)
        BLOCK_SIZE = 65536 if BLOCK_SIZE is None else BLOCK_SIZE
        #CREATE A 16-32 BYTE KEY (DEPENDENT ON THE KEY SIZE) AND A 16-BYTE SALT, 
        #USING THE "get_aes_key_and_salt()" FUNCTION, KEY SIZE (128, 192, OR 256), 
        #AND THE USER-ENTERED PASSWORD STRING, BYTES, OR BYTEARRAY
        KEY_BYTES, SALT_BYTES = get_aes_key_and_salt(KEY_SIZE, PASSWORD, None, KDF_ITERATIONS)
        #CREATE A 12-BYTE NONCE
        NONCE_BYTES = token_bytes(12)
        #USE THE KEY AND NONCE BYTES TO CREATE A CIPHER FOR THE AES-GCM ENCRYPTION
        CIPHER = Cipher(algorithms.AES(KEY_BYTES), modes.GCM(NONCE_BYTES))
        #START THE ENCRYPTION STREAMER
        ENCRYPTOR = CIPHER.encryptor()
        #CHECK PERMISSIONS
        if not all([is_normal(FILE_PATH), has_permissions(FILE_PATH, 'RW')]):
            return [False, f'\nPERMISSION_DENIED!\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
        elif PROCESSED_FOLDER_BYTES_TOTAL is not None:
            PROCESSED_BYTES = PROCESSED_FOLDER_BYTES_TOTAL
        else:
            PROCESSED_BYTES = 0
        with open(FILE_PATH, 'rb') as INFILE:
            #CHECK IF THE FILE IS EMPTY OR ALREADY AES-GCM ENCRYPTED
            AES_GCM_HEADERS_CHECK = check_aes_gcm_headers(INFILE)
            if AES_GCM_HEADERS_CHECK[1] == 'FILE_EMPTY':
                return [False, f'\nFILE_EMPTY!\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
            elif AES_GCM_HEADERS_CHECK[0]:
                return [False, f'\nALREADY_AES-GCM_ENCRYPTED!\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
            #CREATE AND OPEN A TEMPORARY FILE, TO WRITE TO, IN WRITE BYTES MODE
            with open(FILE_PATH + '.tmp', 'wb') as OUTFILE:
                RESERVED_HEADERS_LENGTH_LIST = [7, 3, 12, 16, 16]
                for RESERVED_HEADER_LENGTH in RESERVED_HEADERS_LENGTH_LIST:
                    #WRITE THE RESERVED SPACE FOR THE HEADER SIZE INTEGER (MAX INTEGER OF 4294967295, BINARY ENCODED INTO 4 BYTES) 
                    #AND THE HEADER BYTES, USING NULL-BYTES
                    OUTFILE.write(pack('>I', RESERVED_HEADER_LENGTH) + (b'\x00' * RESERVED_HEADER_LENGTH))
                if all(VALUE is None for VALUE in [BYTES_TOTAL, START_TIME, PROCESSED_FOLDER_BYTES_TOTAL]):
                    if START_TIME is None and any([PYTHON_PROGRESSBAR, TKINTER_PROGRESSBAR_WINDOW]):
                        START_TIME = time()
                        BYTES_TOTAL = getsize(FILE_PATH)
                #STREAM-ENCRYPT THE PLAINTEXT DATA, IN CHUNKS (TO ALLOW ENCRYPTION OF ALL FILE TYPES)
                while True:
                    PLAINTEXT_CHUNK = bytearray(INFILE.read(BLOCK_SIZE))
                    if not PLAINTEXT_CHUNK:
                        break
                    elif START_TIME is not None:
                        CHUNK_LENGTH = len(PLAINTEXT_CHUNK)
                        PROCESSED_BYTES += CHUNK_LENGTH
                        if PROCESSED_FOLDER_BYTES_TOTAL is not None: 
                            PROCESSED_FOLDER_BYTES_TOTAL += CHUNK_LENGTH
                        if PYTHON_PROGRESSBAR: 
                            python_progressbar(BYTES_TOTAL, START_TIME, PROCESSED_BYTES)
                        if TKINTER_PROGRESSBAR_WINDOW:
                            PERCENT_COMPLETE = (PROCESSED_BYTES / BYTES_TOTAL) * 100
                            ELAPSED_SECONDS = time() - START_TIME
                            if ELAPSED_SECONDS <= 0: 
                                ETA_SECONDS = 0
                            else:
                                BYTES_PER_SECOND = PROCESSED_BYTES / ELAPSED_SECONDS
                                REMAINING_BYTES = BYTES_TOTAL - PROCESSED_BYTES
                                ETA_SECONDS = REMAINING_BYTES / BYTES_PER_SECOND
                            TKINTER_PROGRESSBAR_WINDOW.after(0, lambda t=f'Estimated time left: {convert_seconds(ETA_SECONDS)}': TKINTER_PROGRESSBAR_MESSAGE.config(text=t))
                            TKINTER_PROGRESSBAR_WINDOW.after(0, lambda v=PERCENT_COMPLETE: TKINTER_PROGRESSBAR.config(value=v))
                            TKINTER_PROGRESSBAR_WINDOW.after(0, lambda t=f'{round(PERCENT_COMPLETE)}%': TKINTER_PROGRESSBAR_PERCENTAGE.config(text=t))
                    ENCRYPTED_CHUNK = bytearray(ENCRYPTOR.update(PLAINTEXT_CHUNK))
                    #OVERWRITE THE PLAINTEXT CHUNK VARIABLE BUFFER CONTENTS, IN THE RAM, 
                    #TO ZEROED BYTES, TO PREVENT REMAINING PLAINTEXT FILE CONTENTS, IN THE RAM
                    PLAINTEXT_CHUNK[:] = b'\x00' * len(PLAINTEXT_CHUNK)
                    #REMOVE THE PLAINTEXT CHUNK VARIABLE BUFFER REFERENCE FROM THE RAM
                    del PLAINTEXT_CHUNK
                    OUTFILE.write(pack('>I', len(ENCRYPTED_CHUNK)) + ENCRYPTED_CHUNK)
                    #OVERWRITE THE ENCRYPTED CHUNK VARIABLE BUFFER CONTENTS, IN THE RAM, 
                    #TO ZEROED BYTES, TO PREVENT REMAINING ENCRYPTED FILE CONTENTS, IN THE RAM
                    ENCRYPTED_CHUNK[:] = b'\x00' * len(ENCRYPTED_CHUNK)
                    #REMOVE THE ENCRYPTED CHUNK VARIABLE BUFFER REFERENCE FROM THE RAM
                    del ENCRYPTED_CHUNK
                #CLOSE THE ENCRYPTION STREAMER
                ENCRYPTOR.finalize()
                TAG_BYTES = ENCRYPTOR.tag
                #RESET THE FILE POINTER AND OVERWRITE THE RESERVED HEADER SPACE,
                #WITH THE AES-GCM ENCRYPTION HEADERS
                OUTFILE.seek(0)
                HEADERS_LIST = ['AES-GCM', KEY_SIZE, NONCE_BYTES, TAG_BYTES, SALT_BYTES]
                for HEADER in HEADERS_LIST:
                    HEADER_BYTES = HEADER if isinstance(HEADER, bytes) else str(HEADER).encode()
                    OUTFILE.write(pack('>I', len(HEADER_BYTES)) + HEADER_BYTES)
                #DELETE THE HEADERS LIST AND HEADER VARIABLES, AFTER WRITING TO THE TEMPORARY FILE, 
                #TO PREVENT ANY HEADER DATA FROM BEING STORED, IN THE RAM
                del HEADERS_LIST, HEADER
                #DELETE THE NONCE, TAG, AND SALT BYTES TO PREVENT STORING THEM, IN THE RAM
                del NONCE_BYTES, TAG_BYTES, SALT_BYTES
        #OVERWRITE THE PASSWORD VARIABLE BUFFER CONTENTS, IN THE RAM, 
        #TO ZEROED BYTES, TO PREVENT THE PASSWORD FROM BEING STORED, IN THE RAM,
        #IF THE SUPPLIED PASSWORD IS A BYTEARRAY TYPE
        if isinstance(PASSWORD, bytearray):
            PASSWORD[:] = b'\x00' * len(PASSWORD)
        #REMOVE THE PASSWORD VARIABLE BUFFER REFERENCE FROM THE RAM
        del PASSWORD
        #OVERWRITE THE ORIGINAL FILE'S PLAINTEXT CONTENTS WITH RANDOM BYTES,
        #BEFORE DELETION, TO PREVENT THE RECOVERY OF ANY PLAINTEXT FILE CONTENT DATA FROM THE DRIVE
        wipe_file_contents(FILE_PATH, BLOCK_SIZE)
        #DELETE THE ORIGINAL FILE AND RENAME THE ".tmp" FILE TO THE ORIGINAL FILE NAME AND EXTENSION
        replace(FILE_PATH + '.tmp', FILE_PATH)
        if PROCESSED_FOLDER_BYTES_TOTAL is None and getattr(_PROGRESSBAR_STATE, 'active', False):
            stdout.write('\n')
            ansi.show_terminal_cursor()
        return [True, f'\nAES-GCM-{KEY_SIZE}_FILE_ENCRYPTION_SUCCESSFUL!\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
    except OSError as ERROR:
        file_processing_exception_cleanup(FILE_PATH, ERROR)
        return [False, f'\nPERMISSION_DENIED!\n{ERROR}\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
    except PermissionError as ERROR:
        file_processing_exception_cleanup(FILE_PATH, ERROR)
        return [False, f'\nPERMISSION_DENIED!\n{ERROR}\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
    except Exception as ERROR:
        ERROR_TEXT = str(ERROR).strip() + '\nTry using a smaller block size.' if ERROR is not None and str(ERROR).strip() and BLOCK_SIZE > 65536 else ERROR if str(ERROR).strip() else 'An unknown error occurred, try using a smaller block size.'
        file_processing_exception_cleanup(FILE_PATH, ERROR_TEXT)
        return [False, f'\n[{type(ERROR)}]\nFunction: "aes_gcm_encrypt_file()"\n{ERROR_TEXT}\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]

#THIS FUNCTION:
#1.) REQUIRES: 
    #A.) A FILE PATH STRING
    #B.) A PASSWORD STRING, BYTES, OR BYTEARRAY
#2.) OPTIONALLY ACCEPTS: 
    #A.) A KDF ITERATIONS INTEGER
    #B.) A BLOCK SIZE INTEGER (DEFAULT IS 65536)
    #C.) A BYTES_TOTAL INTEGER (FOR CALCULATING ETA, IN THE PYTHON AND/OR GUI PROGRESSBAR OF THE "aes_gcm_decrypt_folder()" FUNCTION)
    #D.) A START TIME FLOAT (FOR CALCULATING ETA, IN THE PYTHON AND/OR GUI PROGRESSBAR OF THE "aes_gcm_decrypt_folder()" FUNCTION)
    #E.) A PYTHON PROGRESSBAR BOOL FOR DISPLAYING A PROGRESSBAR, IN A TERMINAL (DEFAULT IS "False")
    #F.) A "tkinter.Toplevel()" CLASS (FOR A GUI PROGRESSBAR WINDOW)
    #G.) A "tkinter.Label()" CLASS (FOR ETA, IN THE GUI PROGRESSBAR WINDOW)
    #H.) A "ttk.Progressbar()" CLASS (FOR THE PROGRESSBAR WINDOW, PROGRESSBAR)
    #I.) A "tkinter.Label()" CLASS (FOR PERCENTAGE, IN THE GUI PROGRESSBAR WINDOW)
    #J.) A PROCESSED FOLDER BYTES TOTAL INTEGER (FOR CALCULATING ETA, IN THE PYTHON AND/OR GUI PROGRESSBAR OF THE "aes_gcm_decrypt_folder()" FUNCTION)
#3.) AES-GCM DECRYPTS THE SUPPLIED FILE PATH (IF THE SUPPLIED PASSWORD, IS CORRECT)
#4.) RETURNS:
    #A.) "True" (SUCCESS) or "False" (ERROR)
    #B.) ANY INFO
    #C.) A PROCESSED FOLDER BYTES TOTAL INTEGER (FOR CALCULATING ETA, IN THE PROGRESSBAR, OF THE "aes_gcm_decrypt_folder()" FUNCTION)
@error_safe_python_progressbar_decorator
def aes_gcm_decrypt_file(
        FILE_PATH, PASSWORD, KDF_ITERATIONS=None, BLOCK_SIZE=None, 
        BYTES_TOTAL=None, START_TIME=None, PYTHON_PROGRESSBAR=False, TKINTER_PROGRESSBAR_WINDOW=None, 
        TKINTER_PROGRESSBAR_MESSAGE=None, TKINTER_PROGRESSBAR=None, TKINTER_PROGRESSBAR_PERCENTAGE=None, PROCESSED_FOLDER_BYTES_TOTAL=None
    ):
    if not isinstance(FILE_PATH, str):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_file()"\nThe file path parameter must be a string type.')
    elif not isinstance(PASSWORD, (str, bytes, bytearray)):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_file()"\nThe password parameter must be a string, bytes, or bytearray type.')
    elif KDF_ITERATIONS and not isinstance(KDF_ITERATIONS, int):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_file()"\nThe key derivation function iterations parameter must be an integer type.')
    elif BLOCK_SIZE and not isinstance(BLOCK_SIZE, int):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_file()"\nThe block size parameter must be an integer type.')
    elif BYTES_TOTAL and not isinstance(BYTES_TOTAL, int):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_file()"\nThe bytes total parameter must be an integer type.')
    elif START_TIME and not isinstance(START_TIME, float):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_file()"\nThe start time parameter must be a float type.')
    elif PYTHON_PROGRESSBAR and not isinstance(PYTHON_PROGRESSBAR, bool):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_file()"\nThe python progressbar parameter must be a bool type.')
    elif TKINTER_PROGRESSBAR_WINDOW and not isinstance(TKINTER_PROGRESSBAR_WINDOW, Toplevel):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_file()"\nThe tkinter progressbar window parameter must be a "tkinter.Toplevel()" type.')
    elif TKINTER_PROGRESSBAR_MESSAGE and not isinstance(TKINTER_PROGRESSBAR_MESSAGE, Label):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_file()"\nThe tkinter progressbar message parameter must be a "tkinter.Label()" type.')
    elif TKINTER_PROGRESSBAR and not isinstance(TKINTER_PROGRESSBAR, ttk.Progressbar):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_file()"\nThe tkinter progressbar parameter must be a "ttk.Progressbar()" type.')
    elif TKINTER_PROGRESSBAR_PERCENTAGE and not isinstance(TKINTER_PROGRESSBAR_PERCENTAGE, Label):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_file()"\nThe tkinter progressbar percentage parameter must be a "tkinter.Label()" type.')
    elif PROCESSED_FOLDER_BYTES_TOTAL and not isinstance(PROCESSED_FOLDER_BYTES_TOTAL, int):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_file()"\nThe processed folder bytes total parameter must be an integer type.')
    elif not isabs(FILE_PATH):
        raise ValueError('[ValueError]\nFunction: "aes_gcm_decrypt_file()"\nThe file path parameter must be an absolute path.')
    elif not isfile(FILE_PATH):
        raise FileNotFoundError('[FileNotFoundError]\nFunction: "aes_gcm_decrypt_file()"\nThe file path parameter must be a path to an existing file.')
    elif any([TKINTER_PROGRESSBAR_WINDOW, TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE]) and not all([TKINTER_PROGRESSBAR_WINDOW, TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE]):
        raise ValueError('[ValueError]\nFunction: "aes_gcm_decrypt_file()"\nWhen using a tkinter progressbar with this function, all 4 optional tkinter classes must be supplied.')
    try:
        FILE_PATH = abspath(FILE_PATH)
        BLOCK_SIZE = 65536 if BLOCK_SIZE is None else BLOCK_SIZE
        if PYTHON_PROGRESSBAR:
            ansi.hide_terminal_cursor()
        #CHECK PERMISSIONS
        if not all([is_normal(FILE_PATH), has_permissions(FILE_PATH, 'RW')]):
            return [False, f'\nPERMISSION_DENIED!\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
        #OPEN THE FILE TO DECRYPT, IN READ BYTES MODE
        with open(FILE_PATH, 'rb') as INFILE:
            #CHECK IF THE FILE IS EMPTY, NOT AES-GCM ENCRYPTED, OR HAS ANY OTHER ERROR
            AES_GCM_HEADERS_CHECK = check_aes_gcm_headers(INFILE)
            if not AES_GCM_HEADERS_CHECK[0]:
                return [False, f'\n{AES_GCM_HEADERS_CHECK[1]}!\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
            ALGORITHM_AND_MODE, KEY_SIZE, NONCE_BYTES, TAG_BYTES, SALT_BYTES, TOTAL_HEADERS_SIZE = AES_GCM_HEADERS_CHECK
            if PROCESSED_FOLDER_BYTES_TOTAL is not None:
                PROCESSED_FOLDER_BYTES_TOTAL += TOTAL_HEADERS_SIZE
                PROCESSED_BYTES = PROCESSED_FOLDER_BYTES_TOTAL
            else:
                PROCESSED_BYTES = TOTAL_HEADERS_SIZE
            #DERIVE A KEY THAT MATCHES THE ORIGINAL KEY, USING THE USER-ENTERED PASSWORD AND THE SALT BYTES STORED, 
            #IN THE FILE'S SALT BYTES HEADER
            KEY_BYTES = get_aes_key_and_salt(KEY_SIZE, PASSWORD, SALT_BYTES, KDF_ITERATIONS)[0]
            #USE THE KEY, NONCE, AND TAG BYTES TO CREATE A CIPHER FOR THE AES-GCM DECRYPTION
            CIPHER = Cipher(algorithms.AES(KEY_BYTES), modes.GCM(NONCE_BYTES, TAG_BYTES))
            #DELETE THE NONCE, TAG, AND SALT BYTES TO PREVENT STORING THEM, IN THE RAM
            del NONCE_BYTES, TAG_BYTES, SALT_BYTES
            #START THE DECRYPTION STREAMER
            DECRYPTOR = CIPHER.decryptor()
            #SET THE FILE POINTER TO THE FIRST ENCRYPTED FILE CHUNK, AFTER THE FILE'S HEADERS
            INFILE.seek(TOTAL_HEADERS_SIZE)
            with open(FILE_PATH + '.tmp', 'wb') as OUTFILE:
                #IF RUNNING A TKINTER PROGRESSBAR FROM THIS FUNCTION,
                #THE REQUIRED VARIABLES ARE SET
                if START_TIME is None and any([PYTHON_PROGRESSBAR, TKINTER_PROGRESSBAR_WINDOW]):
                    START_TIME = time()
                    BYTES_TOTAL = getsize(FILE_PATH)
                #STREAM-DECRYPT THE ENCRYPTED DATA, IN CHUNKS (TO ALLOW DECRYPTION OF ALL FILE TYPES)
                while True:
                    #READ THE BIG ENDIAN ENCODED SIZE DATA
                    SIZE_DATA = INFILE.read(4)
                    #CHECK FOR THE END OF THE FILE
                    if not SIZE_DATA or len(SIZE_DATA) < 4:
                        break
                    #READ THE CHUNK SIZE INTEGER
                    (CHUNK_SIZE,) = unpack('>I', SIZE_DATA)
                    #CHECK IF THE CHUNK SIZE INTEGER, IS CORRUPTED
                    if CHUNK_SIZE <= 0:
                        file_processing_exception_cleanup(FILE_PATH, ERROR_TEXT)
                        return [False, f'\nCHUNK_SIZE_DATA_CORRUPTED!\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
                    #READ THE AES-GCM ENCRYPTED CHUNK
                    ENCRYPTED_CHUNK = bytearray(INFILE.read(CHUNK_SIZE))
                    #CHECK IF THE ENCRYPTED CHUNK IS CORRUPTED
                    if len(ENCRYPTED_CHUNK) != CHUNK_SIZE:
                        file_processing_exception_cleanup(FILE_PATH, ERROR_TEXT)
                        return [False, f'\nCHUNK_DATA_CORRUPTED!\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
                    if START_TIME is not None:
                        CHUNK_LENGTH = 4 + len(ENCRYPTED_CHUNK)
                        PROCESSED_BYTES += CHUNK_LENGTH
                        if PROCESSED_FOLDER_BYTES_TOTAL is not None:
                            PROCESSED_FOLDER_BYTES_TOTAL += CHUNK_LENGTH
                        if PYTHON_PROGRESSBAR:
                            python_progressbar(BYTES_TOTAL, START_TIME, PROCESSED_BYTES)
                        if TKINTER_PROGRESSBAR_WINDOW:
                            PERCENT_COMPLETE = (PROCESSED_BYTES / BYTES_TOTAL) * 100
                            ELAPSED_SECONDS = time() - START_TIME
                            if ELAPSED_SECONDS <= 0:
                                ETA_SECONDS = 0
                            else:
                                BYTES_PER_SECOND = PROCESSED_BYTES / ELAPSED_SECONDS
                                REMAINING_BYTES = BYTES_TOTAL - PROCESSED_BYTES
                                ETA_SECONDS = REMAINING_BYTES / BYTES_PER_SECOND
                            TKINTER_PROGRESSBAR_WINDOW.after(0, lambda t=f'Estimated time left: {convert_seconds(ETA_SECONDS)}': TKINTER_PROGRESSBAR_MESSAGE.config(text=t))
                            TKINTER_PROGRESSBAR_WINDOW.after(0, lambda v=PERCENT_COMPLETE: TKINTER_PROGRESSBAR.config(value=v))
                            TKINTER_PROGRESSBAR_WINDOW.after(0, lambda t=f'{round(PERCENT_COMPLETE)}%': TKINTER_PROGRESSBAR_PERCENTAGE.config(text=t))
                    PLAINTEXT_CHUNK = bytearray(DECRYPTOR.update(ENCRYPTED_CHUNK))
                    #OVERWRITE THE ENCRYPTED CHUNK VARIABLE BUFFER CONTENTS, IN THE RAM, 
                    #TO ZEROED BYTES, TO PREVENT REMAINING ENCRYPTED FILE CONTENTS, IN THE RAM
                    ENCRYPTED_CHUNK[:] = b'\x00' * len(ENCRYPTED_CHUNK)
                    #REMOVE THE ENCRYPTED CHUNK VARIABLE BUFFER REFERENCE FROM THE RAM
                    del ENCRYPTED_CHUNK
                    OUTFILE.write(PLAINTEXT_CHUNK)
                    #OVERWRITE THE PLAINTEXT CHUNK VARIABLE BUFFER CONTENTS, IN THE RAM, 
                    #TO ZEROED BYTES, TO PREVENT REMAINING PLAINTEXT FILE CONTENTS, IN THE RAM
                    PLAINTEXT_CHUNK[:] = b'\x00' * len(PLAINTEXT_CHUNK)
                    #REMOVE THE PLAINTEXT CHUNK VARIABLE BUFFER REFERENCE FROM THE RAM
                    del PLAINTEXT_CHUNK
                #FINALIZE, AFTER ALL CHUNKS ARE PROCESSED
                FINAL_BYTES = DECRYPTOR.finalize()
                if FINAL_BYTES:
                    OUTFILE.write(FINAL_BYTES)
                del FINAL_BYTES
        #OVERWRITE THE PASSWORD VARIABLE BUFFER CONTENTS, IN THE RAM, 
        #TO ZEROED BYTES, TO PREVENT THE PASSWORD FROM BEING STORED, IN THE RAM,
        #IF THE SUPPLIED PASSWORD IS A BYTEARRAY TYPE
        if isinstance(PASSWORD, bytearray):
            PASSWORD[:] = b'\x00' * len(PASSWORD)
        #REMOVE THE PASSWORD VARIABLE BUFFER REFERENCE FROM THE RAM
        del PASSWORD
        #OVERWRITE THE ORIGINAL FILE'S ENCRYPTED CONTENTS WITH RANDOM BYTES,
        #BEFORE DELETION, TO PREVENT THE RECOVERY OF ANY ENCRYPTED FILE CONTENT DATA FROM THE DRIVE
        wipe_file_contents(FILE_PATH, BLOCK_SIZE)
        #DELETE THE ORIGINAL FILE AND RENAME THE ".tmp" FILE TO THE ORIGINAL FILE NAME AND EXTENSION
        replace(FILE_PATH + '.tmp', FILE_PATH)
        if PROCESSED_FOLDER_BYTES_TOTAL is None and getattr(_PROGRESSBAR_STATE, 'active', False):
            stdout.write('\n')
            ansi.show_terminal_cursor()
        return [True, f'\nAES-GCM_FILE_DECRYPTION_SUCCESSFUL!\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
    except InvalidTag:
        if isfile(FILE_PATH + '.tmp'): remove(FILE_PATH + '.tmp')
        return [False, f'\nINCORRECT_PASSWORD!\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
    except OSError as ERROR:
        file_processing_exception_cleanup(FILE_PATH, ERROR)
        return [False, f'\nPERMISSION_DENIED!\n{ERROR}\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
    except PermissionError as ERROR:
        file_processing_exception_cleanup(FILE_PATH, ERROR)
        return [False, f'\nPERMISSION_DENIED!\n{ERROR}\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
    except Exception as ERROR:
        ERROR_TEXT = (str(ERROR).strip() + '\nTry using a smaller block size.' if str(ERROR).strip() and BLOCK_SIZE > 65536 else (ERROR if str(ERROR).strip() else 'An unknown error occurred, try using a smaller block size.'))
        file_processing_exception_cleanup(FILE_PATH, ERROR_TEXT)
        return [False, f'\n[{type(ERROR)}]\nFunction: "aes_gcm_decrypt_file()"\n{ERROR_TEXT}\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]

#THIS FUNCTION:
#1.) REQUIRES: 
    #A.) A PLAINTEXT STRING OR BYTES
    #B.) A KEY SIZE INTEGER
    #C.) A PASSWORD STRING, BYTES, OR BYTEARRAY
#2.) CREATES A 16 BYTE SALT AND 12 BYTE NONCE
#3.) AES-GCM ENCRYPTS THE VARIABLE
#4.) RETURNS:
    #A.) "True" (SUCCESS) or "False" (ERROR)
    #IF SUCCESS:
        #B.) SALT BYTES 
        #C.) NONCE BYTES
        #D.) TAG BYTES
def aes_gcm_encrypt_variable(PLAINTEXT_VARIABLE, KEY_SIZE, PASSWORD):
    KEY_SIZE_LIST = [128, 192, 256]
    if not isinstance(PLAINTEXT_VARIABLE, (str, bytes)):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_variable()"\nThe plaintext variable parameter must be a string or bytes type.')
    elif not isinstance(PASSWORD, (str, bytes, bytearray)):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_variable()"\nThe password parameter must be a string, bytes, or bytearray type.')
    elif KEY_SIZE not in KEY_SIZE_LIST:
        raise ValueError('[ValueError]\nFunction: "aes_gcm_encrypt_variable()"\nThe key size parameter must be an integer type consisting of 128, 192, or 256.')
    else:
        try:
            PLAINTEXT = PLAINTEXT_VARIABLE.encode() if isinstance(PLAINTEXT_VARIABLE, str) else PLAINTEXT_VARIABLE
            KEY_BYTES, SALT_BYTES = get_aes_key_and_salt(KEY_SIZE, PASSWORD)
            NONCE_BYTES = token_bytes(12)
            CIPHER = Cipher(algorithms.AES(KEY_BYTES), modes.GCM(NONCE_BYTES))
            ENCRYPTOR = CIPHER.encryptor()
            ENCRYPTED_VARIABLE_BYTES = ENCRYPTOR.update(PLAINTEXT) + ENCRYPTOR.finalize()
            TAG_BYTES = ENCRYPTOR.tag
            return [True, ENCRYPTED_VARIABLE_BYTES, SALT_BYTES, NONCE_BYTES, TAG_BYTES]
        except BaseException as ERROR:
            return [False, f'[{ERROR.__class__.__name__ if str(ERROR).strip() else 'UnknownError'}]\nFunction: "aes_gcm_encrypt_variable()"\n{ERROR if str(ERROR).strip() else 'An unknown error occurred!'}']

#THIS FUNCTION:
#1.) REQUIRES:
    #A.) AN ENCRYPTED BYTES VARIABLE
    #B.) A KEY SIZE INTEGER
    #C.) A PASSWORD STRING, BYTES, OR BYTEARRAY
    #D.) A SALT BYTES
    #E.) A NONCE BYTES
    #F.) A TAG BYTES
#2.) VALIDATES THE PASSWORD USING THE SALT BYTES, TO CREATE A MATCHING KEY TO THE ORIGINAL ENCRYPTION KEY, IN COMBINATION WITH THE PASSWORD, USING THE "get_aes_key_and_salt()" FUNCTION
#3.) DECRYPTS THE SUPPLIED ENCRYPTED VARIABLE
#4.) RETURNS:
    #A.) "True" (SUCCESS) or "False" (ERROR) 
    #IF SUCCESS:
        #B.) DECRYPTED PLAINTEXT
def aes_gcm_decrypt_variable(ENCRYPTED_BYTES, KEY_SIZE, PASSWORD, SALT_BYTES, NONCE_BYTES, TAG_BYTES):
    KEY_SIZE_LIST = [128, 192, 256]
    if not isinstance(ENCRYPTED_BYTES, bytes):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_variable()"\nThe encrypted bytes parameter must be a bytes type.')
    elif not isinstance(PASSWORD, (str, bytes, bytearray)):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_variable()"\nThe password parameter must be a string, bytes, or bytearray type.')
    elif not isinstance(SALT_BYTES, bytes):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_variable()"\nThe salt bytes parameter must be a bytes type.')
    elif not isinstance(NONCE_BYTES, bytes):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_variable()"\nThe nonce bytes parameter must be a bytes type.')
    elif not isinstance(TAG_BYTES, bytes):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_variable()"\nThe tag bytes parameter must be a bytes type.')
    elif KEY_SIZE not in KEY_SIZE_LIST:
        raise ValueError('[ValueError]\nFunction: "aes_gcm_decrypt_variable()"\nThe key size parameter must be an integer type consisting of 128, 192, or 256.')
    elif len(SALT_BYTES) != 16:
        raise ValueError('[ValueError]\nFunction: "aes_gcm_decrypt_variable()"\nThe salt bytes parameter must be 16 bytes long.')
    elif len(NONCE_BYTES) != 12:
        raise ValueError('[ValueError]\nFunction: "aes_gcm_decrypt_variable()"\nThe nonce bytes parameter must be 12 bytes long.')
    elif len(TAG_BYTES) != 16:
        raise ValueError('[ValueError]\nFunction: "aes_gcm_decrypt_variable()"\nThe tag bytes parameter must be 16 bytes long.')
    else:
        try:
            KEY_BYTES = get_aes_key_and_salt(KEY_SIZE, PASSWORD, SALT_BYTES)[0]
            CIPHER = Cipher(algorithms.AES(KEY_BYTES), modes.GCM(NONCE_BYTES, TAG_BYTES))
            DECRYPTOR = CIPHER.decryptor()
            PLAINTEXT = DECRYPTOR.update(ENCRYPTED_BYTES) + DECRYPTOR.finalize()
            return [True, PLAINTEXT]
        except InvalidTag:
            return [False, f'INCORRECT_PASSWORD!']
        except BaseException as ERROR:
            return [False, f'[{ERROR.__class__.__name__ if str(ERROR).strip() else 'UnknownError'}]\nFunction: "aes_gcm_decrypt_variable()"\n{ERROR if str(ERROR).strip() else 'An unknown error occurred!'}']
