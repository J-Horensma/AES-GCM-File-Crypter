.aes_gcm_file_crypter import main as gui_main

def main():
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--version', action='store_true')
    ARGUMENTS = PARSER.parse_args()

    if ARGUMENTS.version:
        print(__version__)
        return

    gui_main()

if __name__ == '__main__':
    main()
