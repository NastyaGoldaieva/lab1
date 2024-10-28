from copress import compress
from decompress import decompress


def main():
    while True:
        print("Wellcome to the archivator")
        hol = input("Chose Compres[f] or Decompress[d] [x]-exit ")
        if hol == 'f':
            print("chose compression")
            compress()
        elif hol == 'd':
            print("Chosen decompression")
            decompress()
        elif hol == 'x':
            break

        else:
            print("incorrect input, try again")
            main()
    return
if __name__ == '__main__':
    main()
