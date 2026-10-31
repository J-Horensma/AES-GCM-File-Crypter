![Preview](assets/icon/ico/256x256.ico)

# AES-GCM File-Crypter 1.0.0 (Standard)
<br></br>

## About
The Standard edition of this application has a GUI and a CLI for securely encrypting or decrypting files and/or entire folders with AES-GCM cryptography and forensic recovery-prevention features. The Standard edition GUI and CLI will continue to remain free, source-available, and maintained with updates when necessary.
</br>

Please note:
* A Forensic edition GUI will be released soon that includes a KDF iterations drop-down option and an OS-specific metadata wipe screen to wipe all traces of the original file's content before encryption from the device being used, at a price of $20 CAD/copy.
* A Pro edition including the Forensic edition GUI and an upgraded CLI with the OS-specific metadata wipe option will be released, at a price of $50 CAD/copy.
* A Pro+ edition may later be released as well that will wipe metadata from a disk or USB and reformat it so no data is left before copying encrypted files to it, at a price of $100/copy. 
<br></br>

## Why Choose AES-GCM Cryptography?
AES-GCM Cryptography is one of the most secure and modern approaches for encryption and decryption. It supports three key sizes (128, 192, and 256 bits).
<br></br>

## Forensic Recovery-Prevention Features:

### 1.) RAM Data-Recovery Prevention
During encryption or decryption, any sensitive data, that would normally remain in the device's RAM until the application closes, is immediately cleared once the operation finishes.

This feature is designed to prevent recovery of processed data from the device’s RAM.

### 2.) Disk Data-Recovery Prevention
After encryption or decryption:
* A temporary file is created to hold the processed data.
* The original file is overwritten with random bytes and then deleted.
* The temporary file is renamed to the original file’s name.
  
This feature is designed to prevent recovery of the original file’s contents from the device’s disk.
<br></br>

## GUI Install (Windows)
```NOT YET AVAILABLE```
<br></br>

## GUI Usage (Windows):
The GUI for Windows will be coming soon to the Microsoft store.
The CLI for Windows will be coming soon to pip that includes a GUI.
<br></br>

### 1.) Select a folder or file to encrypt or decrypt

![Preview](assets/previews/windows_home_screen.png)
![Preview](assets/previews/windows_choose_path.png)

### 2.) Create or enter the password  

![Preview](assets/previews/windows_create_password.png)
![Preview](assets/previews/windows_enter_password.png)  

### 3.) Choose a key-size (If encrypting)

![Preview](assets/previews/windows_choose_key_size.png)

### 4.) Wait for the progressbar to finish and that's it!

![Preview](assets/previews/windows_gui_progressbar.png)

<br></br>

## GUI Install (Linux)
```NOT YET AVAILABLE```
<br></br>

## GUI Usage (Linux):
The CLI for Linux will be coming soon to pip that includes a GUI.
<br></br>

### 1.) Select a folder or file to encrypt or decrypt

![Preview](assets/previews/linux_home_screen.png)
![Preview](assets/previews/linux_choose_path.png)

### 2.) Create or enter the password  

![Preview](assets/previews/linux_create_password.png)  
![Preview](assets/previews/linux_enter_password.png)

### 3.) Choose a key-size (If encrypting)

![Preview](assets/previews/linux_choose_key_size.png)

### 4.) Wait for the progressbar to finish and that's it!

![Preview](assets/previews/linux_gui_progressbar.png)

<br></br>

## GUI Install (Mac)
```NOT YET AVAILABLE```
<br></br>

## GUI Usage (Mac):
While untested, this application has been developed with all OS', for PC, in mind and might work for Mac. If this application does work on Mac, while the look might be different, the usage instructions are the same across all OS', so look at the instructions for Windows or Linux above.
<br></br>

## Compile From Source (Optional):  

### Windows:
1.) Ensure the latest Python, PyInstaller, and any required dependencies are installed.

2.) Open a terminal, navigate to this file’s directory, and run:
```python -m PyInstaller --clean --noconfirm --onefile --windowed --icon=assets/icon/ico/icon.ico --add-data "assets;assets" "AES-GCM File-Crypter.pyw"```  

### Linux:
1.) Ensure the latest Python, PyInstaller, and any required dependencies are installed.

2.) Open a terminal, navigate to this file’s directory, and run:
* ```python -m PyInstaller --clean --noconfirm --onefile --windowed --icon="assets/icon/ico/icon.ico" --add-data "assets:assets" --hidden-import=_cffi_backend --collect-binaries cffi --collect-data cffi "AES-GCM File-Crypter.pyw"```

### Mac:
This application is untested on Mac but may work, if so, look up how to compile a python application with pyinstaller on Mac and compile this project into a ".dmg" file.
<br></br>

## CLI INSTALL:
```NOT YET AVAILABLE```
<br></br>

## CLI Usage:
1.) For CLI instructions:
* ```python -m aes_gcm_file_crypter --help```

2.) For further instructions:
* ```python -m aes_gcm_file_crypter encrypt_folder --help```
* ```python -m aes_gcm_file_crypter decrypt_folder --help```
* ```python -m aes_gcm_file_crypter encrypt_file --help```
* ```python -m aes_gcm_file_crypter decrypt_file --help```
