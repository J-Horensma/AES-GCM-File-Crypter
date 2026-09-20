![Preview](assets/icon/ico/256x256.ico)

# AES-GCM File-Crypter
<br></br>

## About
This application includes both a GUI and a CLI edition for securely encrypting or decrypting files and/or entire folders using AES‑GCM cryptography, along with forensic recovery‑prevention features. \
</br>

## Why AES-GCM Cryptography?
AES-GCM Cryptography is one of the most secure and modern approaches for encryption and decryption. It supports three key sizes (128, 192, and 256 bits). \
</br>

## What Are The Forensic Recovery-Prevention Features?:

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

## Usage (Windows): 

### 1.) Select encryption or decryption options  

![Preview](assets/previews/windows_preview_1.png)
![Preview](assets/previews/windows_preview_2.png)
![Preview](assets/previews/windows_preview_3.png)  

### 2.) Enter the password  

![Preview](assets/previews/windows_preview_4.png)  

### 3.) Encrypt or decrypt a file or an entire folder  
<br></br>

## Usage (Linux):

### 1.) Select encryption or decryption options  

![Preview](assets/previews/linux_preview_1.png)
![Preview](assets/previews/linux_preview_2.png)
![Preview](assets/previews/linux_preview_3.png)  

### 2.) Enter the password  

![Preview](assets/previews/linux_preview_4.png)  

### 3.) Encrypt or decrypt a file or an entire folder  
<br></br>

## Compile, Yourself (Optional):  

### Windows:
1.) Ensure the latest Python, PyInstaller, and any required dependencies are installed. \

2.) Open a terminal, navigate to this file’s directory, and run: \
```python -m PyInstaller --clean --noconfirm --onefile --windowed --icon=assets/icon/ico/icon.ico --add-data "assets;assets" "AES-GCM File-Crypter.pyw"```  

### Linux:
1.) Ensure the latest Python, PyInstaller, and any required dependencies are installed. \

2.) Open a terminal, navigate to this file’s directory, and run: \
```python -m PyInstaller --clean --noconfirm --onefile --windowed --icon="assets/icon/ico/icon.ico" --add-data "assets:assets" --hidden-import=_cffi_backend --collect-binaries cffi --collect-data cffi "AES-GCM File-Crypter.pyw"```
s
