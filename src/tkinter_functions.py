'''
Custom License With Redistribution Limitations
----------------------------------------------

"tkinter_functions" Copyright © 2026 Joel Horensma

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

from os.path import isabs, isdir, isfile, expanduser
from string import printable
from platform import system
from tkinter import Tk, ttk, Toplevel, Frame, PhotoImage, Label, StringVar, Entry, Button, filedialog
  
#THIS FUNCTION:
#1.) REQUIRES:
    #A.) A "tkinter.Tk()" OR "tkinter.Toplevel()" CLASS
    #B.) ICON ICO AND/OR ICON PNG FILE PATH STRING(S) (DEPENDING ON THE OS)
#2.) SETS THE WINDOW ICON
def set_window_icon(WINDOW, ICON_ICO_FILE_PATH=None, ICON_PNG_FILE_PATH=None):
    if not isinstance(WINDOW, (Tk, Toplevel)):
        raise TypeError('[TypeError]\nFunction: "set_window_icon()"\nThe window parameter must be a "tkinter.Tk()" or "tkinter.Toplevel()" type.')
    elif ICON_ICO_FILE_PATH and not isinstance(ICON_ICO_FILE_PATH, str):
        raise TypeError('[TypeError]\nFunction: "set_window_icon()"\nThe icon ico file path parameter must be a string type.')
    elif ICON_PNG_FILE_PATH and not isinstance(ICON_PNG_FILE_PATH, str):
        raise TypeError('[TypeError]\nFunction: "set_window_icon()"\nThe icon png file path parameter must be a string type.')
    elif system() == 'Windows' and not all([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]):
        raise ValueError('[ValueError]\nFunction: "set_window_icon()"\nThe icon ico and icon png file path parameters must both be set when calling this function on Windows.')
    elif system() == 'Darwin' and not ICON_ICO_FILE_PATH:
        raise ValueError('[ValueError]\nFunction: "set_window_icon()"\nThe icon ico file path parameter must be set when calling this function on Mac.')
    elif system() != 'Darwin' and not ICON_PNG_FILE_PATH:
        raise ValueError('[ValueError]\nFunction: "set_window_icon()"\nThe icon png file path parameter must be set when calling this function on an OS other than Mac.')
    elif ICON_ICO_FILE_PATH and not isabs(ICON_ICO_FILE_PATH):
        raise ValueError('[ValueError]\nFunction: "set_window_icon()"\nThe icon ico file path parameter must be an absolute path.')
    elif ICON_PNG_FILE_PATH and not isabs(ICON_PNG_FILE_PATH):
        raise ValueError('[ValueError]\nFunction: "set_window_icon()"\nThe icon png file path parameter must be an absolute path.')
    elif ICON_ICO_FILE_PATH and not isfile(ICON_ICO_FILE_PATH):
        raise FileNotFoundError('[FileNotFoundError]\nFunction: "set_window_icon()"\nThe icon ico file path parameter must be a path to an existing file.')
    elif ICON_PNG_FILE_PATH and not isfile(ICON_PNG_FILE_PATH):
        raise FileNotFoundError('[FileNotFoundError]\nFunction: "set_window_icon()"\nThe icon png file path parameter must be a path to an existing file.')
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
        raise Exception(f'[{ERROR.__class__.__name__ if str(ERROR).strip() else 'UnknownError'}]\nFunction: "set_window_icon()"\n{ERROR if str(ERROR).strip() else 'An unknown error occurred!'}')

#THIS FUNCTION:
#1.) REQUIRES A "tkinter.Tk()" CLASS
#2.) RETURNS WIDTH AND HEIGHT INTEGERS OF THE DEVICE SCREEN
def get_device_screen_size(ROOT_WINDOW):
    if not isinstance(ROOT_WINDOW, Tk):
        raise TypeError('[TypeError]\nFunction: "get_device_screen_size()"\nThe root window parameter must be a "tkinter.Tk()" class type.')
    try:
        ROOT_WINDOW.update_idletasks()
        SCREEN_WIDTH = ROOT_WINDOW.winfo_screenwidth()
        SCREEN_HEIGHT = ROOT_WINDOW.winfo_screenheight()
        return [SCREEN_WIDTH, SCREEN_HEIGHT]
    except BaseException as ERROR:
        raise Exception(f'[{ERROR.__class__.__name__ if str(ERROR).strip() else 'UnknownError'}]\nFunction: "get_device_screen_size()"\n{ERROR if str(ERROR).strip() else 'An unknown error occurred!'}')

#THIS FUNCTION:
#1.) REQUIRES A "tkinter.Tk()" OR "tkinter.Toplevel()" CLASS
#2.) CLEARS ALL WIDGETS, IN THE WINDOW, WHILE KEEPING THE WINDOW OPEN
def clear_window(WINDOW):
    if not isinstance(WINDOW, (Tk, Toplevel)):
        raise TypeError('[TypeError]\nFunction: "clear_window()"\nThe window parameter must be a "tkinter.Tk()" or "tkinter.Toplevel()" type.')
    try:
        WINDOW.update_idletasks()
        for WIDGET in ROOT_WINDOW.winfo_children():
            WIDGET.destroy()
    except BaseException as ERROR:
        raise Exception(f'[{ERROR.__class__.__name__ if str(ERROR).strip() else 'UnknownError'}]\nFunction: "clear_window()"\n{ERROR if str(ERROR).strip() else 'An unknown error occurred!'}')

#THIS FUNCTION:
#1.) REQUIRES:
    #A.) A "tkinter.Tk()" OR "tkinter.Toplevel()" CLASS
    #B.) WINDOW WIDTH AND WINDOW HEIGHT INTEGERS
#2.) CENTERS THE WINDOW WITH A WINDOW SIZE OF THE SUPPLIED DIMENSIONS
def center_window(WINDOW, WINDOW_WIDTH, WINDOW_HEIGHT):
    if not isinstance(WINDOW, (Tk, Toplevel)):
        raise TypeError('[TypeError]\nFunction: "center_window()"\nThe window parameter must be a "tkinter.Tk()" or "tkinter.Toplevel()" type.')
    elif not isinstance(WINDOW_WIDTH, int):
        raise TypeError('[TypeError]\nFunction: "center_window()"\nThe window width parameter must be an integer.')
    elif not isinstance(WINDOW_HEIGHT, int):
        raise TypeError('[TypeError]\nFunction: "center_window()"\nThe window height parameter must be an integer.')
    try:
        WINDOW.update_idletasks()
        X = (WINDOW.winfo_screenwidth() - WINDOW_WIDTH) // 2
        Y = (WINDOW.winfo_screenheight() - WINDOW_HEIGHT) // 2
        WINDOW.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{X}+{Y}')
    except BaseException as ERROR:
        raise Exception(f'[{ERROR.__class__.__name__ if str(ERROR).strip() else 'UnknownError'}]\nFunction: "center_window()"\n{ERROR if str(ERROR).strip() else 'An unknown error occurred!'}')

#THIS FUNCTION:
#1.) REQUIRES:
    #A.) A "tkinter.Tk()" CLASS
    #B.) A LIST OF DROPDOWN MENU OPTIONS
#2.) OPTIONALLY ACCEPTS:
    #A.) ICON ICO AND/OR ICON PNG FILE PATH STRING(S)
    #B.) PROMPT TITLE AND/OR PROMPT MESSAGE STRING(S) (DEFAULT IS "Select An Option")
#3.) PROMPTS THE USER TO SELECT A DROPDOWN MENU OPTION
#4.) RETURNS THE USER-SELECTED OPTION AS A STRING OR "None" IF THE WINDOW IS CLOSED OR CANCELLED
def dropdown_menu_prompt(ROOT_WINDOW, DROPDOWN_MENU_OPTIONS, ICON_ICO_FILE_PATH=None, ICON_PNG_FILE_PATH=None, PROMPT_TITLE=None, PROMPT_MESSAGE=None):
    if not isinstance(ROOT_WINDOW, Tk):
        raise TypeError('[TypeError]\nFunction: "dropdown_menu_prompt()"\nThe root window parameter must be a "tkinter.Tk()" type.')
    elif not isinstance(DROPDOWN_MENU_OPTIONS, list):
        raise TypeError('[TypeError]\nFunction: "dropdown_menu_prompt()"\nThe dropdown menu options parameter must be a list type.')
    elif not isinstance(ICON_ICO_FILE_PATH, str):
        raise TypeError('[TypeError]\nFunction: "dropdown_menu_prompt()"\nThe icon ico file path parameter must be a string type.')
    elif not isinstance(ICON_PNG_FILE_PATH, str):
        raise TypeError('[TypeError]\nFunction: "dropdown_menu_prompt()"\nThe icon png file path parameter must be a string type.')
    elif not isinstance(PROMPT_TITLE, str):
        raise TypeError('[TypeError]\nFunction: "dropdown_menu_prompt()"\nThe prompt title parameter must be a string type.')
    elif not isinstance(PROMPT_MESSAGE, str):
        raise TypeError('[TypeError]\nFunction: "dropdown_menu_prompt()"\nThe prompt message parameter must be a string type.')
    elif system() == 'Windows' and any([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]) and not all([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]):
        raise ValueError('[ValueError]\nFunction: "dropdown_menu_prompt()"\nThe icon ico and icon png file path parameters, must both be set if using an icon with this function on Windows.')
    elif system() == 'Darwin' and any([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]) and not ICON_ICO_FILE_PATH:
        raise ValueError('[ValueError]\nFunction: "dropdown_menu_prompt()"\nThe icon ico file path parameter must be set if using an icon with this function on Mac.')
    elif system() != 'Darwin' and any([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]) and not ICON_PNG_FILE_PATH:
        raise ValueError('[ValueError]\nFunction: "dropdown_menu_prompt()"\nThe icon png file path parameter must be set if using an icon with this function on an OS other than Mac.')
    elif ICON_ICO_FILE_PATH and not isabs(ICON_ICO_FILE_PATH):
        raise ValueError('[ValueError]\nFunction: "dropdown_menu_prompt()"\nThe icon ico file path parameter must be an absolute path.')
    elif ICON_PNG_FILE_PATH and not isabs(ICON_PNG_FILE_PATH):
        raise ValueError('[ValueError]\nFunction: "dropdown_menu_prompt()"\nThe icon png file path parameter must be an absolute path.')
    elif ICON_ICO_FILE_PATH and not isfile(ICON_ICO_FILE_PATH):
        raise FileNotFoundError('[FileNotFoundError]\nFunction: "dropdown_menu_prompt()"\nThe icon ico file path parameter must be a path to an existing file.')
    elif ICON_PNG_FILE_PATH and not isfile(ICON_PNG_FILE_PATH):
        raise FileNotFoundError('[FileNotFoundError]\nFunction: "dropdown_menu_prompt()"\nThe icon png file path parameter must be a path to an existing file.')
    try:
        PROMPT_TITLE = 'Select An Option' if PROMPT_TITLE is None else PROMPT_TITLE
        PROMPT_MESSAGE = 'Select An Option:' if PROMPT_MESSAGE is None else PROMPT_MESSAGE
        SELECTED_DROPDOWN_MENU_VALUE = None
        def close_window():
            DROPDOWN_MENU_WINDOW.destroy()
        def process_selected_value():
            nonlocal SELECTED_DROPDOWN_MENU_VALUE
            SELECTED_DROPDOWN_MENU_VALUE = DROPDOWN_MENU.get()
            DROPDOWN_MENU_WINDOW.destroy()
        DROPDOWN_MENU_WINDOW = Toplevel(ROOT_WINDOW)
        if ICON_ICO_FILE_PATH or ICON_PNG_FILE_PATH:
            set_window_icon(DROPDOWN_MENU_WINDOW, ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH)
        DROPDOWN_MENU_WINDOW.title(PROMPT_TITLE)
        DROPDOWN_MENU_WINDOW.resizable(False, False)
        #TRIGGER A CLOSE FUNCTION WHEN THE "X" BUTTON IS CLICKED
        DROPDOWN_MENU_WINDOW.protocol('WM_DELETE_WINDOW', close_window)
        #SEND ALL MOUSE AND KEYBOARD EVENTS TO THIS WINDOW
        DROPDOWN_MENU_WINDOW.grab_set()
        MESSAGE_LABEL = Label(DROPDOWN_MENU_WINDOW, text=PROMPT_MESSAGE, font=('Times New Roman', 18, 'bold'))
        MESSAGE_LABEL.pack(padx=10, pady=10)
        DROPDOWN_MENU = ttk.Combobox(DROPDOWN_MENU_WINDOW, values=DROPDOWN_MENU_OPTIONS, state='readonly', font=('Times New Roman', 18, 'bold'))
        DROPDOWN_MENU.pack(fill='both', padx=10)
        DROPDOWN_MENU.current(0)
        CANCEL_BUTTON = Button(DROPDOWN_MENU_WINDOW, text='Cancel', font=('Times New Roman', 18, 'bold'), command=close_window)
        CANCEL_BUTTON.pack(side='left', padx=10, pady=10)
        CONFIRM_BUTTON = Button(DROPDOWN_MENU_WINDOW, text='Confirm', font=('Times New Roman', 18, 'bold'), command=process_selected_value)
        CONFIRM_BUTTON.pack(side='right', padx=10, pady=10)
        DROPDOWN_MENU_WINDOW.bind('<Return>', lambda event: CONFIRM_BUTTON.invoke())
        #WAIT UNTIL THE WINDOW IS DESTROYED, BEFORE RETURNING
        DROPDOWN_MENU_WINDOW.wait_window()
        return SELECTED_DROPDOWN_MENU_VALUE
    except BaseException as ERROR:
        raise Exception(f'[{ERROR.__class__.__name__ if str(ERROR).strip() else 'UnknownError'}]\nFunction: "dropdown_menu_prompt()"\n{ERROR if str(ERROR).strip() else 'An unknown error occurred!'}')

#THIS FUNCTION:
#1.) REQUIRES "tkinter.Entry()" AND "tkinter.Button()" CLASSES
#2.) SHOWS/HIDES THE INPUT VALUE OF THE "tkinter.Entry()" WIDGET AND CHANGES THE TEXT OF THE SHOW/HIDE BUTTON
def toggle_input_visibility(ENTRY_WIDGET, VISIBILITY_BUTTON):
    if not isinstance(ENTRY_WIDGET, Entry):
        raise TypeError('[TypeError]\nFunction: "toggle_input_visibility()"\nThe entry widget parameter must be a "tkinter.Entry()" type.')
    elif not isinstance(VISIBILITY_BUTTON, Button):
        raise TypeError('[TypeError]\nFunction: "toggle_input_visibility()"\nThe visibility button parameter must be a "tkinter.Button()" type.')
    try:
        if ENTRY_WIDGET.cget('show') == '':
            ENTRY_WIDGET.config(show='*')
            VISIBILITY_BUTTON.config(text='Show')
        else:
            ENTRY_WIDGET.config(show='')
            VISIBILITY_BUTTON.config(text='Hide')
    except BaseException as ERROR:
        raise Exception(f'[{ERROR.__class__.__name__ if str(ERROR).strip() else 'UnknownError'}]\nFunction: "toggle_input_visibility()"\n{ERROR if str(ERROR).strip() else 'An unknown error occurred!'}')

#THIS FUNCTION:
#1.) CAN BE TRIGGERED ON-KEY RELEASE WITH "Entry().bind('<KeyRelease>', lambda ON_KEY_UP: update_create_password_input_status(STATUS_LABEL, PASSWORD_ENTRY, CONFIRM_PASSWORD_ENTRY, CONFIRM_BUTTON, MINIMUM_PASSWORD_LENGTH))"
#2.) REQUIRES:
    #A.) A "tkinter.Label()" CLASS
    #B.) 2x "tkinter.Entry()" CLASSES
    #C.) A "tkinter.Button()" CLASS
    #D.) A MINIMUM PASSWORD LENGTH INTEGER
#3) UPDATES WHAT THE SUPPLIED STATUS LABEL DISPLAYS DYNAMICALLY
def update_create_password_input_status(STATUS_LABEL, PASSWORD_ENTRY, CONFIRM_PASSWORD_ENTRY, CONFIRM_BUTTON, MINIMUM_PASSWORD_LENGTH, ON_KEY_UP=None):
    if not isinstance(STATUS_LABEL, Label):
        raise TypeError('[TypeError]\nFunction: "update_create_password_input_status()"\nThe status label parameter must be a "tkinter.Label()" type.')
    elif not isinstance(PASSWORD_ENTRY, Entry):
        raise TypeError('[TypeError]\nFunction: "update_create_password_input_status()"\nThe password entry parameter must be a "tkinter.Entry()" type.')
    elif not isinstance(CONFIRM_PASSWORD_ENTRY, Entry):
        raise TypeError('[TypeError]\nFunction: "update_create_password_input_status()"\nThe confirm password entry parameter must be a "tkinter.Entry()" type.')
    elif not isinstance(CONFIRM_BUTTON, Button):
        raise TypeError('[TypeError]\nFunction: "update_create_password_input_status()"\nThe confirm button parameter must be a "tkinter.Button()" type.')
    elif not isinstance(MINIMUM_PASSWORD_LENGTH, int):
        raise TypeError('[TypeError]\nFunction: "update_create_password_input_status()"\nThe minimum password length parameter must be an integer type.')
    try:
        PASSWORD_VALUE = PASSWORD_ENTRY.get()
        CONFIRM_PASSWORD_VALUE = CONFIRM_PASSWORD_ENTRY.get()
        def is_ascii_only(VALUE):
            return all(CHARACTER in printable for CHARACTER in VALUE)
        ASCII_CHECK =  all([is_ascii_only(VALUE) for VALUE in [PASSWORD_VALUE, CONFIRM_PASSWORD_VALUE]])
        LENGTH_CHECK = len(PASSWORD_VALUE) >= MINIMUM_PASSWORD_LENGTH if PASSWORD_VALUE else len(CONFIRM_PASSWORD_VALUE) >= MINIMUM_PASSWORD_LENGTH
        MATCH_CHECK = PASSWORD_VALUE == CONFIRM_PASSWORD_VALUE
        IS_PASSWORD_EMPTY = True if not PASSWORD_VALUE else False
        IS_CONFIRM_PASSWORD_EMPTY = True if not CONFIRM_PASSWORD_VALUE else False
        if IS_PASSWORD_EMPTY and IS_CONFIRM_PASSWORD_EMPTY:
            STATUS_LABEL.config(text='Cannot be empty!', fg='red')
        elif not ASCII_CHECK:
            STATUS_LABEL.config(text='Contains invalid characters!', fg='red')
        elif not LENGTH_CHECK:
            STATUS_LABEL.config(text=f'{len(PASSWORD_VALUE) if PASSWORD_VALUE else len(CONFIRM_PASSWORD_VALUE)}/{MINIMUM_PASSWORD_LENGTH} characters', fg='red')
        elif any([PASSWORD_VALUE, CONFIRM_PASSWORD_VALUE]) and any([IS_PASSWORD_EMPTY, IS_CONFIRM_PASSWORD_EMPTY]):
            STATUS_LABEL.config(text='Fill both fields', fg='grey')
        elif not MATCH_CHECK:
            STATUS_LABEL.config(text='Do not match!', fg='red')
        if all([ASCII_CHECK, LENGTH_CHECK, MATCH_CHECK]):
            STATUS_LABEL.config(text='Acceptable and matching', fg='green')
            #ENABLE THE CONFIRM BUTTON IF ALL CHECKS PASS
            CONFIRM_BUTTON.config(state='normal')
        else:
            #DISABLE THE CONFIRM BUTTON IF ANY CHECKS FAIL
            CONFIRM_BUTTON.config(state='disabled')
    except BaseException as ERROR:
        raise Exception(f'[{ERROR.__class__.__name__ if str(ERROR).strip() else 'UnknownError'}]\nFunction: "update_create_password_input_status()"\n{ERROR if str(ERROR).strip() else 'An unknown error occurred!'}')

#THIS FUNCTION:
#1.) REQUIRES A "tkinter.Tk()" CLASS
#2.) OPTIONALLY ACCEPTS:
    #A.) A MINIMUM PASSWORD LENGTH INTEGER (DEFAULT IS 16)
    #B.) ICON ICO AND/OR ICON PNG FILE PATH STRING(S)
    #C.) A PROMPT TITLE STRING (DEFAULT IS "Create A Password")
#3.) DISPLAYS A CREATE PASSWORD PROMPT
#4.) RETURNS THE USER-ENTERED PASSWORD AS A BYTEARRAY OR "None" IF THE WINDOW IS CLOSED OR CANCELLED
def create_password_prompt(ROOT_WINDOW, MINIMUM_PASSWORD_LENGTH=None, ICON_ICO_FILE_PATH=None, ICON_PNG_FILE_PATH=None, PROMPT_TITLE=None):
    if not isinstance(ROOT_WINDOW, Tk):
        raise TypeError('[TypeError]\nFunction: "create_password_prompt()"\nThe root window parameter must be a "tkinter.Tk()" type.')
    elif MINIMUM_PASSWORD_LENGTH and not isinstance(MINIMUM_PASSWORD_LENGTH, int):
        raise TypeError('[TypeError]\nFunction: "create_password_prompt()"\nThe minimum password length parameter must be an integer type.')
    elif PROMPT_TITLE and not isinstance(PROMPT_TITLE, str):
        raise TypeError('[TypeError]\nFunction: "create_password_prompt()"\nThe prompt title parameter must be a string type.')
    elif system() == 'Windows' and any([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]) and not all([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]):
        raise ValueError('[ValueError]\nFunction: "create_password_prompt()"\nThe icon ico and icon png file path parameters must both be set if using an icon with this function on Windows.')
    elif system() == 'Darwin' and any([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]) and not ICON_ICO_FILE_PATH:
        raise ValueError('[ValueError]\nFunction: "create_password_prompt()"\nThe icon ico file path parameter must be set if using an icon with this function on Mac.')
    elif system() != 'Darwin' and any([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]) and not ICON_PNG_FILE_PATH:
        raise ValueError('[ValueError]\nFunction: "create_password_prompt()"\nThe icon png file path parameter must be set if using an icon with this function on an OS other than Mac.')
    elif ICON_ICO_FILE_PATH and not isabs(ICON_ICO_FILE_PATH):
        raise ValueError('[ValueError]\nFunction: "create_password_prompt()"\nThe icon ico file path parameter must be an absolute path.')
    elif ICON_PNG_FILE_PATH and not isabs(ICON_PNG_FILE_PATH):
        raise ValueError('[ValueError]\nFunction: "create_password_prompt()"\nThe icon png file path parameter must be an absolute path.')
    elif ICON_ICO_FILE_PATH and not isfile(ICON_ICO_FILE_PATH):
        raise FileNotFoundError('[FileNotFoundError]\nFunction: "create_password_prompt()"\nThe icon ico file path parameter must be a path to an existing file.')
    elif ICON_PNG_FILE_PATH and not isfile(ICON_PNG_FILE_PATH):
        raise FileNotFoundError('[FileNotFoundError]\nFunction: "create_password_prompt()"\nThe icon png file path parameter must be a path to an existing file.')
    try:
        MINIMUM_PASSWORD_LENGTH = 16 if MINIMUM_PASSWORD_LENGTH is None else MINIMUM_PASSWORD_LENGTH
        PROMPT_TITLE = 'Create A Password' if PROMPT_TITLE is None else PROMPT_TITLE
        PASSWORD_VALUE = None
        def close_window():
            #DELETE THE PASSWORD ENTRY FROM THE RAM
            PASSWORD_ENTRY.delete(0, 'end')
            #DELETE THE CONFIRM PASSWORD ENTRY FROM THE RAM
            CONFIRM_PASSWORD_ENTRY.delete(0, 'end')
            CREATE_PASSWORD_WINDOW.destroy()
        def process_password():
            nonlocal PASSWORD_VALUE
            #SET THE PASSWORD VALUE TO A BYTEARRAY, TO PREVENT RAM EXPOSURE
            PASSWORD_VALUE = bytearray(PASSWORD_ENTRY.get(), 'ascii')
            #DELETE THE PASSWORD ENTRY FROM THE RAM
            PASSWORD_ENTRY.delete(0, 'end')
            #DELETE THE CONFIRM PASSWORD ENTRY FROM THE RAM
            CONFIRM_PASSWORD_ENTRY.delete(0, 'end')
            CREATE_PASSWORD_WINDOW.destroy()
        CREATE_PASSWORD_WINDOW = Toplevel(ROOT_WINDOW)
        if ICON_ICO_FILE_PATH or ICON_PNG_FILE_PATH:
            set_window_icon(CREATE_PASSWORD_WINDOW, ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH)
        CREATE_PASSWORD_WINDOW.title(PROMPT_TITLE)
        CREATE_PASSWORD_WINDOW.resizable(False, False)
        CREATE_PASSWORD_WINDOW.protocol('WM_DELETE_WINDOW', close_window)
        CREATE_PASSWORD_WINDOW.grab_set()
        ROW_1_FRAME = Frame(CREATE_PASSWORD_WINDOW)
        ROW_1_FRAME.pack(padx=10, pady=5, anchor='center')
        Label(ROW_1_FRAME, text='Create A Password', font=('Times New Roman', 18, 'bold')).pack(padx=10, pady=10)
        PASSWORD_VISIBILITY_VARIABLE = StringVar()
        PASSWORD_ENTRY = Entry(ROW_1_FRAME, textvariable=PASSWORD_VISIBILITY_VARIABLE, show='*', font=('Times New Roman', 26, 'bold'))
        PASSWORD_ENTRY.pack(side='left', padx=(0, 10))
        #SET FOCUS ON THE PASSWORD ENTRY
        PASSWORD_ENTRY.focus_force()
        #SET THE PASSWORD VISIBILITY BUTTON
        PASSWORD_VISIBILITY_BUTTON = Button(ROW_1_FRAME, text='Show', command=lambda: toggle_input_visibility(PASSWORD_ENTRY, PASSWORD_VISIBILITY_BUTTON), font=('Times New Roman', 18, 'bold'))
        PASSWORD_VISIBILITY_BUTTON.pack(side='left')
        ROW_2_FRAME = Frame(CREATE_PASSWORD_WINDOW)
        ROW_2_FRAME.pack(padx=10, pady=5, anchor='center')
        Label(ROW_2_FRAME, text='Confirm Password', font=('Times New Roman', 18, 'bold')).pack(padx=10, pady=10)
        CONFIRM_PASSWORD_VISIBILITY_VARIABLE = StringVar()
        CONFIRM_PASSWORD_ENTRY = Entry(ROW_2_FRAME, textvariable=CONFIRM_PASSWORD_VISIBILITY_VARIABLE, show='*', font=('Times New Roman', 26, 'bold'))
        CONFIRM_PASSWORD_ENTRY.pack(side='left', padx=(0, 10))
        #SET CONFIRM PASSWORD VISIBILITY BUTTON
        CONFIRM_PASSWORD_VISIBILITY_BUTTON = Button(ROW_2_FRAME, text='Show', command=lambda: toggle_input_visibility(CONFIRM_PASSWORD_ENTRY, CONFIRM_PASSWORD_VISIBILITY_BUTTON), font=('Times New Roman', 18, 'bold'))
        CONFIRM_PASSWORD_VISIBILITY_BUTTON.pack(side='left')
        #SET A PASSWORD CHECK STATUS LABEL
        STATUS_LABEL = Label(CREATE_PASSWORD_WINDOW, text=None, anchor='s', font=('Times New Roman', 14, 'bold'))
        STATUS_LABEL.pack(pady=(5, 10))
        ROW_3_FRAME = Frame(CREATE_PASSWORD_WINDOW)
        ROW_3_FRAME.pack(pady=10, fill='x')
        CANCEL_BUTTON = Button(ROW_3_FRAME, text='Cancel', command=close_window, font=('Times New Roman', 18, 'bold'))
        CANCEL_BUTTON.pack(side='left', padx=10)
        CONFIRM_BUTTON = Button(ROW_3_FRAME, text='Confirm', state='disabled', command=process_password, font=('Times New Roman', 18, 'bold'))
        CONFIRM_BUTTON.pack(side='right', padx=10)
        #UPDATE THE STATUS LABEL ON-KEY UP
        PASSWORD_ENTRY.bind('<KeyRelease>', lambda ON_KEY_UP: update_create_password_input_status(STATUS_LABEL, PASSWORD_ENTRY, CONFIRM_PASSWORD_ENTRY, CONFIRM_BUTTON, MINIMUM_PASSWORD_LENGTH))
        CONFIRM_PASSWORD_ENTRY.bind('<KeyRelease>', lambda ON_KEY_UP: update_create_password_input_status(STATUS_LABEL, PASSWORD_ENTRY, CONFIRM_PASSWORD_ENTRY, CONFIRM_BUTTON, MINIMUM_PASSWORD_LENGTH))
        #ALLOW CONFIRM BUTTON ON-ENTER KEY PRESS
        CREATE_PASSWORD_WINDOW.bind('<Return>', lambda ON_ENTER: CONFIRM_BUTTON.invoke())
        CREATE_PASSWORD_WINDOW.wait_window()
        return PASSWORD_VALUE
    except BaseException as ERROR:
        raise Exception(f'[{ERROR.__class__.__name__ if str(ERROR).strip() else 'UnknownError'}]\nFunction: "create_password_prompt()"\n{ERROR if str(ERROR).strip() else 'An unknown error occurred!'}')

#THIS FUNCTION:
#1.) CAN BE TRIGGERED, ON-KEY RELEASE WITH "ENTRY_VARIABLE.bind('<KeyRelease>', lambda ON_KEY_UP: update_enter_password_input_status(STATUS_LABEL, PASSWORD_ENTRY, CONFIRM_BUTTON))"
#2.) REQUIRES:
    #A.) A "tkinter.Label()"
    #B.) A "tkinter.Entry()"
    #C.) A "tkinter.Button()"
#3.) UPDATES WHAT THE SUPPLIED PASSWORD STATUS LABEL DISPLAYS
def update_enter_password_input_status(STATUS_LABEL, PASSWORD_ENTRY, CONFIRM_BUTTON, ON_KEY_UP=None):
    if not isinstance(STATUS_LABEL, Label):
        raise TypeError('[TypeError]\nFunction: "update_enter_password_input_status()"\nThe status label parameter must be a "tkinter.Label()" type.')
    elif not isinstance(PASSWORD_ENTRY, Entry):
        raise TypeError('[TypeError]\nFunction: "update_enter_password_input_status()"\nThe password entry parameter must be a "tkinter.Entry()" type.')
    elif not isinstance(CONFIRM_BUTTON, Button):
        raise TypeError('[TypeError]\nFunction: "update_enter_password_input_status()"\nThe confirm button parameter must be a "tkinter.Button()" type.')
    try:
        PASSWORD_VALUE = PASSWORD_ENTRY.get()
        ASCII_CHECK =  all(CHARACTER in printable for CHARACTER in PASSWORD_VALUE)
        if not PASSWORD_VALUE:
            STATUS_LABEL.config(text='Cannot be empty!', fg='red')
        elif not ASCII_CHECK:
            STATUS_LABEL.config(text='Contains invalid characters!', fg='red')
        else:
            STATUS_LABEL.config(text='')
        if not PASSWORD_VALUE or not ASCII_CHECK:
            CONFIRM_BUTTON.config(state='disabled')
        else:
            CONFIRM_BUTTON.config(state='normal')
    except BaseException as ERROR:
        raise Exception(f'[{ERROR.__class__.__name__ if str(ERROR).strip() else 'UnknownError'}]\nFunction: "update_enter_password_input_status()"\n{ERROR if str(ERROR).strip() else 'An unknown error occurred!'}')

#THIS FUNCTION:
#1.) REQUIRES A "tkinter.Tk()" CLASS
#2.) OPTIONALLY ACCEPTS:
    #A.) ICON ICO AND/OR ICON PNG FILE PATH STRING(S)
    #B.) PROMPT TITLE STRING (DEFAULT IS "Enter Password")
#3.) DISPLAYS AN ENTER PASSWORD PROMPT
#4.) RETURNS THE USER-ENTERED PASSWORD AS A BYTEARRAY OR "None" IF THE WINDOW IS CLOSED OR CANCELLED
def enter_password_prompt(ROOT_WINDOW, ICON_ICO_FILE_PATH=None, ICON_PNG_FILE_PATH=None, PROMPT_TITLE=None):
    if not isinstance(ROOT_WINDOW, Tk):
        raise TypeError('[TypeError]\nFunction: "enter_password_prompt()"\nThe root window parameter must be a "tkinter.Tk()" type.')
    elif PROMPT_TITLE and not isinstance(PROMPT_TITLE, str):
        raise TypeError('[TypeError]\nFunction: "enter_password_prompt()"\nThe prompt title parameter must be a string type.')
    elif system() == 'Windows' and any([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]) and not all([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]):
        raise ValueError('[ValueError]\nFunction: "enter_password_prompt()"\nThe icon ico and icon png file path parameters must both be set if using an icon with this function on Windows.')
    elif system() == 'Darwin' and any([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]) and not ICON_ICO_FILE_PATH:
        raise ValueError('[ValueError]\nFunction: "enter_password_prompt()"\nThe icon ico file path parameter must be set if using an icon with this function on Mac.')
    elif system() != 'Darwin' and any([ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH]) and not ICON_PNG_FILE_PATH:
        raise ValueError('[ValueError]\nFunction: "enter_password_prompt()"\nThe icon png file path parameter must be set if using an icon with this function on an OS other than Mac.')
    elif ICON_ICO_FILE_PATH and not isabs(ICON_ICO_FILE_PATH):
        raise ValueError('[ValueError]\nFunction: "enter_password_prompt()"\nThe icon ico file path parameter must be an absolute path.')
    elif ICON_PNG_FILE_PATH and not isabs(ICON_PNG_FILE_PATH):
        raise ValueError('[ValueError]\nFunction: "enter_password_prompt()"\nThe icon png file path parameter must be an absolute path.')
    elif ICON_ICO_FILE_PATH and not isfile(ICON_ICO_FILE_PATH):
        raise FileNotFoundError('[FileNotFoundError]\nFunction: "enter_password_prompt()"\nThe icon ico file path parameter must be a path to an existing file.')
    elif ICON_PNG_FILE_PATH and not isfile(ICON_PNG_FILE_PATH):
        raise FileNotFoundError('[FileNotFoundError]\nFunction: "enter_password_prompt()"\nThe icon png file path parameter must be a path to an existing file.')
    try:
        PROMPT_TITLE = 'Enter Password' if PROMPT_TITLE is None else PROMPT_TITLE
        PASSWORD_VALUE = None
        def close_window():
            #DELETE THE PASSWORD ENTRY FROM THE RAM
            PASSWORD_ENTRY.delete(0, 'end')
            ENTER_PASSWORD_WINDOW.destroy()
        def process_password():
            nonlocal PASSWORD_VALUE
            #SET THE PASSWORD VALUE TO A BYTEARRAY, TO PREVENT RAM EXPOSURE
            PASSWORD_VALUE = bytearray(PASSWORD_ENTRY.get(), 'ascii')
            #DELETE THE PASSWORD ENTRY FROM THE RAM
            PASSWORD_ENTRY.delete(0, 'end')
            ENTER_PASSWORD_WINDOW.destroy()
        ENTER_PASSWORD_WINDOW = Toplevel(ROOT_WINDOW)
        if ICON_ICO_FILE_PATH or ICON_PNG_FILE_PATH:
            set_window_icon(ENTER_PASSWORD_WINDOW, ICON_ICO_FILE_PATH, ICON_PNG_FILE_PATH)
        ENTER_PASSWORD_WINDOW.title(PROMPT_TITLE)
        ENTER_PASSWORD_WINDOW.resizable(False, False)
        ENTER_PASSWORD_WINDOW.protocol('WM_DELETE_WINDOW', close_window)
        ENTER_PASSWORD_WINDOW.grab_set()
        ROW_1_FRAME = Frame(ENTER_PASSWORD_WINDOW)
        ROW_1_FRAME.pack(padx=10, pady=5, anchor='center')
        Label(ROW_1_FRAME, text='Enter Password', font=('Times New Roman', 18, 'bold')).pack(padx=10, pady=10)
        PASSWORD_VISIBILITY_VARIABLE = StringVar()
        PASSWORD_ENTRY = Entry(ROW_1_FRAME, textvariable=PASSWORD_VISIBILITY_VARIABLE, show='*', font=('Times New Roman', 26, 'bold'))
        PASSWORD_ENTRY.pack(side='left', padx=(0, 10))
        PASSWORD_ENTRY.focus_force()
        PASSWORD_VISIBILITY_BUTTON = Button(ROW_1_FRAME, text='Show', command=lambda: toggle_input_visibility(PASSWORD_ENTRY, PASSWORD_VISIBILITY_BUTTON), font=('Times New Roman', 18, 'bold'))
        PASSWORD_VISIBILITY_BUTTON.pack(side='left')
        #SET A PASSWORD CHECK STATUS LABEL
        STATUS_LABEL = Label(ENTER_PASSWORD_WINDOW, font=('Times New Roman', 14, 'bold'), fg='grey')
        STATUS_LABEL.pack(pady=(5, 10))
        ROW_2_FRAME = Frame(ENTER_PASSWORD_WINDOW)
        ROW_2_FRAME.pack(pady=10, fill='x')
        CANCEL_BUTTON = Button(ROW_2_FRAME, text='Cancel', command=close_window, font=('Times New Roman', 18, 'bold'))
        CANCEL_BUTTON.pack(side='left', padx=10)
        CONFIRM_BUTTON = Button(ROW_2_FRAME, text='Confirm', state='disabled', command=process_password, font=('Times New Roman', 18, 'bold'))
        CONFIRM_BUTTON.pack(side='right', padx=10)
        #UPDATE THE STATUS LABEL ON-KEY UP
        PASSWORD_ENTRY.bind('<KeyRelease>', lambda ON_KEY_UP: update_enter_password_input_status(STATUS_LABEL, PASSWORD_ENTRY, CONFIRM_BUTTON))
        #ALLOW CONFIRM BUTTON ON-ENTER KEY PRESS
        ENTER_PASSWORD_WINDOW.bind('<Return>', lambda ON_ENTER: CONFIRM_BUTTON.invoke())
        ENTER_PASSWORD_WINDOW.wait_window()
        return PASSWORD_VALUE
    except BaseException as ERROR:
        raise Exception(f'[{ERROR.__class__.__name__ if str(ERROR).strip() else 'UnknownError'}]\nFunction: "enter_password_prompt()"\n{ERROR if str(ERROR).strip() else 'An unknown error occurred!'}')
    
#THIS FUNCTION:
#1.) OPTIONALLY ACCEPTS PROMPT TITLE AND/OR PROMPT PATH STRING(S)
#2.) PROMPTS THE USER TO CHOOSE A FOLDER PATH
#3.) RETURNS THE FOLDER PATH THAT WAS CHOSEN AS A STRING OR "None" IF THE WINDOW IS CLOSED OR CANCELLED
def folder_path_prompt(PROMPT_TITLE=None, PROMPT_PATH=None):
    if PROMPT_TITLE and not isinstance(PROMPT_TITLE, str):
        raise TypeError('[TypeError]\nFunction: "folder_path_prompt()"\nThe prompt title parameter must be a string type.')
    elif PROMPT_PATH and not isabs(PROMPT_PATH):
        raise ValueError('[ValueError]\nFunction: "folder_path_prompt()"\nThe prompt path parameter must be an absolute path.')
    elif PROMPT_PATH and not isdir(PROMPT_PATH):
        raise NotADirectoryError('[NotADirectoryError]\nFunction: "folder_path_prompt()"\nThe prompt path parameter must be a path to an existing folder.')
    try:
        PROMPT_TITLE = 'Choose A Folder' if PROMPT_TITLE is None else PROMPT_TITLE
        PROMPT_PATH = expanduser('~') if PROMPT_PATH is None else PROMPT_PATH
        PATH = filedialog.askdirectory(
            title=PROMPT_TITLE,
            initialdir=PROMPT_PATH
        )
        if not PATH:
            PATH = None
        return PATH
    except BaseException as ERROR:
        raise Exception(f'[{ERROR.__class__.__name__ if str(ERROR).strip() else UnknownError}]\nFunction: "folder_path_prompt()"\n{ERROR if str(ERROR).strip() else 'An unknown error occurred!'}')

#THIS FUNCTION:
#1.) OPTIONALLY ACCEPTS:
    #A.) PROMPT TITLE AND/OR PROMPT PATH STRING(S)
    #B.) A FILE TYPES LIST
    #FORMAT: [('Text Files', '*.txt'), ('Python Files', '*.py')]
#2.) PROMPTS THE USER TO CHOOSE A FILE PATH
#3.) RETURNS THE FILE PATH THAT WAS CHOSEN AS A STRING OR "None" IF THE WINDOW IS CLOSED OR CANCELLED
def file_path_prompt(PROMPT_TITLE=None, PROMPT_PATH=None, FILE_TYPES=None):
    if PROMPT_TITLE and not isinstance(PROMPT_TITLE, str):
        raise TypeError('[TypeError]\nFunction: "file_path_prompt()"\nThe prompt title parameter must be a string type.')
    elif FILE_TYPES and not isinstance(FILE_TYPES, list):
        raise TypeError('[TypeError]\nFunction: "file_path_prompt()"\nThe file types parameter must be a list type.')
    elif PROMPT_PATH and not isabs(PROMPT_PATH):
        raise ValueError('[ValueError]\nFunction: "file_path_prompt()"\nThe prompt path parameter must be an absolute path.')
    elif PROMPT_PATH and not isdir(PROMPT_PATH):
        raise NotADirectoryError('[NotADirectoryError]\nFunction: "file_path_prompt()"\nThe prompt path parameter must be a path to an existing folder.')
    try:
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
        return PATH
    except BaseException as ERROR:
        raise Exception(f'[{ERROR.__class__.__name__ if str(ERROR).strip() else 'UnknownError'}]\nFunction: "file_path_prompt()"\n{ERROR if str(ERROR).strip() else 'An unknown error occurred!'}')

#THIS FUNCTION:
#1.) REQUIRES A "tkinter.Tk()" CLASS
#2.) RETURNS A LIST CONTAINING: 
    #A.) A "tkinter.Toplevel()" CLASS
    #B.) A "tkinter.Label()" CLASS (FOR MESSAGES)
    #C.) A "ttk.Progressbar()" CLASS (FOR PROGRESSBAR)
    #D.) A "tkinter.Label()" (FOR PERCENTAGE)
def progressbar_window(ROOT_WINDOW):
    if not isinstance(ROOT_WINDOW, Tk):
        raise TypeError('[TypeError]\nFunction: "progressbar_window()"\nThe root window parameter must be a "tkinter.Tk()" type.')
    try:
        PROGRESSBAR_WINDOW = Toplevel(ROOT_WINDOW)
        #HIDE THE WINDOW TITLE BAR
        PROGRESSBAR_WINDOW.overrideredirect(True)
        PROGRESSBAR_WINDOW.resizable(False, False)
        PROGRESSBAR_STYLE = ttk.Style()
        PROGRESSBAR_STYLE.theme_use('default')
        PROGRESSBAR_STYLE.configure('Green.Horizontal.TProgressbar', thickness=38, background='#5CB85C', relief='raised')
        ROW_1_FRAME = Frame(PROGRESSBAR_WINDOW)
        ROW_1_FRAME.pack()
        PROGRESSBAR_MESSAGE = Label(ROW_1_FRAME, text=None, font=('Times New Roman', 18, 'bold'), wraplength=465)
        PROGRESSBAR_MESSAGE.pack(padx=10, pady=(10, 0))
        ROW_2_FRAME = Frame(PROGRESSBAR_WINDOW)
        ROW_2_FRAME.pack()
        PROGRESSBAR = ttk.Progressbar(ROW_2_FRAME, length=400, mode='determinate', style='Green.Horizontal.TProgressbar')
        PROGRESSBAR.pack(padx=(10, 0), pady=10, side='left')
        PROGRESSBAR_PERCENTAGE = Label(ROW_2_FRAME, text=None, font=('Times New Roman', 18, 'bold'))
        PROGRESSBAR_PERCENTAGE.pack(padx=10, side='left')
        return PROGRESSBAR_WINDOW, PROGRESSBAR_MESSAGE, PROGRESSBAR, PROGRESSBAR_PERCENTAGE
    except BaseException as ERROR:
        raise Exception(f'[{ERROR.__class__.__name__ if str(ERROR).strip() else 'UnknownError'}]\nFunction: "progressbar_window()"\n{ERROR if str(ERROR).strip() else 'An unknown error occurred!'}')
