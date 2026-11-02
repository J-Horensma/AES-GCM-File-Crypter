![Preview](assets/icon/ico/256x256.ico)

# AES-GCM File-Crypter (Standard) 1.0.1
<br></br>
![Preview](assets/previews/windows/gui_progressbar.png)
<br></br>

## About
This application has a GUI and a CLI for securely encrypting or decrypting entire folder/s or a single file using AES-GCM cryptography with basic forensic recovery-prevention features. The Standard edition GUI and CLI will continue to remain free, source-available, and maintained with updates when necessary.
<br></br>

## Features:
* Cross-platform support
* GUI and CLI interfaces
* AES-GCM authenticated encryption
* RAM and disk file-data forensic recovery-prevention
* Entire folder or single file processing
* Multi-threaded processing
* Real-time progress reporting with percentage and ETA
<br></br>

## Forensic Recovery-Prevention Features:

### 1.) RAM Data-Recovery Prevention
During encryption or decryption, any sensitive data, that would normally remain in the device's RAM until the application closes, is immediately cleared once the operation finishes.

This feature is designed to reduce the likelihood of recovering sensitive data from system RAM after processing.

### 2.) Disk Data-Recovery Prevention
After encryption or decryption:
* A temporary file is created to hold the processed data.
* The original file is overwritten with random bytes and then deleted.
* The temporary file is renamed to the original file’s name.

This feature is designed to reduce the likelihood of recovering the original file contents from the device's disk.
<br></br>

## GUI Install (Windows)
The GUI for Windows will be coming soon to the Microsoft Store. \
The CLI that includes a GUI can be downloaded via Python's pip (See the CLI section).
<br></br>

## GUI Usage (Windows):

### 1.) Select a folder or file to encrypt or decrypt
![Preview](assets/previews/windows/home_screen.png)
![Preview](assets/previews/windows/choose_path.png)

### 2.) Choose a key-size (If encrypting)
![Preview](assets/previews/windows/choose_key_size.png)

### 3.) Create or enter the password
![Preview](assets/previews/windows/create_password.png)
![Preview](assets/previews/windows/enter_password.png)

### 4.) Wait for the progressbar to finish and that's it!
![Preview](assets/previews/windows/gui_progressbar.png)
![Preview](assets/previews/windows/finished_process.png)
<br></br>

## GUI Install (Linux)
The CLI that includes a GUI can be downloaded via Python's pip (See the CLI section).
<br></br>

## GUI Usage (Linux):

### 1.) Select a folder or file to encrypt or decrypt
![Preview](assets/previews/linux/home_screen.png)
![Preview](assets/previews/linux/choose_path.png)

### 2.) Choose a key-size (If encrypting)
![Preview](assets/previews/linux/choose_key_size.png)

### 3.) Create or enter the password
![Preview](assets/previews/linux/create_password.png)
![Preview](assets/previews/linux/enter_password.png)

### 4.) Wait for the progressbar to finish and that's it!
![Preview](assets/previews/linux/gui_progressbar.png)
![Preview](assets/previews/linux/finished_process.png)
<br></br>

## GUI Install (Mac)
```UNTESTED```
<br></br>

## GUI Usage (Mac):
```UNTESTED```
<br></br>

## Compile From Source (Optional):  

### Windows:
1.) Ensure the latest Python, PyInstaller, and any required dependencies are installed. \
2.) Open a terminal, navigate to this file’s directory, and use the following command.
```
python -m PyInstaller --clean --noconfirm --onefile --windowed --icon=assets/icon/ico/icon.ico --add-data "assets;assets" "AES-GCM File-Crypter.pyw"
```  

### Linux:
1.) Ensure the latest Python, PyInstaller, and any required dependencies are installed. \
2.) Open a terminal, navigate to this file’s directory, and use the following command.
```
python -m PyInstaller --clean --noconfirm --onefile --windowed --icon="assets/icon/ico/icon.ico" --add-data "assets:assets" --hidden-import=_cffi_backend --collect-binaries cffi --collect-data cffi "AES-GCM File-Crypter.pyw"
```

### Mac:
```UNTESTED```
<br></br>

## CLI Global Install For All OS' From PyPi ("pip"):
### 1.) Ensure the latest Python is installed.
### 2.) Open a terminal and use the following command.
```
pip install aes-gcm-file-crypter==1.0.1
```

## CLI Local Install Package For All OS' In The "/dist/python_package" Directory:
### 1.) Ensure the latest Python is installed.
### 2.) Open a terminal and use the following commands to start the CLI in a virtual environment:
```
cd /path/to/dist/python_package
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```
<br></br>

## Visit The PyPi Repository For This CLI
[https://pypi.org/project/aes-gcm-file-crypter/](https://pypi.org/project/aes-gcm-file-crypter/)
<br></br>

## CLI Usage For All OS':
### 1.) For general CLI instructions use the following command.
```
python -m aes_gcm_file_crypter --help
```
### 2.) For detailed instructions of each function use the following:
```
python -m aes_gcm_file_crypter encrypt_folder --help
```
```
python -m aes_gcm_file_crypter decrypt_folder --help
```
```
python -m aes_gcm_file_crypter encrypt_file --help
```
```
python -m aes_gcm_file_crypter decrypt_file --help
```
### 3.) To start the GUI from the CLI, use the following command.
```
python -m aes_gcm_file_crypter
```
<br></br>

## Please Note:
* A Forensic edition GUI will be released soon that includes a KDF iterations drop-down option and OS-specific metadata-removal features designed to reduce recoverable metadata traces of the original file, at a price of $20 CAD/copy.
* A Pro edition including the Forensic edition GUI and an upgraded CLI with the new features added will be released, at a price of $50 CAD/copy.
* A Pro+ edition may later be released that will include all the features of the Pro edition plus an option to securely erase supported metadata from a storage device before re-formatting the device and copying encrypted files to it, at a price of $100 CAD/copy.
