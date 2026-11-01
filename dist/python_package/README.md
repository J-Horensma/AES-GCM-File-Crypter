# AES-GCM File-Crypter CLI (Standard) 1.0.1
<br></br>

## About
A CLI for securely encrypting or decrypting entire folder/s or a single file using AES-GCM cryptography with basic forensic recovery-prevention features.
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

## CLI Usage:
1.) For CLI instructions, use the following command.
* ```python -m aes_gcm_file_crypter --help```

2.) For detailed instructions of each function:
* ```python -m aes_gcm_file_crypter encrypt_folder --help```
* ```python -m aes_gcm_file_crypter decrypt_folder --help```
* ```python -m aes_gcm_file_crypter encrypt_file --help```
* ```python -m aes_gcm_file_crypter decrypt_file --help```

3.) To start the GUI from the CLI, use the following command.
* ```python -m aes_gcm_file_crypter```

## Visit The Github Repository For This GUI And CLI
[https://github.com/J-Horensma/AES-GCM-File-Crypter](https://github.com/J-Horensma/AES-GCM-File-Crypter)
