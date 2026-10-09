'''
Custom License With Redistribution Limitations
----------------------------------------------

"AES-GCM File-Crypter" Copyright © 2026 Joel Horensma

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

from threading import Thread
from os.path import abspath, join, dirname
from platform import system
from tkinter import Tk, ttk, Frame, scrolledtext, Button, messagebox
try:
    from .src.tkinter_functions import (
        set_window_icon, center_window, dropdown_menu_prompt, create_password_prompt, 
        enter_password_prompt, folder_path_prompt, file_path_prompt, progressbar_window
    )
    from .src.aes_gcm_crypt import (
        aes_gcm_encrypt_folder, aes_gcm_decrypt_folder,
        aes_gcm_encrypt_file, aes_gcm_decrypt_file
    )
except ImportError:
    from src.tkinter_functions import (
        set_window_icon, center_window, dropdown_menu_prompt, create_password_prompt, 
        enter_password_prompt, folder_path_prompt, file_path_prompt, progressbar_window
    )
    from src.aes_gcm_crypt import (
        aes_gcm_encrypt_folder, aes_gcm_decrypt_folder,
        aes_gcm_encrypt_file, aes_gcm_decrypt_file
    )

def main():
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
        FOLDER_PATH = abspath(folder_path_prompt(PROMPT_TITLE))
        if not FOLDER_PATH:
            return
        DROPDOWN_MENU_OPTIONS = ['AES-GCM-128 (Least drive-space used)', 'AES-GCM-192', 'AES-GCM-256 (Most secure)']
        PROMPT_TITLE = 'Select A Key Size'
        PROMPT_MESSAGE = 'Select A Key Size:'
        SELECTED_ENCRYPTION = dropdown_menu_prompt(ROOT_WINDOW, DROPDOWN_MENU_OPTIONS, ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH, PROMPT_TITLE, PROMPT_MESSAGE)
        if not SELECTED_ENCRYPTION:
            return
        KEY_SIZE = int(SELECTED_ENCRYPTION[8:12])
        MINIMUM_PASSWORD_LENGTH = 16
        PASSWORD = create_password_prompt(ROOT_WINDOW, MINIMUM_PASSWORD_LENGTH, ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH)
        if PASSWORD is None:
            return
        else:
            CONFIRMATION = messagebox.askyesno(
                title='Confirm Selection',
                message=f'The folder path:\n"{FOLDER_PATH}", will be AES-GCM-{KEY_SIZE} encrypted.\nAre you sure you want to continue?'
            )
            if not CONFIRMATION:
                return
        ACTIVITY_LOG.config(state='normal')
        ACTIVITY_LOG.insert('insert', f'AES-GCM-{KEY_SIZE} encrypting the folder: "{FOLDER_PATH}",\nplease wait...\n')
        ACTIVITY_LOG.config(state='disabled')
        ACTIVITY_LOG.see('end')
        def finish_process(ENCRYPT_RESULT, PROGRESSBAR_WINDOW):
            enable_buttons()
            ACTIVITY = ENCRYPT_RESULT[1]
            ACTIVITY_LOG.config(state='normal')
            ACTIVITY_LOG.insert('insert', f'{ACTIVITY}\n\n')
            ACTIVITY_LOG.config(state='disabled')
            ACTIVITY_LOG.see('end')
            PROGRESSBAR_WINDOW.after(0, lambda: PROGRESSBAR_WINDOW.destroy())
        def start_process():
            disable_buttons()
            PROGRESSBAR_WINDOW, PROGRESSBAR_MESSAGE, PROGRESSBAR, PROGRESSBAR_PERCENTAGE = progressbar_window(ROOT_WINDOW)
            ENCRYPT_RESULT = aes_gcm_encrypt_folder(FOLDER_PATH, KEY_SIZE, PASSWORD, None, PROGRESSBAR_WINDOW, PROGRESSBAR_MESSAGE, PROGRESSBAR, PROGRESSBAR_PERCENTAGE)
            ROOT_WINDOW.after(0, lambda: finish_process(ENCRYPT_RESULT, PROGRESSBAR_WINDOW))
        Thread(target=start_process, daemon=True).start()

    def aes_gcm_decrypt_folder_thread():    
        PROMPT_TITLE = 'Choose A Folder To Decrypt'
        FOLDER_PATH = abspath(folder_path_prompt(PROMPT_TITLE))
        if not FOLDER_PATH:
            return
        PASSWORD = enter_password_prompt(ROOT_WINDOW, ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH)
        if PASSWORD is None:
            return
        ACTIVITY_LOG.config(state='normal')
        ACTIVITY_LOG.insert('insert', f'Decrypting the folder: "{FOLDER_PATH}",\nplease wait...\n')
        ACTIVITY_LOG.config(state='disabled')
        ACTIVITY_LOG.see('end')
        PROGRESS_BAR = ttk.Progressbar(ROOT_WINDOW, mode='indeterminate')
        PROGRESS_BAR.pack(fill='both')
        def finish_process(DECRYPT_RESULT):
            PROGRESS_BAR.stop()
            PROGRESS_BAR.pack_forget()
            enable_buttons()
            ACTIVITY = DECRYPT_RESULT[1]
            ACTIVITY_LOG.config(state='normal')
            ACTIVITY_LOG.insert('insert', f'{ACTIVITY}\n\n')
            ACTIVITY_LOG.config(state='disabled')
            ACTIVITY_LOG.see('end')
        def start_process():
            disable_buttons()
            PROGRESS_BAR.start()
            DECRYPT_RESULT = aes_gcm_decrypt_folder(FOLDER_PATH, PASSWORD)
            ROOT_WINDOW.after(0, lambda: finish_process(DECRYPT_RESULT))
        Thread(target=start_process, daemon=True).start()

    def aes_gcm_encrypt_file_thread():
        PROMPT_TITLE='Choose A File To Encrypt'
        FILE_PATH = abspath(file_path_prompt(PROMPT_TITLE))
        if not FILE_PATH:
            return
        DROPDOWN_MENU_OPTIONS = ['AES-GCM-128 (Least drive-space used)', 'AES-GCM-192', 'AES-GCM-256 (Most secure)']
        PROMPT_TITLE = 'Select A Key Size'
        PROMPT_MESSAGE = 'Select A Key Size:'
        SELECTED_ENCRYPTION = dropdown_menu_prompt(ROOT_WINDOW, DROPDOWN_MENU_OPTIONS, ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH, PROMPT_TITLE, PROMPT_MESSAGE)
        if not SELECTED_ENCRYPTION:
            return
        KEY_SIZE = int(SELECTED_ENCRYPTION[8:12])
        MINIMUM_PASSWORD_LENGTH = 16
        PASSWORD = create_password_prompt(ROOT_WINDOW, MINIMUM_PASSWORD_LENGTH, ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH)
        if PASSWORD is None:
            return
        else:
            CONFIRMATION = messagebox.askyesno(
                title='Confirm Selection',
                message=f'The file path:\n"{FILE_PATH}", will be AES-GCM-{KEY_SIZE} encrypted.\nAre you sure you want to continue?'
            )
            if not CONFIRMATION:
                return
        ACTIVITY_LOG.config(state='normal')
        ACTIVITY_LOG.insert('insert', f'AES-GCM-{KEY_SIZE} encrypting the file: "{FILE_PATH}",\nplease wait...\n')
        ACTIVITY_LOG.config(state='disabled')
        ACTIVITY_LOG.see('end')
        def finish_process(ENCRYPT_RESULT, PROGRESSBAR_WINDOW):
            enable_buttons()
            ACTIVITY = ENCRYPT_RESULT[1]
            ACTIVITY_LOG.config(state='normal')
            ACTIVITY_LOG.insert('insert', f'{ACTIVITY}\n\n')
            ACTIVITY_LOG.config(state='disabled')
            ACTIVITY_LOG.see('end')
            PROGRESSBAR_WINDOW.after(0, lambda: PROGRESSBAR_WINDOW.destroy())
        def start_process():
            disable_buttons()
            PROGRESSBAR_WINDOW, PROGRESSBAR_MESSAGE, PROGRESSBAR, PROGRESSBAR_PERCENTAGE = progressbar_window(ROOT_WINDOW)
            ENCRYPT_RESULT = aes_gcm_encrypt_file(FILE_PATH, KEY_SIZE, PASSWORD, None, None, None, PROGRESSBAR_WINDOW, PROGRESSBAR_MESSAGE, PROGRESSBAR, PROGRESSBAR_PERCENTAGE)
            ROOT_WINDOW.after(0, lambda: finish_process(ENCRYPT_RESULT, PROGRESSBAR_WINDOW))
        Thread(target=start_process, daemon=True).start()

    def aes_gcm_decrypt_file_thread():
        PROMPT_TITLE='Choose A File To Decrypt'
        FILE_PATH = abspath(file_path_prompt(PROMPT_TITLE))
        if not FILE_PATH:
            return
        PASSWORD = enter_password_prompt(ROOT_WINDOW, ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH)
        if PASSWORD is None:
            return
        ACTIVITY_LOG.config(state='normal')
        ACTIVITY_LOG.insert('insert', f'Decrypting the file: "{FILE_PATH}",\nplease wait...\n')
        ACTIVITY_LOG.config(state='disabled')
        ACTIVITY_LOG.see('end')
        PROGRESS_BAR = ttk.Progressbar(ROOT_WINDOW, mode='indeterminate')
        PROGRESS_BAR.pack(fill='both')
        def finish_process(DECRYPT_RESULT):
            PROGRESS_BAR.stop()
            PROGRESS_BAR.pack_forget()
            enable_buttons()
            ACTIVITY = DECRYPT_RESULT[1]
            ACTIVITY_LOG.config(state='normal')
            ACTIVITY_LOG.insert('insert', f'{ACTIVITY}\n\n')
            ACTIVITY_LOG.config(state='disabled')
            ACTIVITY_LOG.see('end')
        def start_process():
            disable_buttons()
            PROGRESS_BAR.start()
            DECRYPT_RESULT = aes_gcm_decrypt_file(FILE_PATH, PASSWORD)
            ROOT_WINDOW.after(0, lambda: finish_process(DECRYPT_RESULT))
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
    ROOT_WINDOW.title('AES-GCM File-Crypter')
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
    try:
        ROOT_WINDOW.mainloop()
    except KeyboardInterrupt:
        print('"Ctrl + c" was pressed, closing AES-GCM File-Crypter...')
        ROOT_WINDOW.quit()
    except BaseException as ERROR:
        print(f'{ERROR if str(ERROR).strip() else 'An unknown error occurred!'}\nClosing AES-GCM File-Crypter...')
        ROOT_WINDOW.quit()

#CALL THE "main()" FUNCTION IF THIS FILE IS NOT IMPORTED AS A PYTHON PACKAGE
if __package__ in (None, ''):
    main()
else:
    #SKIP CALLING THE "main()" FUNCTION IF THIS FILE IS IMPORTED AS A PYTHON PACKAGE,
    #SO THE "main()" FUNCTION DOES NOT GET CALLED A SECOND TIME WHEN THE APPLICATION IS CLOSED
    pass
