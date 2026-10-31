![Preview](assets/icon/ico/256x256.ico)

# AES-GCM File-Crypter 1.0.0 (Standard)
<br></br>

## About
A CLI for securely encrypting or decrypting files and/or entire folders using AES-GCM cryptography with basic forensic recovery-prevention features.
</br>

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

## CLI Usage (Python):
1.) For CLI instructions:
* ```python -m aes_gcm_file_crypter --help```

2.) For detailed instructions of each function:
* ```python -m aes_gcm_file_crypter encrypt_folder --help```
* ```python -m aes_gcm_file_crypter decrypt_folder --help```
* ```python -m aes_gcm_file_crypter encrypt_file --help```
* ```python -m aes_gcm_file_crypter decrypt_file --help```

## Project Page
[https://github.com/J-Horensma/AES-GCM-File-Crypter](https://github.com/J-Horensma/AES-GCM-File-Crypter)