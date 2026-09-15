![Preview](assets/icon/ico/256x256.ico)

# AES-GCM File-Crypter
<br></br>

## About This Application
This is a GUI application, for securely encrypting/decrypting files and/or entire folders, with AES-GCM cryptography and forensic recovery prevention features. \
</br>

## What Is AES-GCM Cryptography?
AES-GCM Cryptography, is the most secure and modern approach for encryption/decryption and has 3 options (128, 192, and 256 bit). \
</br>

## What Are The Forensic Recovery Prevention Features Of This Application?:

### 1.) RAM Data Recovery Prevention
When encrypting/decrypting with this application, data normally stored, in the computer's RAM, until an application is closed, is immediately removed, after the encryption/decryption is finished. \
This feature, is designed to prevent recovery of data, from the RAM, of the device using this application.

### 2.) Disk Data Recovery Prevention
After the encryption/decryption step, a temporary file is made, where the encrypted/decrypted data is copied to, then the temporary file, is re-named to the original file's name, after the original file's deletion. The original file, is over-written with random bytes, then deleted, and the temporary file, is re-named to the original file's name, as previously mentioned. \
This feature, is designed to prevent recovery of the original file's content, from the disk of the device using this application. \
<br></br>

## Usage (Windows): 

### 1.) Pick encryption/decryption options  

![Preview](assets/previews/windows_preview_1.png)
![Preview](assets/previews/windows_preview_2.png)
![Preview](assets/previews/windows_preview_3.png)  

### 2.) Enter the password  

![Preview](assets/previews/windows_preview_4.png)  

### 3.) Encrypt/decrypt a file or an entire folder  
<br></br>

## Usage (Linux):

### 1.) Pick encryption/decryption options  

![Preview](assets/previews/linux_preview_1.png)
![Preview](assets/previews/linux_preview_2.png)
![Preview](assets/previews/linux_preview_3.png)  

### 2.) Enter the password  

![Preview](assets/previews/linux_preview_4.png)  

### 3.) Encrypt/decrypt a file or an entire folder  
<br></br>

## Compile, Yourself (Optional):  

### Windows:
1.) Make sure the latest python, PyInstaller, and any missing requirements are installed, \
then open a terminal and change directory to this file's directory, before entering the following shellcode

2.) ```python -m PyInstaller --clean --noconfirm --onefile --windowed --icon=assets/icon/ico/icon.ico --add-data "assets;assets" "AES-GCM File-Crypter.pyw"```  

### Linux:
1.) Make sure the latest python, PyInstaller, and any missing requirements are installed, \
then open a terminal and change directory to this file's directory, before entering the following shellcode

2.) ```python -m PyInstaller --clean --noconfirm --onefile --windowed --icon="assets/icon/ico/icon.ico" --add-data "assets:assets" --hidden-import=_cffi_backend --collect-binaries cffi --collect-data cffi "AES-GCM File-Crypter.pyw"```
