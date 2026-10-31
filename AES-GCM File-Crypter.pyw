'''
Custom License With Redistribution Limitations
----------------------------------------------

"AES-GCM File-Crypter" (Standard) Copyright © 2026 Joel Horensma

For clarity:
"Software" means the source code in this file.
"Personal" means any use not intended for financial gain.
"Commercial" means use with product(s) and/or service(s) intended for financial gain.

Personal use is permitted.

Redistribution, sale, or relicensing of the unmodified Software, or a
substantially unchanged copy of the Software, is prohibited without prior
written permission from the copyright holder.

This copyright notice and license must be retained, precisely as-is in all copies of the Software.
'''

from threading import Thread
from os.path import abspath, join, dirname, getsize
from platform import system
from tkinter import Tk, Menu, messagebox, Frame, scrolledtext, Button
try:
    from .src.tkinter_functions import (
        set_window_icon, center_window, dropdown_menu_prompt, create_password_prompt, 
        enter_password_prompt, folder_path_prompt, file_path_prompt, progressbar_window
    )
    from .src.aes_gcm_crypt import (
        recursive_files_and_bytes_total, convert_bytes, aes_gcm_encrypt_folder, aes_gcm_decrypt_folder,
        aes_gcm_encrypt_file, aes_gcm_decrypt_file
    )
except ImportError:
    from src.tkinter_functions import (
        set_window_icon, center_window, dropdown_menu_prompt, create_password_prompt, 
        enter_password_prompt, folder_path_prompt, file_path_prompt, progressbar_window
    )
    from src.aes_gcm_crypt import (
        recursive_files_and_bytes_total, convert_bytes, aes_gcm_encrypt_folder, aes_gcm_decrypt_folder,
        aes_gcm_encrypt_file, aes_gcm_decrypt_file
    )

def main():
    try:
        #SET THE VERSION AND EDITION
        _VERSION = '1.0.1'
        _EDITION = 'Standard'
        if system() != 'Windows':
            from signal import signal, SIGTSTP
            def handle_ctrl_z(signum, frame):
                print('"Ctrl + z" was pressed, closing AES-GCM File-Crypter...')
                ROOT_WINDOW.quit()
            signal(SIGTSTP, handle_ctrl_z)
        def disable_buttons():
            ENCRYPT_FOLDER_BUTTON.config(state='disabled')
            DECRYPT_FOLDER_BUTTON.config(state='disabled')
            ENCRYPT_FILE_BUTTON.config(state='disabled')
            DECRYPT_FILE_BUTTON.config(state='disabled')
        def enable_buttons():
            ENCRYPT_FOLDER_BUTTON.config(state='normal')
            DECRYPT_FOLDER_BUTTON.config(state='normal')
            ENCRYPT_FILE_BUTTON.config(state='normal')
            DECRYPT_FILE_BUTTON.config(state='normal')
        def aes_gcm_encrypt_folder_thread():
            PROMPT_TITLE = 'Choose A Folder To Encrypt'
            FOLDER_PATH = folder_path_prompt(PROMPT_TITLE)
            if not FOLDER_PATH:
                return
            DROPDOWN_MENU_OPTIONS = ['AES-GCM-256 (Most secure)', 'AES-GCM-192', 'AES-GCM-128 (Least drive-space used)']
            PROMPT_TITLE = 'Select A Key Size:'
            PROMPT_MESSAGE = 'Select A Key Size:'
            SELECTED_ENCRYPTION = dropdown_menu_prompt(ROOT_WINDOW, DROPDOWN_MENU_OPTIONS, PROMPT_TITLE, PROMPT_MESSAGE)
            if not SELECTED_ENCRYPTION:
                return
            KEY_SIZE = int(SELECTED_ENCRYPTION[8:12])
            MINIMUM_PASSWORD_LENGTH = 16
            PASSWORD = create_password_prompt(ROOT_WINDOW, MINIMUM_PASSWORD_LENGTH)
            if PASSWORD is None:
                return
            ACTIVITY_LOG.config(state='normal')
            CONVERTED_BYTES_TOTAL = convert_bytes(recursive_files_and_bytes_total(FOLDER_PATH)[2])
            ACTIVITY_LOG.insert('end', f'AES-GCM-{KEY_SIZE} encrypting a total of {CONVERTED_BYTES_TOTAL} in the folder: "{FOLDER_PATH}"\nplease wait...\n')
            ACTIVITY_LOG.config(state='disabled')
            ACTIVITY_LOG.see('end')
            def finish_process(ENCRYPT_RESULT, PROGRESSBAR_WINDOW):
                enable_buttons()
                ACTIVITY = ENCRYPT_RESULT[1]
                ACTIVITY_LOG.config(state='normal')
                ACTIVITY_LOG.insert('end', f'{ACTIVITY}\n\n')
                ACTIVITY_LOG.config(state='disabled')
                ACTIVITY_LOG.see('end')
                PROGRESSBAR_WINDOW.after(0, lambda: PROGRESSBAR_WINDOW.destroy())
            def start_process():
                disable_buttons()
                PROGRESSBAR_WINDOW, PROGRESSBAR_MESSAGE, PROGRESSBAR, PROGRESSBAR_PERCENTAGE = progressbar_window(ROOT_WINDOW)
                ENCRYPT_RESULT = aes_gcm_encrypt_folder(FOLDER_PATH, KEY_SIZE, PASSWORD, None, None, False, PROGRESSBAR_WINDOW, PROGRESSBAR_MESSAGE, PROGRESSBAR, PROGRESSBAR_PERCENTAGE)
                ROOT_WINDOW.after(0, lambda: finish_process(ENCRYPT_RESULT, PROGRESSBAR_WINDOW))
            Thread(target=start_process, daemon=True).start()
    
        def aes_gcm_decrypt_folder_thread():    
            PROMPT_TITLE = 'Choose A Folder To Decrypt'
            FOLDER_PATH = folder_path_prompt(PROMPT_TITLE)
            if not FOLDER_PATH:
                return
            PASSWORD = enter_password_prompt(ROOT_WINDOW)
            if PASSWORD is None:
                return
            ACTIVITY_LOG.config(state='normal')
            CONVERTED_BYTES_TOTAL = convert_bytes(recursive_files_and_bytes_total(FOLDER_PATH)[2])
            ACTIVITY_LOG.insert('end', f'AES-GCM decrypting a total of {CONVERTED_BYTES_TOTAL} in the folder: "{FOLDER_PATH}"\nplease wait...\n')
            ACTIVITY_LOG.config(state='disabled')
            ACTIVITY_LOG.see('end')
            def finish_process(DECRYPT_RESULT, PROGRESSBAR_WINDOW):
                enable_buttons()
                ACTIVITY = DECRYPT_RESULT[1]
                ACTIVITY_LOG.config(state='normal')
                ACTIVITY_LOG.insert('end', f'{ACTIVITY}\n\n')
                ACTIVITY_LOG.config(state='disabled')
                ACTIVITY_LOG.see('end')
                PROGRESSBAR_WINDOW.after(0, lambda: PROGRESSBAR_WINDOW.destroy())
            def start_process():
                disable_buttons()
                PROGRESSBAR_WINDOW, PROGRESSBAR_MESSAGE, PROGRESSBAR, PROGRESSBAR_PERCENTAGE = progressbar_window(ROOT_WINDOW)
                DECRYPT_RESULT = aes_gcm_decrypt_folder(FOLDER_PATH, PASSWORD, None, None, False, PROGRESSBAR_WINDOW, PROGRESSBAR_MESSAGE, PROGRESSBAR, PROGRESSBAR_PERCENTAGE)
                ROOT_WINDOW.after(0, lambda: finish_process(DECRYPT_RESULT, PROGRESSBAR_WINDOW))
            Thread(target=start_process, daemon=True).start()
    
        def aes_gcm_encrypt_file_thread():
            PROMPT_TITLE='Choose A File To Encrypt'
            FILE_PATH = file_path_prompt(PROMPT_TITLE)
            if not FILE_PATH:
                return
            DROPDOWN_MENU_OPTIONS = ['AES-GCM-256 (Most secure)', 'AES-GCM-192', 'AES-GCM-128 (Least drive-space used)']
            PROMPT_TITLE = 'Select A Key Size:'
            PROMPT_MESSAGE = 'Select A Key Size:'
            SELECTED_ENCRYPTION = dropdown_menu_prompt(ROOT_WINDOW, DROPDOWN_MENU_OPTIONS, PROMPT_TITLE, PROMPT_MESSAGE)
            if not SELECTED_ENCRYPTION:
                return
            KEY_SIZE = int(SELECTED_ENCRYPTION[8:12])
            MINIMUM_PASSWORD_LENGTH = 16
            PASSWORD = create_password_prompt(ROOT_WINDOW, MINIMUM_PASSWORD_LENGTH)
            if PASSWORD is None:
                return
            ACTIVITY_LOG.config(state='normal')
            ACTIVITY_LOG.insert('end', f'AES-GCM-{KEY_SIZE} encrypting a total of {convert_bytes(getsize(FILE_PATH))} of data in the file: "{FILE_PATH}"\nplease wait...\n')
            ACTIVITY_LOG.config(state='disabled')
            ACTIVITY_LOG.see('end')
            def finish_process(ENCRYPT_RESULT, PROGRESSBAR_WINDOW):
                enable_buttons()
                ACTIVITY = ENCRYPT_RESULT[1]
                ACTIVITY_LOG.config(state='normal')
                ACTIVITY_LOG.insert('end', f'{ACTIVITY}\n\n')
                ACTIVITY_LOG.config(state='disabled')
                ACTIVITY_LOG.see('end')
                PROGRESSBAR_WINDOW.after(0, lambda: PROGRESSBAR_WINDOW.destroy())
            def start_process():
                disable_buttons()
                PROGRESSBAR_WINDOW, PROGRESSBAR_MESSAGE, PROGRESSBAR, PROGRESSBAR_PERCENTAGE = progressbar_window(ROOT_WINDOW)
                ENCRYPT_RESULT = aes_gcm_encrypt_file(FILE_PATH, KEY_SIZE, PASSWORD, None, None, None, None, False, PROGRESSBAR_WINDOW, PROGRESSBAR_MESSAGE, PROGRESSBAR, PROGRESSBAR_PERCENTAGE, None)
                ROOT_WINDOW.after(0, lambda: finish_process(ENCRYPT_RESULT, PROGRESSBAR_WINDOW))
            Thread(target=start_process, daemon=True).start()
    
        def aes_gcm_decrypt_file_thread():
            PROMPT_TITLE='Choose A File To Decrypt'
            FILE_PATH = file_path_prompt(PROMPT_TITLE)
            if not FILE_PATH:
                return
            PASSWORD = enter_password_prompt(ROOT_WINDOW)
            if PASSWORD is None:
                return
            ACTIVITY_LOG.config(state='normal')
            ACTIVITY_LOG.insert('end', f'AES-GCM decrypting a total of {convert_bytes(getsize(FILE_PATH))} of data in the file: "{FILE_PATH}"\nplease wait...\n')
            ACTIVITY_LOG.config(state='disabled')
            ACTIVITY_LOG.see('end')
            def finish_process(DECRYPT_RESULT, PROGRESSBAR_WINDOW):
                enable_buttons()
                ACTIVITY = DECRYPT_RESULT[1]
                ACTIVITY_LOG.config(state='normal')
                ACTIVITY_LOG.insert('end', f'{ACTIVITY}\n\n')
                ACTIVITY_LOG.config(state='disabled')
                ACTIVITY_LOG.see('end')
                PROGRESSBAR_WINDOW.after(0, lambda: PROGRESSBAR_WINDOW.destroy())
            def start_process():
                disable_buttons()
                PROGRESSBAR_WINDOW, PROGRESSBAR_MESSAGE, PROGRESSBAR, PROGRESSBAR_PERCENTAGE = progressbar_window(ROOT_WINDOW)
                DECRYPT_RESULT = aes_gcm_decrypt_file(FILE_PATH, PASSWORD, None, None, None, None, False, PROGRESSBAR_WINDOW, PROGRESSBAR_MESSAGE, PROGRESSBAR, PROGRESSBAR_PERCENTAGE, None)
                ROOT_WINDOW.after(0, lambda: finish_process(DECRYPT_RESULT, PROGRESSBAR_WINDOW))
            Thread(target=start_process, daemon=True).start()
    
        ROOT_WINDOW = Tk()
        BASE_DIRECTORY = abspath(dirname(__file__))
        ICON_ICO_FILE_PATH = join(BASE_DIRECTORY, 'assets', 'icon', 'ico', 'icon.ico')
        ICON_PNG_FILE_PATH = join(BASE_DIRECTORY, 'assets', 'icon', 'png', '256x256.png')
        set_window_icon(ROOT_WINDOW, ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH)
        ROOT_WINDOW.configure(bg='#D3D5D4')
        WINDOW_WIDTH = 900
        WINDOW_HEIGHT = 500
        center_window(ROOT_WINDOW, WINDOW_WIDTH, WINDOW_HEIGHT)
        ROOT_WINDOW.title(f'AES-GCM File-Crypter (Standard) {_VERSION}')
        MENU_BAR = Menu(ROOT_WINDOW)
        HELP_MENU = Menu(MENU_BAR, tearoff=0)
        HELP_MENU.add_command(
            label=f'About',
            command=lambda: messagebox.showinfo(
                'About',
                f'AES-GCM File-Crypter ({_EDITION})\nVersion {_VERSION}'
            )
        )
        MENU_BAR.add_cascade(label='Help', menu=HELP_MENU)
        ROOT_WINDOW.config(menu=MENU_BAR)
        BUTTON_FRAME = Frame(ROOT_WINDOW, bg='#D3D5D4')
        BUTTON_FRAME.pack(expand=True)
        ENCRYPT_FOLDER_BUTTON = Button(
            BUTTON_FRAME,
            text='Encrypt A Folder',
            width=18,
            font=('Times New Roman', 18, 'bold'),
            command=aes_gcm_encrypt_folder_thread
        )
        ENCRYPT_FOLDER_BUTTON.pack(pady=10)
        DECRYPT_FOLDER_BUTTON = Button(
            BUTTON_FRAME,
            text='Decrypt A Folder',
            width=18,
            font=('Times New Roman', 18, 'bold'),
            command=aes_gcm_decrypt_folder_thread
        )
        DECRYPT_FOLDER_BUTTON.pack(pady=10)
        ENCRYPT_FILE_BUTTON = Button(
            BUTTON_FRAME,
            text='Encrypt A File',
            width=18,
            font=('Times New Roman', 18, 'bold'),
            command=aes_gcm_encrypt_file_thread
        )
        ENCRYPT_FILE_BUTTON.pack(pady=10)
        DECRYPT_FILE_BUTTON = Button(
            BUTTON_FRAME,
            text='Decrypt A File',
            width=18,
            font=('Times New Roman', 18, 'bold'),
            command=aes_gcm_decrypt_file_thread
        )
        DECRYPT_FILE_BUTTON.pack(pady=10)
        ACTIVITY_LOG = scrolledtext.ScrolledText(ROOT_WINDOW, width=900, height=10)
        ACTIVITY_LOG.pack(expand=True, fill='both')
        ACTIVITY_LOG.insert('insert', 'Activity Log:\n\n')
        ACTIVITY_LOG.config(state='disabled')
        ROOT_WINDOW.mainloop()
    except KeyboardInterrupt:
        print('"Ctrl + c" was pressed, closing AES-GCM File-Crypter...')
        ROOT_WINDOW.quit()
    except Exception as ERROR:
        print(f'{type(ERROR)}\nClosing AES-GCM File-Crypter...')
        ROOT_WINDOW.quit()

#CALL THE "main()" (GUI) FUNCTION IF THIS FILE IS NOT IMPORTED AS A PYTHON PACKAGE
if __package__ in (None, ''):
    main()
else:
    pass
