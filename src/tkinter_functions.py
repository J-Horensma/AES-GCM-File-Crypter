'''
Custom License, With Redistribution Limitations
-----------------------------------------------

"tkinter_functions" Copyright © 2026 Joel Horensma

For clarity:
"software" means the source code of this file.
"personal" means any use not intended for financial gain.
"commercial" means use with product(s) and/or service(s) intended for financial gain.

This software may be used, modified, and/or incorporated into projects for personal use.

Commercial use of this software is allowed when:
1.) Substantial modifications and/or additions have first been incorporated into the software (More than minor cosmetic and/or structural changes).
2.) The software changes must be reasonably demonstrable in the behavior, functionality, and/or structure of the running software(s) and/or service(s).

Redistribution, with commercial intent, of the unmodified software, or a substantially unchanged copy of it, is prohibited without prior written permission.

This copyright notice and license must be retained, precisely as-is, in all copies of the software.
'''

from os.path import abspath, isdir, isfile, expanduser
from platform import system
from tkinter import Tk, ttk, Toplevel, Frame, PhotoImage, Label, StringVar, Entry, Button, filedialog

#THIS FUNCTION:
#1.) REQUIRES A "tkinter.Tk()" ROOT WINDOW OR "Tk().Toplevel()" WINDOW CLASS,
#2.) REQUIRES ICON ICO AND/OR ICON PNG FILE PATH STRING/S
#3.) SETS THE WINDOW ICON
def set_window_icon(WINDOW, ICON_ICO_FILE_PATH=None, ICON_PNG_FILE_PATH=None):
    if system() == 'Windows' and not all([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]):
        raise ValueError('[ValueError]\nFunction: "set_window_icon()"\nThe icon ico and icon png file path parameters, must both be set when calling this function, on Windows.')
    elif system() == 'Darwin' and not ICON_ICO_FILE_PATH:
        raise ValueError('[ValueError]\nFunction: "set_window_icon()"\nThe icon ico file path parameter, must be set when calling this function, on Mac.')
    elif system() != 'Darwin'] and not ICON_PNG_FILE_PATH:
        raise ValueError('[ValueError]\nFunction: "set_window_icon()"\nThe icon png file path parameter, must be set when calling this function, on an OS other than Mac.')
    elif not isinstance(WINDOW, (Tk, Toplevel)):
        raise TypeError('[TypeError]\nFunction: "set_window_icon()"\nThe window parameter, must be a "tkinter.Tk()" or "Tk().Toplevel()" class type.')
    elif ICON_ICO_FILE_PATH and not isinstance(ICON_ICO_FILE_PATH, str):
        raise TypeError('[TypeError]\nFunction: "set_window_icon()"\nThe icon ico file path parameter, must be a string type.')
    elif ICON_PNG_FILE_PATH and not isinstance(ICON_PNG_FILE_PATH, str):
        raise TypeError('[TypeError]\nFunction: "set_window_icon()"\nThe icon png file path parameter, must be a string type.')
    elif ICON_ICO_FILE_PATH and not isabs(ICON_ICO_FILE_PATH):
        raise ValueError('[ValueError]\nFunction: "set_window_icon()"\nThe icon ico file path parameter, must be an absolute path.')
    elif ICON_PNG_FILE_PATH and not isabs(ICON_PNG_FILE_PATH):
        raise ValueError('[ValueError]\nFunction: "set_window_icon()"\nThe icon png file path parameter, must be an absolute path.')
    elif ICON_ICO_FILE_PATH and not isfile(ICON_ICO_FILE_PATH):
        raise FileNotFoundError('[FileNotFoundError]\nFunction: "set_window_icon()"\nThe icon ico file path parameter, must be a path to an existing file.')
    elif ICON_PNG_FILE_PATH and not isfile(ICON_PNG_FILE_PATH):
        raise FileNotFoundError('[FileNotFoundError]\nFunction: "set_window_icon()"\nThe icon png file path parameter, must be a path to an existing file.')
    try:
        if system() == 'Windows':
            ICON_IMAGE = PhotoImage(file=ICON_PNG_FILE_PATH)
            WINDOW.iconphoto(True, ICON_IMAGE)
            try:
                WINDOW.iconbitmap(ICON_ICO_FILE_PATH)
            except:
                pass
        elif system() == 'Darwin':
            ICON_IMAGE = PhotoImage(file=ICON_ICO_FILE_PATH)
            WINDOW.iconphoto(True, ICON_IMAGE)
        else:
            ICON_IMAGE = PhotoImage(file=ICON_PNG_FILE_PATH)
            WINDOW.iconphoto(True, ICON_IMAGE)
    except BaseException as ERROR:
        raise Exception(f'ERROR!\n{ERROR}')

#THIS FUNCTION:
#1.) REQUIRES A "tkinter.Tk()" ROOT WINDOW CLASS
#2.) RETURNS THE WIDTH AND HEIGHT OF THE DEVICE SCREEN, AS A LIST
def get_device_screen_size(ROOT_WINDOW):
    if not isinstance(ROOT_WINDOW, Tk):
        raise TypeError('[TypeError]\nFunction: "get_screen_size()"\nThe root window parameter, must be a "tkinter.Tk()" class type.')
    try:
        ROOT_WINDOW.update_idletasks()
        SCREEN_WIDTH = ROOT_WINDOW.winfo_screenwidth()
        SCREEN_HEIGHT = ROOT_WINDOW.winfo_screenheight()
        return [SCREEN_WIDTH, SCREEN_HEIGHT]
    except BaseException as ERROR:
        raise Exception(f'ERROR!\n{ERROR}')

#THIS FUNCTION:
#1.) REQUIRES A "tkinter.Tk()" ROOT WINDOW CLASS
#2.) CLEARS ALL WIDGETS, IN THE ROOT WINDOW
def clear_root_window(ROOT_WINDOW):
    if not isinstance(ROOT_WINDOW, Tk):
        raise TypeError('[TypeError]\nFunction: "clear_root_window()"\nThe root window parameter, must be a "tkinter.Tk()" class type.')
    try:
        ROOT_WINDOW.update_idletasks()
        for WIDGET in ROOT_WINDOW.winfo_children():
            WIDGET.destroy()
    except BaseException as ERROR:
        raise Exception(f'ERROR!\n{ERROR}')

#THIS FUNCTION:
#1.) REQUIRES A "tkinter.Tk()" OR "Tk().Toplevel()" WINDOW CLASS, A WINDOW WIDTH INTEGER, AND A WINDOW HEIGHT INTEGER
#2.) CENTERS THE WINDOW WITH A WINDOW SIZE OF THE SUPPLIED DIMENTIONS
def center_window(WINDOW, WINDOW_WIDTH, WINDOW_HEIGHT):
    if not isinstance(WINDOW, (Tk, Toplevel)):
        raise TypeError('[TypeError]\nFunction: "center_window()"\nThe window parameter, must be a "tkinter.Tk()" or "Tk().Toplevel()" class type.')
    elif not isinstance(WINDOW_WIDTH, int):
        raise TypeError('[TypeError]\nFunction: "center_window()"\nThe window width parameter, must be an integer.')
    elif not isinstance(WINDOW_HEIGHT, int):
        raise TypeError('[TypeError]\nFunction: "center_window()"\nThe window height parameter, must be an integer.')
    try:
        WINDOW.update_idletasks()
        X = (WINDOW.winfo_screenwidth() - WINDOW_WIDTH) // 2
        Y = (WINDOW.winfo_screenheight() - WINDOW_HEIGHT) // 2
        WINDOW.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{X}+{Y}')
    except BaseException as ERROR:
        raise Exception(f'ERROR!\n{ERROR}')

#THIS FUNCTION:
#1.) REQUIRES A "tkinter.Tk()" ROOT WINDOW CLASS AND A LIST OF DROPDOWN MENU OPTIONS
#2.) ACCEPTS OPTIONAL ICON ICO AND/OR ICON PNG FILE PATH STRING/S
#3.) ACCEPTS OPTIONAL PROMPT TITLE AND/OR PROMPT MESSAGE STRING/S
#4.) IF NO PROMPT TITLE AND/OR PROMPT MESSAGE STRING/S IS/ARE SUPPLIED, DEFAULT/S IS/ARE SET
#5.) PROMPTS THE USER TO SELECT A DROPDOWN MENU OPTION
#6.) RETURNS THE USER-SELECTED OPTION AS A STRING, OR "None", IF THE WINDOW IS CLOSED OR CANCELLED
def dropdown_menu_prompt(ROOT_WINDOW, DROPDOWN_MENU_OPTIONS, ICON_ICO_FILE_PATH=None, ICON_PNG_FILE_PATH=None, PROMPT_TITLE=None, PROMPT_MESSAGE=None):
    if system() == 'Windows' and any([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]) and not all([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]):
        raise ValueError('[ValueError]\nFunction: "dropdown_menu_prompt()"\nThe icon ico and icon png file path parameters, must both be set if using an icon with this function, on Windows.')
    elif system() == 'Darwin' and any([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]) and not ICON_ICO_FILE_PATH:
        raise ValueError('[ValueError]\nFunction: "dropdown_menu_prompt()"\nThe icon ico file path parameter, must be set if using an icon with this function, on Mac.')
    elif system() != 'Darwin' and any([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]) and not ICON_PNG_FILE_PATH:
        raise ValueError('[ValueError]\nFunction: "dropdown_menu_prompt()"\nThe icon png file path parameter, must be set if using an icon with this function, on an OS other than Mac.')
    elif not isinstance(ROOT_WINDOW, Tk):
        raise TypeError('[TypeError]\nFunction: "dropdown_menu_prompt()"\nThe root window parameter, must be a "tkinter.Tk()" class type.')
    elif not isinstance(DROPDOWN_MENU_OPTIONS, list):
        raise TypeError('[TypeError]\nFunction: "dropdown_menu_prompt()"\nThe dropdown menu options parameter, must be a list type.')
    elif not isinstance(ICON_ICO_FILE_PATH, str):
        raise TypeError('[TypeError]\nFunction: "dropdown_menu_prompt()"\nThe icon ico file path parameter, must be a string type.')
    elif not isinstance(ICON_PNG_FILE_PATH, str):
        raise TypeError('[TypeError]\nFunction: "dropdown_menu_prompt()"\nThe icon png file path parameter, must be a string type.')
    elif not isinstance(PROMPT_TITLE, str):
        raise TypeError('[TypeError]\nFunction: "dropdown_menu_prompt()"\nThe prompt title parameter, must be a string type.')
    elif not isinstance(PROMPT_MESSAGE, str):
        raise TypeError('[TypeError]\nFunction: "dropdown_menu_prompt()"\nThe prompt message parameter, must be a string type.')
    elif ICON_ICO_FILE_PATH and not isabs(ICON_ICO_FILE_PATH):
        raise ValueError('[ValueError]\nFunction: "dropdown_menu_prompt()"\nThe icon ico file path parameter, must be an absolute path.')
    elif ICON_PNG_FILE_PATH and not isabs(ICON_PNG_FILE_PATH):
        raise ValueError('[ValueError]\nFunction: "dropdown_menu_prompt()"\nThe icon png file path parameter, must be an absolute path.')
    elif ICON_ICO_FILE_PATH and not isfile(ICON_ICO_FILE_PATH):
        raise FileNotFoundError('[FileNotFoundError]\nFunction: "dropdown_menu_prompt()"\nThe icon ico file path parameter, must be a path to an existing file.')
    elif ICON_PNG_FILE_PATH and not isfile(ICON_PNG_FILE_PATH):
        raise FileNotFoundError('[FileNotFoundError]\nFunction: "dropdown_menu_prompt()"\nThe icon png file path parameter, must be a path to an existing file.')
    try:
        PROMPT_TITLE = 'Select An Option:' if PROMPT_TITLE is None else PROMPT_TITLE
        PROMPT_MESSAGE = 'Select An Option:' if PROMPT_MESSAGE is None else PROMPT_MESSAGE
        SELECTED_DROPDOWN_MENU_VALUE = None
        def close_window():
            DROPDOWN_MENU_WINDOW.destroy()
        def process_selected_value():
            nonlocal SELECTED_DROPDOWN_MENU_VALUE
            SELECTED_DROPDOWN_MENU_VALUE = DROPDOWN_MENU.get()
            DROPDOWN_MENU_WINDOW.destroy()
        #CREATE A NEW WINDOW, SEPARATE FROM THE ROOT WINDOW
        DROPDOWN_MENU_WINDOW = Toplevel(ROOT_WINDOW)
        if ICON_ICO_FILE_PATH and ICON_PNG_FILE_PATH:
            set_window_icon(DROPDOWN_MENU_WINDOW, ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH)
        #TRIGGER A CLOSE FUNCTION, WHEN THE "X" BUTTON, IS CLICKED
        DROPDOWN_MENU_WINDOW.protocol('WM_DELETE_WINDOW', close_window)
        DROPDOWN_MENU_WINDOW.title(PROMPT_TITLE)
        #PREVENT RESIZING WIDTH AND HEIGHT OF THE WINDOW
        DROPDOWN_MENU_WINDOW.resizable(False, False)
        #SEND ALL MOUSE AND KEYBOARD EVENTS TO THIS WINDOW
        DROPDOWN_MENU_WINDOW.grab_set()
        #WINDOW WIDGETS (START)
        #----------------------
        MESSAGE_LABEL = Label(DROPDOWN_MENU_WINDOW, text=PROMPT_MESSAGE, font=('Times New Roman', 18, 'bold'))
        MESSAGE_LABEL.pack(padx=10, pady=10)
        DROPDOWN_MENU = ttk.Combobox(DROPDOWN_MENU_WINDOW, values=DROPDOWN_MENU_OPTIONS, state='readonly', font=('Times New Roman', 18, 'bold'))
        DROPDOWN_MENU.pack(fill='both', padx=10)
        DROPDOWN_MENU.current(0)
        CANCEL_BUTTON = Button(DROPDOWN_MENU_WINDOW, text='Cancel', font=('Times New Roman', 18, 'bold'), command=close_window)
        CANCEL_BUTTON.pack(side='left', padx=10, pady=10)
        CONFIRM_BUTTON = Button(DROPDOWN_MENU_WINDOW, text='Confirm', font=('Times New Roman', 18, 'bold'), command=process_selected_value)
        CONFIRM_BUTTON.pack(side='right', padx=10, pady=10)
        CONFIRM_BUTTON.focus_set()
        DROPDOWN_MENU_WINDOW.bind('<Return>', lambda event: CONFIRM_BUTTON.invoke())
        #--------------------
        #WINDOW WIDGETS (END)
        #WAIT UNTIL THE WINDOW IS DESTROYED, BEFORE, RETURNING
        DROPDOWN_MENU_WINDOW.wait_window()
        return SELECTED_DROPDOWN_MENU_VALUE
    except BaseException as ERROR:
        raise Exception(f'ERROR!\n{ERROR}')

#THIS FUNCTION:
#1.) REQUIRES "tkinter.Entry()" AND "tkinter.Button()" WIDGETS
#2.) SHOWS/HIDES THE INPUT VALUE OF THE "tkinter.Entry()" WIDGET AND CHANGES THE TEXT, OF THE SHOW/HIDE BUTTON
def toggle_input_visibility(ENTRY_WIDGET, VISIBILITY_BUTTON):
    if not isinstance(ENTRY_WIDGET, Entry):
        raise TypeError('[TypeError]\nFunction: "toggle_input_visibility()"\nThe entry widget parameter, must be a "tkinter.Entry()" class type.')
    elif not isinstance(VISIBILITY_BUTTON, Button):
        raise TypeError('[TypeError]\nFunction: "toggle_input_visibility()"\nThe visibility button parameter, must be a "tkinter.Button()" class type.')
    try:
        if ENTRY_WIDGET.cget('show') == '':
            ENTRY_WIDGET.config(show='*')
            VISIBILITY_BUTTON.config(text='Show')
        else:
            ENTRY_WIDGET.config(show='')
            VISIBILITY_BUTTON.config(text='Hide')
    except BaseException as ERROR:
        raise Exception(f'ERROR!\n{ERROR}')

#THIS FUNCTION:
#1.) REQUIRES A "tkinter.Tk()" ROOT WINDOW CLASS
#2.) ACCEPTS OPTIONAL ICON ICO AND/OR ICON PNG FILE PATH STRING/S
#3.) ACCEPTS OPTIONAL PROMPT TITLE AND PROMPT MESSAGE STRINGS
#4.) IF NO PROMPT TITLE AND/OR PROMPT MESSAGE STRING/S IS/ARE SUPPLIED, DEFAULT/S IS/ARE SET
#5.) PROMPTS THE USER TO INPUT A PASSWORD
#6.) ALLOWS THE USER TO SHOW/HIDE, THE INPUT
def password_input_prompt(ROOT_WINDOW, ICON_ICO_FILE_PATH=None, ICON_PNG_FILE_PATH=None, PROMPT_TITLE=None, PROMPT_MESSAGE=None):
    if system() == 'Windows' and any([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]) and not all([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]):
        raise ValueError('[ValueError]\nFunction: "password_input_prompt()"\nThe icon ico and icon png file path parameters, must both be set if using an icon with this function, on Windows.')
    elif system() == 'Darwin' and any([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]) and not ICON_ICO_FILE_PATH:
        raise ValueError('[ValueError]\nFunction: "password_input_prompt()"\nThe icon ico file path parameter, must be set if using an icon with this function, on Mac.')
    elif system() != 'Darwin' and any([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]) and not ICON_PNG_FILE_PATH:
        raise ValueError('[ValueError]\nFunction: "password_input_prompt()"\nThe icon png file path parameter, must be set if using an icon with this function, on an OS other than Mac.')
    elif not isinstance(ROOT_WINDOW, Tk):
        raise TypeError('[TypeError]\nFunction: "password_input_prompt()"\nThe root window parameter, must be a "tkinter.Tk()" class type.')
    elif ICON_ICO_FILE_PATH and not isinstance(ICON_ICO_FILE_PATH, str):
            raise TypeError('[TypeError]\nFunction: "password_input_prompt()"\nThe icon ico file path parameter, must be a string type.')
    elif ICON_PNG_FILE_PATH and not isinstance(ICON_PNG_FILE_PATH, str):
        raise TypeError('[TypeError]\nFunction: "password_input_prompt()"\nThe icon png file path parameter, must be a string type.')
    elif PROMPT_TITLE and not isinstance(PROMPT_TITLE, str):
        raise TypeError('[TypeError]\nFunction: "password_input_prompt()"\nThe prompt title parameter, must be a string type.')
    elif PROMPT_MESSAGE and not isinstance(PROMPT_MESSAGE, str):
        raise TypeError('[TypeError]\nFunction: "password_input_prompt()"\nThe prompt message parameter, must be a string type.')
    elif ICON_ICO_FILE_PATH and not isabs(ICON_ICO_FILE_PATH):
        raise ValueError('[ValueError]\nFunction: "password_input_prompt()"\nThe icon ico file path parameter, must be an absolute path.')
    elif ICON_PNG_FILE_PATH and not isabs(ICON_PNG_FILE_PATH):
        raise ValueError('[ValueError]\nFunction: "password_input_prompt()"\nThe icon png file path parameter, must be an absolute path.')
    elif ICON_ICO_FILE_PATH and not isfile(ICON_ICO_FILE_PATH):
        raise FileNotFoundError('[FileNotFoundError]\nFunction: "password_input_prompt()"\nThe icon ico file path parameter, must be a path to an existing file.')
    elif ICON_PNG_FILE_PATH and not isfile(ICON_PNG_FILE_PATH):
        raise FileNotFoundError('[FileNotFoundError]\nFunction: "password_input_prompt()"\nThe icon png file path parameter, must be a path to an existing file.')
    PROMPT_TITLE = 'Enter A Password:' if PROMPT_TITLE is None else PROMPT_TITLE
    PROMPT_MESSAGE = 'Enter A Password:' if PROMPT_MESSAGE is None else PROMPT_MESSAGE
    PASSWORD_INPUT_VALUE = None
    def close_window():
        PASSWORD_INPUT_WINDOW.destroy()
    def process_password_input():
        nonlocal PASSWORD_INPUT_VALUE
        PASSWORD_INPUT_VALUE = PASSWORD_INPUT.get()
        PASSWORD_INPUT_WINDOW.destroy()
    #CREATE A NEW WINDOW, SEPARATE FROM THE ROOT WINDOW
    PASSWORD_INPUT_WINDOW = Toplevel(ROOT_WINDOW)
    if ICON_ICO_FILE_PATH and ICON_PNG_FILE_PATH:
        set_window_icon(PASSWORD_INPUT_WINDOW, ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH)
    #TRIGGER A CLOSE FUNCTION, WHEN THE "X" BUTTON, IS CLICKED
    PASSWORD_INPUT_WINDOW.protocol('WM_DELETE_WINDOW', close_window)
    PASSWORD_INPUT_WINDOW.title(PROMPT_TITLE)
    #PREVENT RESIZING WIDTH AND HEIGHT OF THE WINDOW
    PASSWORD_INPUT_WINDOW.resizable(False, False)
    #SEND ALL MOUSE AND KEYBOARD EVENTS TO THIS WINDOW
    PASSWORD_INPUT_WINDOW.grab_set()
    #WINDOW WIDGETS (START)
    #----------------------
    MESSAGE_LABEL = Label(PASSWORD_INPUT_WINDOW, text=PROMPT_MESSAGE, font=('Times New Roman', 18, 'bold'))
    MESSAGE_LABEL.pack(padx=10, pady=10)
    VISIBILITY = StringVar()
    CENTERED_FRAME = Frame(PASSWORD_INPUT_WINDOW)
    CENTERED_FRAME.pack(padx=10, anchor='center')
    PASSWORD_INPUT = Entry(CENTERED_FRAME, textvariable=VISIBILITY, show='*', font=('Times New Roman', 26, 'bold'))
    PASSWORD_INPUT.pack(padx=(0, 10), side='left')
    PASSWORD_INPUT.focus_set()
    VISIBILITY_BUTTON = Button(CENTERED_FRAME, text='Show', font=('Times New Roman', 18, 'bold'), command=lambda: toggle_input_visibility(PASSWORD_INPUT, VISIBILITY_BUTTON))
    VISIBILITY_BUTTON.pack(side='left')
    CANCEL_BUTTON = Button(PASSWORD_INPUT_WINDOW, text='Cancel', font=('Times New Roman', 18, 'bold'), command=close_window)
    CANCEL_BUTTON.pack(side='left', padx=10, pady=10)
    CONFIRM_BUTTON = Button(PASSWORD_INPUT_WINDOW, text='Confirm', font=('Times New Roman', 18, 'bold'), command=process_password_input)
    CONFIRM_BUTTON.pack(side='right', padx=10, pady=10)
    PASSWORD_INPUT_WINDOW.bind('<Return>', lambda event: CONFIRM_BUTTON.invoke())
    #--------------------
    #WINDOW WIDGETS (END)
    #WAIT UNTIL THE WINDOW IS DESTROYED, BEFORE, RETURNING
    PASSWORD_INPUT_WINDOW.wait_window()
    return PASSWORD_INPUT_VALUE

#THIS FUNCTION:
#1.) ACCEPTS OPTIONAL PROMPT TITLE AND/OR PROMPT PATH STRING/S
#2.) PROMPTS THE USER TO CHOOSE A FOLDER PATH
#3.) RETURNS THE ABSOLUTE FOLDER PATH THAT WAS CHOSEN, AS A STRING, OR "None", IF THE WINDOW IS CLOSED OR CANCELLED
def folder_path_prompt(PROMPT_TITLE=None, PROMPT_PATH=None):
    if PROMPT_TITLE and not isinstance(PROMPT_TITLE, str):
        raise TypeError('[TypeError]\nFunction: "folder_path_prompt()"\nThe prompt title parameter, must be a string type.')
    elif PROMPT_PATH and not isabs(PROMPT_PATH):
        raise ValueError('[ValueError]\nFunction: "folder_path_prompt()"\nThe prompt path parameter, must be an absolute path.')
    elif PROMPT_PATH and not isdir(PROMPT_PATH):
        raise NotADirectoryError('[NotADirectoryError]\nFunction: "folder_path_prompt()"\nThe prompt path parameter, must be a path to an existing folder.')
    PROMPT_TITLE = 'Choose A Folder:' if PROMPT_TITLE is None else PROMPT_TITLE
    PROMPT_PATH = expanduser('~') if PROMPT_PATH is None else PROMPT_PATH
    PATH = filedialog.askdirectory(
        title=PROMPT_TITLE,
        initialdir=PROMPT_PATH
    )
    if not PATH:
        PATH = None
    PATH = abspath(PATH)
    return PATH

#THIS FUNCTION:
#1.) ACCEPTS OPTIONAL PROMPT TITLE AND/OR PROMPT PATH STRING/S
#2.) ACCEPTS AN OPTIONAL FILE TYPES LIST
#FORMAT: [('Text Files', '*.txt'), ('Python Files', '*.py')]
#3.) PROMPTS THE USER TO CHOOSE A FILE PATH
#4.) RETURNS THE ABSOLUTE FILE PATH THAT WAS CHOSEN, AS A STRING, OR "None", IF THE WINDOW IS CLOSED OR CANCELLED
def file_path_prompt(PROMPT_TITLE=None, PROMPT_PATH=None, FILE_TYPES=None):
    if PROMPT_TITLE is not None and not isinstance(PROMPT_TITLE, str):
        raise TypeError('[TypeError]\nFunction: "file_path_prompt()"\nThe prompt title parameter, must be a string type.')
    elif PROMPT_PATH is not None and not isdir(PROMPT_PATH):
        raise NotADirectoryError('[NotADirectoryError]\nFunction: "file_path_prompt()"\nThe prompt path parameter, must be an existing absolute folder path.')
    elif FILE_TYPES is not None and not isinstance(FILE_TYPES, list):
        raise TypeError('[TypeError]\nFunction: "file_path_prompt()"\nThe file types parameter, must be a list type.')
    PROMPT_TITLE = 'Choose A File' if PROMPT_TITLE is None else PROMPT_TITLE
    PROMPT_PATH = expanduser('~') if PROMPT_PATH is None else PROMPT_PATH
    FILE_TYPES = [('All Files', '*.*')] if FILE_TYPES is None else FILE_TYPES
    PATH = filedialog.askopenfilename(
        title=PROMPT_TITLE,
        initialdir=PROMPT_PATH,
        filetypes=FILE_TYPES
    )
    if not PATH:
        PATH = None
    PATH = abspath(PATH)
    return PATH
