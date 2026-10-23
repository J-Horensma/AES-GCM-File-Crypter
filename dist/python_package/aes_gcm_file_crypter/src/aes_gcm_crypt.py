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
from psutil import cpu_freq, virtual_memory
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
#AND INITIATES THE FINALLY BLOCK AFTER THAT FUNCTION RETURNS
#3.) CATCHES ANY RAISED ERRORS THAT ARE NOT CAUGHT OR ARE RE-RAISED
_PYTHON_PROGRESSBAR_STATE = local()
def error_safe_python_progressbar_decorator(FUNCTION):
    @wraps(FUNCTION)
    def wrapper(*args, **kwargs):
        global _PYTHON_PROGRESSBAR_STATE
        if stdout is not None and getattr(_PYTHON_PROGRESSBAR_STATE, 'active', False):
            return FUNCTION(*args, **kwargs)
        elif stdout is not None:
            _PYTHON_PROGRESSBAR_STATE.active = True
            ansi.hide_terminal_cursor()
        try:
            return FUNCTION(*args, **kwargs)
        except Exception as ERROR:
            #IF THE PYTHON PROGRESSBAR IS ACTIVE AND AN EXCEPTION OCCURS, WITHIN A DECORATED FUNCTION,
            #THIS DECORATOR WILL CATCH THAT ERROR, WRITE A NEWLINE TO "stdout" AND WRITE THE ERROR TO "stdout"
            if stdout is not None and getattr(_PYTHON_PROGRESSBAR_STATE, 'active', False):
                stdout.write('\n')
                stdout.write(f'{ERROR}')
                stdout.flush()
        finally:
            #WHEN "stdout" IS NOT "None", THE PYTHON PROGRESSBAR IS ACTIVE, AND THE OUTERMOST CALLING DECORATED FUNCTION FINISHES OR AN EXCEPTION OCCURS,
            #WRITE A NEWLINE TO "stdout", TURN OFF THE PYTHON PROGRESSBAR, AND SHOW THE TERMINAL CURSOR AGAIN, BEFORE RETURNING
            #THE CALLING DECORATED FUNCTION OR AFTER AN EXCEPTION IS CAUGHT AND PROCESSED ABOVE
            if stdout is not None and getattr(_PYTHON_PROGRESSBAR_STATE, 'active', False):
                stdout.write('\n')
                stdout.flush()
                _PYTHON_PROGRESSBAR_STATE.active = False
                ansi.show_terminal_cursor()
    return wrapper

#THIS FUNCTION:
#1.) REQUIRES:
    #A.) A VARIABLE OR LIST OF VARIABLES (TO WIPE FROM THE RAM)
#2.) OVERWRITES EACH SUPPLIED VARIABLE'S RAM BUFFER VALUE WITH NULL BYTES AND 
#DELETES EACH VARIABLE VALUE'S RAM BUFFER REFERENCE
def variable_ram_buffer_wipe(VARIABLES):
    try:
        if VARIABLES is None:
            return
        elif not isinstance(VARIABLES, list):
            VARIABLES = [VARIABLES]
        for VALUE in VARIABLES:
            if isinstance(VALUE, bytearray):
                #IF THE VARIABLE VALUE IS A BYTEARRAY TYPE, OVERWRITE IT'S RAM BUFFER CONTENTS 
                #TO ZEROED BYTES, TO PREVENT THE VARIABLE VALUE FROM REMAINING, IN THE RAM
                VALUE[:] = b'\x00' * len(VALUE)
            elif isinstance(VARIABLES, (str, bytes)):
                #PYTHON VARIABLES THAT ARE NOT BYTEARRAY TYPES ARE IMMUTABLE AND
                #CANNOT HAVE THEIR RAM BUFFER VALUES CHANGED DYNAMICALLY, HOWEVER, 
                #THE VARIABLE VALUE CAN BE OVERWRITTEN AND UPDATED,
                #IN THE RAM, AS SOON AS POSSIBLE (NOT AS SECURE AS USING A BYTEARRAY)
                VALUE = b'\x00' * len(VALUE)
            del VALUE
        del VARIABLES
    except Exception as ERROR:
        EXCEPTION_CLASS = ERROR.__class__
        EXCEPTION_NAME = ERROR.__class__.__name__
        ERROR_MESSAGE = str(ERROR).strip() or 'An unknown error occurred!'
        raise EXCEPTION_CLASS(f'[{EXCEPTION_NAME}]\nFunction: "variable_ram_buffer_wipe()"\n{ERROR_MESSAGE}')

#THIS FUNCTION:
#1.) REQUIRES:
    #A.) A FILE PATH STRING
#2.) OPTIONALLY ACCEPTS:
    #A.) A BLOCK SIZE INTEGER
#3.) OVERWRITES THE FILE'S CONTENTS ON THE DISK WITH RANDOM BYTES AND
#REDUCES PLAINTEXT CHUNK DATA LEFT, IN THE RAM, WHILE DOING SO
def file_contents_disk_wipe(FILE_PATH, BLOCK_SIZE=None):
    if not isinstance(FILE_PATH, str):
        raise TypeError('[TypeError]\nFunction: "file_contents_disk_wipe()"\nThe file path parameter must be a string type.')
    elif BLOCK_SIZE and not isinstance(BLOCK_SIZE, int):
        raise TypeError('[TypeError]\nFunction: "file_contents_disk_wipe()"\nThe block size parameter must be an integer type.')
    elif not isabs(FILE_PATH):
        raise TypeError('[TypeError]\nFunction: "file_contents_disk_wipe()"\nThe file path parameter must be an absolute file path.')
    elif not isfile(FILE_PATH):
        raise TypeError('[TypeError]\nFunction: "file_contents_disk_wipe()"\nThe file path parameter must be a path to an existing file.')
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
        EXCEPTION_CLASS = ERROR.__class__
        EXCEPTION_NAME = ERROR.__class__.__name__
        ERROR_MESSAGE = str(ERROR).strip() or 'An unknown error occurred!'
        raise EXCEPTION_CLASS(f'[{EXCEPTION_NAME}]\nFunction: "file_contents_disk_wipe()"\n{ERROR_MESSAGE}')

#THIS FUNCTION:
#1.) REQUIRES: 
    #A.) A KEY SIZE INTEGER
    #B.) A PASSWORD STRING, BYTES, OR BYTEARRAY
#2.) OPTIONALLY ACCEPTS:
    #A.) A 16 BYTE SALT BYTES
    #B.) KDF ITERATIONS INTEGER
#3.) IF A 16 BYTE SALT IS NOT SUPPLIED, ONE IS GENERATED
#4.) IF A KDF ITERATIONS INTEGER IS NOT SUPPLIED, 
#THE MOST SPEED EFFICIENT AND SECURITY BALANCED ONE IS SET, IN ACCORDANCE WITH THE CPU SPEED
#5.) A KDF-KEY IS GENERATED AS A KEY FOR AES CRYPTOGRAPHY
#6.) RETURNS A LIST CONTAINING:
    #A.) KEY BYTES
    #B.) SALT BYTES
def get_aes_key_and_salt(KEY_SIZE, PASSWORD, SALT_BYTES=None, KDF_ITERATIONS=None):
    KEY_SIZE_LIST = [128, 192, 256]
    MAX_KDF_ITERATIONS = max(1, round(600_000 * ((cpu_freq().max or 3000) / 3000)))
    if not isinstance(PASSWORD, (str, bytes, bytearray)):
        raise TypeError('[TypeError]\nFunction: "get_aes_key_and_salt()"\nThe password parameter must be a string, bytes, or bytearray type.')
    elif SALT_BYTES is not None and not isinstance(SALT_BYTES, bytes):
        raise TypeError('[TypeError]\nFunction: "get_aes_key_and_salt()"\nThe salt bytes parameter must be a bytes type.')
    elif KDF_ITERATIONS is not None and not isinstance(KDF_ITERATIONS, int):
        raise TypeError('[TypeError]\nFunction: "get_aes_key_and_salt()"\nThe key derivation function iterations parameter must be an integer type.')
    elif KEY_SIZE not in KEY_SIZE_LIST:
        raise ValueError('[ValueError]\nFunction: "get_aes_key_and_salt()"\nThe key size parameter must be an integer type consisting of 128, 192, or 256.')
    elif SALT_BYTES is not None and len(SALT_BYTES) != 16:
        raise ValueError('[ValueError]\nFunction: "get_aes_key_and_salt()"\nThe salt bytes parameter must be 16 bytes long.')
    elif not 1 <= KDF_ITERATIONS <= MAX_KDF_ITERATIONS:
        raise TypeError(f'[TypeError]\nFunction: "get_aes_key_and_salt()"\nThe key derivation function iterations parameter must be an integer between 1 and {MAX_KDF_ITERATIONS}.')
    else:
        try:
            KDF_ITERATIONS = MAX_KDF_ITERATIONS if KDF_ITERATIONS is None else KDF_ITERATIONS
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
            if isinstance(PASSWORD, str):
                ENCODED_PASSWORD = bytearray(PASSWORD.encode())
            elif isinstance(PASSWORD, bytes):
                ENCODED_PASSWORD = bytearray(PASSWORD)
            elif isinstance(PASSWORD, bytearray):
                ENCODED_PASSWORD = bytearray(PASSWORD)
            #THE "cryptography.hazmat.primitives.kdf.pbkdf2.PBKDF2HMAC.derive()" FUNCTION,
            #STORES THE RETURNED KEY BYTES OBJECT VALUE, IN C-SIDE BUFFERS, NOT THE RAM (MORE DIFFICULT TO INSPECT)
            KEY_BYTES = KEY_DERIVATION_FUNCTION.derive(ENCODED_PASSWORD)
            #THE PASSWORD VARIABLE'S RAM BUFFER IS THE RAM BUFFER FOR THE PASSWORD VARIABLE OF THE CALLER THAT PASSED IT,
            #SO WIPING IT FROM THE CALLER, WILL WIPE IT HERE TOO.
            #ONLY THE ENCODED PASSWORD VARIABLE SHOULD BE WIPED OR NULL BYTE KEY BYTES WILL BE RETURNED, AS KEY BYTES BY THIS FUNCTION,
            #IN SUBSEQUENT CALLS, SUCH AS, IN "encrypt_folder()" OR "decrypt_folder()", AS IT WILL WIPE THE ORIGINAL PASSWORD VARIABLE
            #FROM THEM, BEFORE THEY FINISH.
            variable_ram_buffer_wipe(ENCODED_PASSWORD)
            return [KEY_BYTES, SALT_BYTES]
        except Exception as ERROR:
            EXCEPTION_CLASS = ERROR.__class__
            EXCEPTION_NAME = ERROR.__class__.__name__
            ERROR_MESSAGE = str(ERROR).strip() or 'An unknown error occurred!'
            raise EXCEPTION_CLASS(f'[{EXCEPTION_NAME}]\nFunction: "get_aes_key_and_salt()"\n{ERROR_MESSAGE}')

#THIS FUNCTION:
#1.) REQUIRES A PATH STRING
#2.) CHECKS IF THE PATH IS A NORMAL PATH
#3.) RETURNS "True" OR "False"
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
def recursive_files_and_bytes_total(FOLDER_PATH):
    if not isabs(FOLDER_PATH):
        raise ValueError('[ValueError]\nFunction: "recursive_files_and_bytes_total()"\nThe folder path parameter must be an absolute path.')
    elif not isdir(FOLDER_PATH):
        raise NotADirectoryError('[NotADirectoryError]\nFunction: "recursive_files_and_bytes_total()"\nThe folder path parameter must be a path to an existing folder.')
    try:
        FOLDER_PATH = abspath(FOLDER_PATH)
        ALL_FILE_PATHS = []
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
            ALL_FILE_PATHS.extend(FILE_PATHS)
            for FILE_PATH in FILE_PATHS:
                if FILE_PATH[0]:
                    FILES_TOTAL += 1
                    BYTES_TOTAL += getsize(FILE_PATH[1])
        return FILE_PATHS, FILES_TOTAL, BYTES_TOTAL
    except Exception as ERROR:
        EXCEPTION_CLASS = ERROR.__class__
        EXCEPTION_NAME = ERROR.__class__.__name__
        ERROR_MESSAGE = str(ERROR).strip() or 'An unknown error occurred!'
        raise EXCEPTION_CLASS(f'[{EXCEPTION_NAME}]\nFunction: "recursive_files_and_bytes_total()"\n{ERROR_MESSAGE}')

#THIS FUNCTION:
#1.) REQUIRES:
    #A.) A BYTES NUMBER STRING OR INTEGER
#2.) CONVERTS THE SUPPLIED BYTES NUMBER
#3.) RETURNS THE CONVERTED BYTES AS A STRING
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
        EXCEPTION_CLASS = ERROR.__class__
        EXCEPTION_NAME = ERROR.__class__.__name__
        ERROR_MESSAGE = str(ERROR).strip() or 'An unknown error occurred!'
        raise EXCEPTION_CLASS(f'[{EXCEPTION_NAME}]\nFunction: "convert_bytes()"\n{ERROR_MESSAGE}')

#THIS FUNCTION:
#1.) REQUIRES:
    #A.) A SECONDS INTEGER OR FLOAT
#2.) CONVERTS THE SUPPLIED SECONDS
#3.) RETURNS A CONVERTED SECONDS STRING
def convert_seconds(SECONDS):
    if not isinstance(SECONDS, (int, float)):
        raise TypeError('[TypeError]\nFunction: "convert_seconds()"\nThe seconds parameter must be an integer or float type.')
    try:
        YEARS = f'{round(SECONDS // 31536000)}y:' if SECONDS // 31536000 > 0 else ''; REMAINDER_SECONDS = SECONDS % 31536000
        MONTHS = f'{round(REMAINDER_SECONDS // 2628000)}M:' if REMAINDER_SECONDS // 2628000 > 0 else ''; REMAINDER_SECONDS %= 2628000
        WEEKS = f'{round(REMAINDER_SECONDS // 604800)}w:' if REMAINDER_SECONDS // 604800 > 0 else ''; REMAINDER_SECONDS %= 604800
        DAYS = f'{round(REMAINDER_SECONDS // 86400)}d:' if REMAINDER_SECONDS // 86400 > 0 else ''; REMAINDER_SECONDS %= 86400
        HOURS = f'{round(REMAINDER_SECONDS // 3600)}h:' if REMAINDER_SECONDS // 3600 > 0 else ''; REMAINDER_SECONDS %= 3600
        MINUTES = f'{round(REMAINDER_SECONDS // 60)}m:' if REMAINDER_SECONDS // 60 > 0 else ''; REMAINDER_SECONDS %= 60
        SECONDS = f'{round(REMAINDER_SECONDS % 60)}s'
        CONVERTED_SECONDS = f'{YEARS}{MONTHS}{WEEKS}{DAYS}{HOURS}{MINUTES}{SECONDS}'
        return CONVERTED_SECONDS
    except Exception as ERROR:
        EXCEPTION_CLASS = ERROR.__class__
        EXCEPTION_NAME = ERROR.__class__.__name__
        ERROR_MESSAGE = str(ERROR).strip() or 'An unknown error occurred!'
        raise EXCEPTION_CLASS(f'[{EXCEPTION_NAME}]\nFunction: "convert_seconds()"\n{ERROR_MESSAGE}')

#THIS FUNCTION:
#1.) REQUIRES:
    #A.) A TOTAL INTEGER
    #B.) A START TIME FLOAT
    #C.) A PROCESSED INTEGER
#2.) DISPLAYS A PROGRESSBAR, IN THE TERMINAL, WITH THE SUPPLIED VALUES
def python_progressbar(TOTAL, START_TIME, PROCESSED):
    if not isinstance(TOTAL, int):
        raise TypeError('[TypeError]\nFunction: "python_progressbar()"\nThe total parameter must be an integer type.')
    elif not isinstance(START_TIME, float):
        raise TypeError('[TypeError]\nFunction: "python_progressbar()"\nThe start time parameter must be a float type.')
    elif not isinstance(PROCESSED, int):
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
        EXCEPTION_CLASS = ERROR.__class__
        EXCEPTION_NAME = ERROR.__class__.__name__
        ERROR_MESSAGE = str(ERROR).strip() or 'An unknown error occurred!'
        raise EXCEPTION_CLASS(f'[{EXCEPTION_NAME}]\nFunction: "python_progressbar()"\n{ERROR_MESSAGE}')

#THIS FUNCTION:
#1.) REQUIRES:
    #A.) A TOTAL INTEGER
    #B.) A START TIME FLOAT
    #C.) A PROCESSED INTEGER
    #D.) A "tkinter.Toplevel()" CLASS (FOR A GUI PROGRESSBAR WINDOW)
    #E.) A "tkinter.Label()" CLASS (FOR ETA, IN THE GUI PROGRESSBAR WINDOW)
    #F.) A "ttk.Progressbar()" CLASS (FOR THE PROGRESSBAR WINDOW, PROGRESSBAR)
    #G.) A "tkinter.Label()" CLASS (FOR PERCENTAGE, IN THE GUI PROGRESSBAR WINDOW)
#2.) UPDATES THE SUPPLIED TKINTER PROGRESSBAR WINDOW
def update_tkinter_progressbar(
        TOTAL, START_TIME, PROCESSED, TKINTER_PROGRESSBAR_WINDOW, 
        TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE
    ):
    if not isinstance(TOTAL, int):
        raise TypeError('[TypeError]\nFunction: "update_tkinter_progressbar()"\nThe total parameter must be an integer type.')
    elif not isinstance(START_TIME, float):
        raise TypeError('[TypeError]\nFunction: "update_tkinter_progressbar()"\nThe start time parameter must be a float type.')
    elif not isinstance(PROCESSED, int):
        raise TypeError('[TypeError]\nFunction: "update_tkinter_progressbar()"\nThe processed parameter must be an integer type.')
    elif not isinstance(TKINTER_PROGRESSBAR_WINDOW, Toplevel):
        raise TypeError('[TypeError]\nFunction: "update_tkinter_progressbar()"\nThe tkinter progressbar window parameter must be a "tkinter.Toplevel()" type.')
    elif not isinstance(TKINTER_PROGRESSBAR_MESSAGE, Label):
        raise TypeError('[TypeError]\nFunction: "update_tkinter_progressbar()"\nThe tkinter progressbar message parameter must be a "tkinter.Label()" type.')
    elif not isinstance(TKINTER_PROGRESSBAR, ttk.Progressbar):
        raise TypeError('[TypeError]\nFunction: "update_tkinter_progressbar()"\nThe tkinter progressbar parameter must be a "ttk.Progressbar()" type.')
    elif not isinstance(TKINTER_PROGRESSBAR_PERCENTAGE, Label):
        raise TypeError('[TypeError]\nFunction: "update_tkinter_progressbar()"\nThe tkinter progressbar percentage parameter must be a "tkinter.Label()" type.')
    try:
        PERCENT_COMPLETE = (PROCESSED / TOTAL) * 100
        ELAPSED_SECONDS = max(time() - START_TIME, 0.001)
        PROCESSED_PER_SECOND = PROCESSED / ELAPSED_SECONDS
        REMAINING = TOTAL - PROCESSED
        ETA_SECONDS = REMAINING / PROCESSED_PER_SECOND
        TKINTER_PROGRESSBAR_WINDOW.after(0, lambda t=f'Estimated time left: {convert_seconds(ETA_SECONDS)}': TKINTER_PROGRESSBAR_MESSAGE.config(text=t))
        TKINTER_PROGRESSBAR_WINDOW.after(0, lambda v=PERCENT_COMPLETE: TKINTER_PROGRESSBAR.config(value=v))
        TKINTER_PROGRESSBAR_WINDOW.after(0, lambda t=f'{round(PERCENT_COMPLETE)}%': TKINTER_PROGRESSBAR_PERCENTAGE.config(text=t))
    except Exception as ERROR:
        EXCEPTION_CLASS = ERROR.__class__
        EXCEPTION_NAME = ERROR.__class__.__name__
        ERROR_MESSAGE = str(ERROR).strip() or 'An unknown error occurred!'
        raise EXCEPTION_CLASS(f'[{EXCEPTION_NAME}]\nFunction: "update_tkinter_progressbar()"\n{ERROR_MESSAGE}')
        
#THIS FUNCTION:
#1.) REQUIRES:
    #A.) A FILE PATH STRING
#2.) CHECKS FOR AES-GCM HEADERS, IN THE FILE
#3.) RETURNS EXISTING AES-GCM HEADERS AS A LIST OR "None" WITH ERROR INFORMATION
def check_aes_gcm_headers(FILE_PATH):
    if not isinstance(FILE_PATH, str):
        raise TypeError('[TypeError]\nFunction: "check_aes_gcm_headers()"\nThe file path parameter must be a string type.')
    elif not isabs(FILE_PATH):
        raise TypeError('[TypeError]\nFunction: "check_aes_gcm_headers()"\nThe file path parameter must be an absolute path.')
    elif not isabs(FILE_PATH):
        raise TypeError('[TypeError]\nFunction: "check_aes_gcm_headers()"\nThe file path parameter must be a path to an existing file.')
    try:
        with open(FILE_PATH, 'rb') as FILE:
            TOTAL_HEADERS_SIZE = 0
            #READ THE HEADER SIZE DATA (FIRST 4 BYTES OF EVERY AES-GCM ENCRYPTION HEADER, ENCODED INTO BIG ENDIAN BINARY BYTES)
            ALGORITHM_AND_MODE_HEADER_SIZE_DATA = FILE.read(4)
            #CHECK IF THE FILE IS EMPTY, BY CHECKING FOR THE FIRST AES-GCM ENCRYPTION HEADER'S SIZE DATA
            if len(ALGORITHM_AND_MODE_HEADER_SIZE_DATA) == 0: return [None, 'FILE_EMPTY']
            #THE "aes_gcm_encrypt_file()" FUNCTION, WRITES HEADERS TO AES-GCM ENCRYPTED FILES, IN THE FORMAT: 
            #4 BYTES (CONTAINING BIG ENDIAN BINARY ENCODED HEADER SIZE DATA) + HEADER BYTES
            #LESS THAN 4 BYTES, MEANS THE HEADER SIZE DATA, IS TRUNCATED 
            if len(ALGORITHM_AND_MODE_HEADER_SIZE_DATA) != 4: return [None, 'ALGORITHM_AND_MODE_HEADER_SIZE_TRUNCATED']
            #CONVERT THE HEADER SIZE DATA, FROM BIG ENDIAN BINARY ENCODED, TO AN INTEGER, REPRESENTING THE BYTES LENGTH OF THE HEADER
            (ALGORITHM_AND_MODE_HEADER_SIZE,) = unpack('>I', ALGORITHM_AND_MODE_HEADER_SIZE_DATA)
            #READ THE LENGTH OF THE HEADER
            ALGORITHM_AND_MODE_HEADER = FILE.read(ALGORITHM_AND_MODE_HEADER_SIZE)
            #CHECK IF THE FILE, IS AES-GCM ENCRYPTED
            if ALGORITHM_AND_MODE_HEADER != b'AES-GCM': return [None, 'NOT_AES-GCM_ENCRYPTED']
            #CHECK IF THE HEADER, IS CORRUPTED
            elif ALGORITHM_AND_MODE_HEADER_SIZE != len(ALGORITHM_AND_MODE_HEADER): return [None, 'ALGORITHM_AND_MODE_HEADER_CORRUPTED']
            #UPDATE THE TOTAL HEADERS SIZE VARIABLE, REPRESENTING THE TOTAL BYTES LENGTH OF ALL THE AES-GCM ENCRYPTION HEADERS
            TOTAL_HEADERS_SIZE += 4 + ALGORITHM_AND_MODE_HEADER_SIZE
            KEY_SIZE_HEADER_SIZE_DATA = FILE.read(4)
            if len(KEY_SIZE_HEADER_SIZE_DATA) != 4: return [None, 'KEY_SIZE_HEADER_SIZE_TRUNCATED']
            (KEY_SIZE_HEADER_SIZE,) = unpack('>I', KEY_SIZE_HEADER_SIZE_DATA)
            KEY_SIZE_HEADER = FILE.read(KEY_SIZE_HEADER_SIZE)
            TOTAL_HEADERS_SIZE += 4 + KEY_SIZE_HEADER_SIZE
            NONCE_BYTES_HEADER_SIZE_DATA = FILE.read(4)
            if len(NONCE_BYTES_HEADER_SIZE_DATA) != 4: return [None, 'NONCE_BYTES_HEADER_SIZE_TRUNCATED']
            (NONCE_BYTES_HEADER_SIZE,) = unpack('>I', NONCE_BYTES_HEADER_SIZE_DATA)
            NONCE_BYTES_HEADER = FILE.read(NONCE_BYTES_HEADER_SIZE)
            if NONCE_BYTES_HEADER_SIZE != len(NONCE_BYTES_HEADER) or len(NONCE_BYTES_HEADER) != 12: return [None, 'NONCE_BYTES_HEADER_CORRUPTED']
            TOTAL_HEADERS_SIZE += 4 + NONCE_BYTES_HEADER_SIZE
            TAG_BYTES_HEADER_SIZE_DATA = FILE.read(4)
            if len(TAG_BYTES_HEADER_SIZE_DATA) != 4: return [None, 'TAG_BYTES_HEADER_SIZE_TRUNCATED']
            (TAG_BYTES_HEADER_SIZE,) = unpack('>I', TAG_BYTES_HEADER_SIZE_DATA)
            TAG_BYTES_HEADER = FILE.read(TAG_BYTES_HEADER_SIZE)
            if TAG_BYTES_HEADER_SIZE != len(TAG_BYTES_HEADER) or len(TAG_BYTES_HEADER) != 16: return [None, 'TAG_BYTES_HEADER_CORRUPTED']
            TOTAL_HEADERS_SIZE += 4 + TAG_BYTES_HEADER_SIZE
            SALT_BYTES_HEADER_SIZE_DATA = FILE.read(4)
            if len(SALT_BYTES_HEADER_SIZE_DATA) != 4: return [None, 'SALT_BYTES_HEADER_SIZE_TRUNCATED']
            (SALT_BYTES_HEADER_SIZE,) = unpack('>I', SALT_BYTES_HEADER_SIZE_DATA)
            SALT_BYTES_HEADER = FILE.read(SALT_BYTES_HEADER_SIZE)
            if SALT_BYTES_HEADER_SIZE != len(SALT_BYTES_HEADER) or len(SALT_BYTES_HEADER) != 16: return [None, 'SALT_BYTES_HEADER_CORRUPTED']
            TOTAL_HEADERS_SIZE += 4 + SALT_BYTES_HEADER_SIZE
            if TOTAL_HEADERS_SIZE != 74: return [None, 'UNEXPECTED_TOTAL_HEADERS_SIZE']
            return [ALGORITHM_AND_MODE_HEADER.decode(), int(KEY_SIZE_HEADER.decode()), NONCE_BYTES_HEADER, TAG_BYTES_HEADER, SALT_BYTES_HEADER, TOTAL_HEADERS_SIZE]
    except Exception as ERROR:
        EXCEPTION_CLASS = ERROR.__class__
        EXCEPTION_NAME = ERROR.__class__.__name__
        ERROR_MESSAGE = str(ERROR).strip() or 'An unknown error occurred!'
        raise EXCEPTION_CLASS(f'[{EXCEPTION_NAME}]\nFunction: "check_aes_gcm_headers()"\n{ERROR_MESSAGE}')
        
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
    if not isinstance(PASSWORD, (str, bytes, bytearray)):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_folder()"\nThe password parameter must be a string, bytes, or bytearray type.')
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
    elif any([TKINTER_PROGRESSBAR_WINDOW, TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE]) and not all([TKINTER_PROGRESSBAR_WINDOW, TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE]):
        raise ValueError('[ValueError]\nFunction: "aes_gcm_encrypt_folder()"\nWhen using a tkinter progressbar with this function, all 4 optional tkinter classes must be supplied.')
    try:
        KEY_SIZE_LIST = [128, 192, 256]
        MAX_KDF_ITERATIONS = max(1, round(600_000 * ((cpu_freq().max or 3000) / 3000)))
        KDF_ITERATIONS = MAX_KDF_ITERATIONS if KDF_ITERATIONS is None else KDF_ITERATIONS
        MAX_BLOCK_SIZE = max(1, min(16 * 1024 * 1024, virtual_memory().available // 4))
        BLOCK_SIZE = MAX_BLOCK_SIZE if BLOCK_SIZE is None else BLOCK_SIZE
        if not all([isinstance(FOLDER_PATH, str), isabs(FOLDER_PATH), isdir(FOLDER_PATH)]):
            return [False, f'FOLDER_PATH_DOES_NOT_EXIST!\nThe folder path parameter must be an absolute folder path string to an existing folder path.\nFolder path: {FOLDER_PATH}']
        elif KEY_SIZE not in KEY_SIZE_LIST:
            return [False, f'INVALID_KEY_SIZE!\nThe key size parameter must be an integer value of: 128, 192, or 256.']
        elif KDF_ITERATIONS is not None and not all([isinstance(KDF_ITERATIONS, int), 1 <= KDF_ITERATIONS <= MAX_KDF_ITERATIONS]):
            return [False, f'INVALID_KDF_ITERATIONS!\nThe key derivation function iterations parameter must be an integer between 1 and {MAX_KDF_ITERATIONS}.']
        elif not all([isinstance(BLOCK_SIZE, int), 1 <= BLOCK_SIZE <= MAX_BLOCK_SIZE]):
            return [False, f'INVALID_BLOCK_SIZE!\nThe block size parameter must be an integer between 1 and {MAX_BLOCK_SIZE}.']
        FOLDER_PATH = abspath(FOLDER_PATH)
        ERRORS = []
        if stdout and PYTHON_PROGRESSBAR or TKINTER_PROGRESSBAR_WINDOW:
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
        variable_ram_buffer_wipe(PASSWORD)
        return [True if not ERRORS else False, f'{ERRORS if ERRORS else ''}AES-GCM-{KEY_SIZE}_FOLDER_ENCRYPTION_COMPLETE!\nFolder path: {FOLDER_PATH}']
    except Exception as ERROR:
        EXCEPTION_CLASS = ERROR.__class__
        EXCEPTION_NAME = ERROR.__class__.__name__
        EXCEPTION_PRETEXT = f'[{EXCEPTION_NAME}]\nFunction: "aes_gcm_encrypt_folder()"\n'
        FOLDER_PATH_MESSAGE = f'Folder path: {FOLDER_PATH}'
        ERROR_MESSAGE = (
            f'{EXCEPTION_PRETEXT}'
            f'{str(ERROR).strip() or "An unknown error occurred!"}\n'
            f'{FOLDER_PATH_MESSAGE}'
        )
        if getattr(_PYTHON_PROGRESSBAR_STATE, 'active', False): raise EXCEPTION_CLASS(ERROR_MESSAGE)
        return [False, f'{ERROR_MESSAGE}']

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
    if not isinstance(PASSWORD, (str, bytes, bytearray)):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_folder()"\nThe password parameter must be a string, bytes, or bytearray type.')
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
    elif any([TKINTER_PROGRESSBAR_WINDOW, TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE]) and not all([TKINTER_PROGRESSBAR_WINDOW, TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE]):
        raise ValueError('[ValueError]\nFunction: "aes_gcm_decrypt_folder()"\nWhen using a tkinter progressbar with this function, all 4 optional tkinter classes must be supplied.')
    try:
        MAX_KDF_ITERATIONS = max(1, round(600_000 * ((cpu_freq().max or 3000) / 3000)))
        KDF_ITERATIONS = MAX_KDF_ITERATIONS if KDF_ITERATIONS is None else KDF_ITERATIONS
        MAX_BLOCK_SIZE = max(1, min(16 * 1024 * 1024, virtual_memory().available // 4))
        BLOCK_SIZE = MAX_BLOCK_SIZE if BLOCK_SIZE is None else BLOCK_SIZE
        if not all([isinstance(FOLDER_PATH, str), isabs(FOLDER_PATH), isdir(FOLDER_PATH)]):
            return [False, f'FOLDER_PATH_DOES_NOT_EXIST!\nThe folder path parameter must be an absolute folder path string to an existing folder path.\nFolder path: {FOLDER_PATH}']
        elif not all([isinstance(KDF_ITERATIONS, int), 1 <= KDF_ITERATIONS <= MAX_KDF_ITERATIONS]):
            return [False, f'INVALID_KDF_ITERATIONS!\nThe key derivation function iterations parameter must be an integer between 1 and {MAX_KDF_ITERATIONS}.']
        elif not all([isinstance(BLOCK_SIZE, int), 1 <= BLOCK_SIZE <= MAX_BLOCK_SIZE]):
            return [False, f'INVALID_BLOCK_SIZE!\nThe block size parameter must be an integer between 1 and {MAX_BLOCK_SIZE}.']
        FOLDER_PATH = abspath(FOLDER_PATH)
        ERRORS = []
        if stdout and PYTHON_PROGRESSBAR or TKINTER_PROGRESSBAR_WINDOW:
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
        variable_ram_buffer_wipe(PASSWORD)
        return [True if not ERRORS else False, f'{ERRORS if ERRORS else ''}AES-GCM_FOLDER_DECRYPTION_COMPLETE!\nFolder path: {FOLDER_PATH}']
    except Exception as ERROR:
        EXCEPTION_CLASS = ERROR.__class__
        EXCEPTION_NAME = ERROR.__class__.__name__
        EXCEPTION_PRETEXT = f'[{EXCEPTION_NAME}]\nFunction: "aes_gcm_decrypt_folder()"\n'
        FOLDER_PATH_MESSAGE = f'Folder path: {FOLDER_PATH}'
        ERROR_MESSAGE = (
            f'{EXCEPTION_PRETEXT}'
            f'{str(ERROR).strip() or "An unknown error occurred!"}\n'
            f'{FOLDER_PATH_MESSAGE}'
        )
        if getattr(_PYTHON_PROGRESSBAR_STATE, 'active', False): raise EXCEPTION_CLASS(ERROR_MESSAGE)
        return [False, f'{ERROR_MESSAGE}']

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
    if not isinstance(PASSWORD, (str, bytes, bytearray)):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_encrypt_file()"\nThe password parameter must be a string, bytes, or bytearray type.')
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
    elif any([TKINTER_PROGRESSBAR_WINDOW, TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE]) and not all([TKINTER_PROGRESSBAR_WINDOW, TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE]):
        raise ValueError('[ValueError]\nFunction: "aes_gcm_encrypt_file()"\nWhen using a tkinter progressbar with this function, all 4 optional tkinter classes must be supplied.')
    try:
        KEY_SIZE_LIST = [128, 192, 256]
        MAX_KDF_ITERATIONS = max(1, round(600_000 * ((cpu_freq().max or 3000) / 3000)))
        KDF_ITERATIONS = MAX_KDF_ITERATIONS if KDF_ITERATIONS is None else KDF_ITERATIONS
        MAX_BLOCK_SIZE = max(1, min(16 * 1024 * 1024, virtual_memory().available // 4))
        BLOCK_SIZE = MAX_BLOCK_SIZE if BLOCK_SIZE is None else BLOCK_SIZE
        if not all([isinstance(FILE_PATH, str), isabs(FILE_PATH), isfile(FILE_PATH)]):
            return [False, f'FILE_PATH_DOES_NOT_EXIST!\nThe file path parameter must be an absolute file path string to an existing file path.\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
        elif not all([is_normal(FILE_PATH), has_permissions(FILE_PATH, 'RW')]):
            return [False, f'PERMISSION_DENIED!\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]    
        elif KEY_SIZE not in KEY_SIZE_LIST:
            return [False, f'INVALID_KEY_SIZE!\nThe key size parameter must be an integer value of: 128, 192, or 256.', PROCESSED_FOLDER_BYTES_TOTAL]
        elif not all([isinstance(KDF_ITERATIONS, int), 1 <= KDF_ITERATIONS <= MAX_KDF_ITERATIONS]):
            return [False, f'INVALID_KDF_ITERATIONS!\nThe key derivation function iterations parameter must be an integer between 1 and {MAX_KDF_ITERATIONS}.', PROCESSED_FOLDER_BYTES_TOTAL]
        elif not all([isinstance(BLOCK_SIZE, int), 1 <= BLOCK_SIZE <= MAX_BLOCK_SIZE]):
            return [False, f'INVALID_BLOCK_SIZE!\nThe block size parameter must be an integer between 1 and {MAX_BLOCK_SIZE}.', PROCESSED_FOLDER_BYTES_TOTAL]
        FILE_PATH = abspath(FILE_PATH)
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
        if PROCESSED_FOLDER_BYTES_TOTAL is not None:
            PROCESSED_BYTES = PROCESSED_FOLDER_BYTES_TOTAL
        else:
            PROCESSED_BYTES = 0
        with open(FILE_PATH, 'rb') as INFILE:
            #CHECK IF THE FILE IS EMPTY OR ALREADY AES-GCM ENCRYPTED
            AES_GCM_HEADERS_CHECK = check_aes_gcm_headers(FILE_PATH)
            if AES_GCM_HEADERS_CHECK[1] == 'FILE_EMPTY':
                return [False, f'FILE_EMPTY!\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
            elif AES_GCM_HEADERS_CHECK[0]:
                return [False, f'ALREADY_AES-GCM_ENCRYPTED!\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
            #CREATE AND OPEN A TEMPORARY FILE, TO WRITE TO, IN WRITE BYTES MODE
            with open(FILE_PATH + '.tmp', 'wb') as OUTFILE:
                RESERVED_HEADERS_LENGTH_LIST = [7, 3, 12, 16, 16]
                for RESERVED_HEADER_LENGTH in RESERVED_HEADERS_LENGTH_LIST:
                    #WRITE THE RESERVED SPACE FOR THE HEADER SIZE INTEGER (MAX INTEGER OF 4294967295, BINARY ENCODED INTO 4 BYTES) 
                    #AND THE HEADER BYTES, USING NULL-BYTES
                    OUTFILE.write(pack('>I', RESERVED_HEADER_LENGTH) + (b'\x00' * RESERVED_HEADER_LENGTH))
                if PROCESSED_FOLDER_BYTES_TOTAL is None and any([stdout and PYTHON_PROGRESSBAR, TKINTER_PROGRESSBAR_WINDOW]):
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
                        if stdout and PYTHON_PROGRESSBAR: 
                            python_progressbar(BYTES_TOTAL, START_TIME, PROCESSED_BYTES)
                        if TKINTER_PROGRESSBAR_WINDOW:
                            update_tkinter_progressbar(
                                BYTES_TOTAL, START_TIME, PROCESSED_BYTES, TKINTER_PROGRESSBAR_WINDOW, 
                                TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE
                            )
                    ENCRYPTED_CHUNK = bytearray(ENCRYPTOR.update(PLAINTEXT_CHUNK))
                    variable_ram_buffer_wipe(PLAINTEXT_CHUNK)
                    OUTFILE.write(pack('>I', len(ENCRYPTED_CHUNK)) + ENCRYPTED_CHUNK)
                    variable_ram_buffer_wipe(ENCRYPTED_CHUNK)
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
                    variable_ram_buffer_wipe([HEADER, HEADER_BYTES])
                variable_ram_buffer_wipe([HEADERS_LIST, NONCE_BYTES, TAG_BYTES, SALT_BYTES])
        if PROCESSED_FOLDER_BYTES_TOTAL is None:
            variable_ram_buffer_wipe(PASSWORD)
        file_contents_disk_wipe(FILE_PATH, BLOCK_SIZE)
        #DELETE THE ORIGINAL FILE AND RENAME THE ".tmp" FILE TO THE ORIGINAL FILE NAME AND EXTENSION
        replace(FILE_PATH + '.tmp', FILE_PATH)
        return [True, f'AES-GCM-{KEY_SIZE}_FILE_ENCRYPTION_SUCCESSFUL!\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
    except OSError as ERROR:
        if isfile(FILE_PATH + '.tmp'): remove(FILE_PATH + '.tmp')
        return [False, f'PERMISSION_DENIED!\n{ERROR}\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
    except PermissionError as ERROR:
        if isfile(FILE_PATH + '.tmp'): remove(FILE_PATH + '.tmp')
        return [False, f'PERMISSION_DENIED!\n{ERROR}\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
    except Exception as ERROR:
        if isfile(FILE_PATH + '.tmp'): remove(FILE_PATH + '.tmp')
        EXCEPTION_NAME = ERROR.__class__.__name__
        ERROR_MESSAGE = str(ERROR).strip() or 'An unknown error occurred!'
        return [False, f'[{EXCEPTION_NAME}]\nFunction: "aes_gcm_encrypt_file()"\n{ERROR_MESSAGE}\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]

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
    if not isinstance(PASSWORD, (str, bytes, bytearray)):
        raise TypeError('[TypeError]\nFunction: "aes_gcm_decrypt_file()"\nThe password parameter must be a string, bytes, or bytearray type.')
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
    elif any([TKINTER_PROGRESSBAR_WINDOW, TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE]) and not all([TKINTER_PROGRESSBAR_WINDOW, TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE]):
        raise ValueError('[ValueError]\nFunction: "aes_gcm_decrypt_file()"\nWhen using a tkinter progressbar with this function, all 4 optional tkinter classes must be supplied.')
    try:
        MAX_KDF_ITERATIONS = max(1, round(600_000 * ((cpu_freq().max or 3000) / 3000)))
        KDF_ITERATIONS = MAX_KDF_ITERATIONS if KDF_ITERATIONS is None else KDF_ITERATIONS
        MAX_BLOCK_SIZE = max(1, min(16 * 1024 * 1024, virtual_memory().available // 4))
        BLOCK_SIZE = MAX_BLOCK_SIZE if BLOCK_SIZE is None else BLOCK_SIZE
        if not all([isinstance(FILE_PATH, str), isabs(FILE_PATH), isfile(FILE_PATH)]):
            return [False, f'FILE_PATH_DOES_NOT_EXIST!\nThe file path parameter must be an absolute file path string to an existing file path.\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
        elif not all([is_normal(FILE_PATH), has_permissions(FILE_PATH, 'RW')]):
            return [False, f'PERMISSION_DENIED!\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
        elif not all([isinstance(KDF_ITERATIONS, int), 1 <= KDF_ITERATIONS <= MAX_KDF_ITERATIONS]):
            return [False, f'INVALID_KDF_ITERATIONS!\nThe key derivation function iterations parameter must be an integer between 1 and {MAX_KDF_ITERATIONS}.', PROCESSED_FOLDER_BYTES_TOTAL]
        elif not all([isinstance(BLOCK_SIZE, int), 1 <= BLOCK_SIZE <= MAX_BLOCK_SIZE]):
            return [False, f'INVALID_BLOCK_SIZE!\nThe block size parameter must be an integer between 1 and {MAX_BLOCK_SIZE}.', PROCESSED_FOLDER_BYTES_TOTAL]
        FILE_PATH = abspath(FILE_PATH)
        #OPEN THE FILE TO DECRYPT, IN READ BYTES MODE
        with open(FILE_PATH, 'rb') as INFILE:
            #CHECK IF THE FILE IS EMPTY, NOT AES-GCM ENCRYPTED, OR HAS ANY OTHER ERROR
            AES_GCM_HEADERS_CHECK = check_aes_gcm_headers(FILE_PATH)
            if not AES_GCM_HEADERS_CHECK[0]:
                return [False, f'{AES_GCM_HEADERS_CHECK[1]}!\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
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
            variable_ram_buffer_wipe([NONCE_BYTES, TAG_BYTES, SALT_BYTES])
            #START THE DECRYPTION STREAMER
            DECRYPTOR = CIPHER.decryptor()
            #SET THE FILE POINTER TO THE FIRST ENCRYPTED FILE CHUNK, AFTER THE FILE'S HEADERS
            INFILE.seek(TOTAL_HEADERS_SIZE)
            with open(FILE_PATH + '.tmp', 'wb') as OUTFILE:
                if PROCESSED_FOLDER_BYTES_TOTAL is None and any([stdout and PYTHON_PROGRESSBAR, TKINTER_PROGRESSBAR_WINDOW]):
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
                    #CHECK IF THE CHUNK SIZE INTEGER IS CORRUPTED
                    if CHUNK_SIZE <= 0:
                        return [False, f'CHUNK_SIZE_DATA_CORRUPTED!\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
                    #READ THE AES-GCM ENCRYPTED CHUNK
                    ENCRYPTED_CHUNK = bytearray(INFILE.read(CHUNK_SIZE))
                    #CHECK IF THE ENCRYPTED CHUNK IS CORRUPTED
                    if len(ENCRYPTED_CHUNK) != CHUNK_SIZE:
                        return [False, f'CHUNK_DATA_CORRUPTED!\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
                    if START_TIME is not None:
                        CHUNK_LENGTH = 4 + len(ENCRYPTED_CHUNK)
                        PROCESSED_BYTES += CHUNK_LENGTH
                        if PROCESSED_FOLDER_BYTES_TOTAL is not None:
                            PROCESSED_FOLDER_BYTES_TOTAL += CHUNK_LENGTH
                        if stdout and PYTHON_PROGRESSBAR:
                            python_progressbar(BYTES_TOTAL, START_TIME, PROCESSED_BYTES)
                        if TKINTER_PROGRESSBAR_WINDOW:
                            update_tkinter_progressbar(
                                BYTES_TOTAL, START_TIME, PROCESSED_BYTES, TKINTER_PROGRESSBAR_WINDOW, 
                                TKINTER_PROGRESSBAR_MESSAGE, TKINTER_PROGRESSBAR, TKINTER_PROGRESSBAR_PERCENTAGE
                            )
                    PLAINTEXT_CHUNK = bytearray(DECRYPTOR.update(ENCRYPTED_CHUNK))
                    variable_ram_buffer_wipe(ENCRYPTED_CHUNK)
                    OUTFILE.write(PLAINTEXT_CHUNK)
                    variable_ram_buffer_wipe(PLAINTEXT_CHUNK)
                #FINALIZE, AFTER ALL CHUNKS ARE PROCESSED
                DECRYPTOR.finalize()
        if PROCESSED_FOLDER_BYTES_TOTAL is None:
            variable_ram_buffer_wipe(PASSWORD)
        file_contents_disk_wipe(FILE_PATH, BLOCK_SIZE)
        #DELETE THE ORIGINAL FILE AND RENAME THE ".tmp" FILE TO THE ORIGINAL FILE NAME AND EXTENSION
        replace(FILE_PATH + '.tmp', FILE_PATH)
        return [True, f'AES-GCM_FILE_DECRYPTION_SUCCESSFUL!\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
    except InvalidTag:
        if isfile(FILE_PATH + '.tmp'): remove(FILE_PATH + '.tmp')
        return [False, f'INCORRECT_PASSWORD!\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
    except OSError as ERROR:
        if isfile(FILE_PATH + '.tmp'): remove(FILE_PATH + '.tmp')
        return [False, f'PERMISSION_DENIED!\n{ERROR}\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
    except PermissionError as ERROR:
        if isfile(FILE_PATH + '.tmp'): remove(FILE_PATH + '.tmp')
        return [False, f'PERMISSION_DENIED!\n{ERROR}\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]
    except Exception as ERROR:
        if isfile(FILE_PATH + '.tmp'): remove(FILE_PATH + '.tmp')
        EXCEPTION_NAME = ERROR.__class__.__name__
        ERROR_MESSAGE = str(ERROR).strip() or 'An unknown error occurred!'
        return [False, f'[{EXCEPTION_NAME}]\nFunction: "aes_gcm_decrypt_file()"\n{ERROR_MESSAGE}\nFile path: {FILE_PATH}', PROCESSED_FOLDER_BYTES_TOTAL]

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
        except Exception as ERROR:
            EXCEPTION_NAME = ERROR.__class__.__name__
            ERROR_MESSAGE = str(ERROR).strip() or 'An unknown error occurred!'
            return [False, f'[{EXCEPTION_NAME}]\nFunction: "aes_gcm_encrypt_variable()"\n{ERROR_MESSAGE}']

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
        except Exception as ERROR:
            EXCEPTION_NAME = ERROR.__class__.__name__
            ERROR_MESSAGE = str(ERROR).strip() or 'An unknown error occurred!'
            return [False, f'[{EXCEPTION_NAME}]\nFunction: "aes_gcm_decrypt_variable()"\n{ERROR_MESSAGE}']
