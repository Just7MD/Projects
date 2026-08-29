# very basic hash cracker
import hashlib as hl
import argparse as ap
from sys import exit

parser = ap.ArgumentParser("basic web fuzzer")
parser.add_argument("-H", "--hash")
parser.add_argument("-w", "--wordlist")
parser.add_argument("-f", "--format")
args = parser.parse_args()

hash = args.hash.strip()
wordlist = args.wordlist
format = args.format.strip()

if not hash or not wordlist or not format:
    print("hash, wordlist or format parameter is missing\n")
    parser.print_help()
    exit()

try:
    with open(wordlist, "r") as wl:
        for word in wl:
            word.strip()
            print(f"trying: {word}", end="")
            if hl.new(format, word.encode()).hexdigest().strip() == hash:
                print(f"\n\ncracked! {hash} is {word}")
                exit()
        print("could not crack the hash")
except FileNotFoundError:
    print("could not open the specified wordlist")
    exit()