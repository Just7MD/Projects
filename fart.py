import requests as rq
import argparse as ap
from string import ascii_letters, punctuation
from urllib.parse import parse_qs
from sys import exit

parser = ap.ArgumentParser("basic web fuzzer")
parser.add_argument("-u", "--url")
parser.add_argument("-w", "--wordlist")
parser.add_argument("-m", "--method")
parser.add_argument("-H", "--headers")
parser.add_argument("-d", "--data")
parser.add_argument("-b", "--blacklist")
args = parser.parse_args()


def parse_headers(raw):
    headers = {}
    for pair in raw.split(","):
        if ":" in pair:
            key, value = pair.split(":", 1)
            headers[key.strip()] = value.strip()
    return headers

url = args.url
wordlist = args.wordlist
method = args.method
headers = args.headers
data = args.data

if url is None or wordlist is None:
    print("url or wordlist parameter is missing")
    parser.print_help()
    exit()

blacklist = args.blacklist.split(",") if args.blacklist else []

if method and method not in ["GET", "POST"]:
    print("invalid http method (GET, POST)")
    exit()

get = True if not method or method == "GET" else False

try:
    with open(wordlist, "r") as wls:
        wl = [word.strip() for word in wls]
except Exception:
    print("could not open the specified wordlist")
    exit()

do = [True if arg and "FART" in arg else False for arg in [url, headers, data]]

for word in wl:
    t_url = url.replace("FART", word) if do[0] else url
    t_headers_raw = headers.replace("FART", word) if do[1] else headers
    t_data_raw = data.replace("FART", word) if do[2] else data

    if t_headers_raw:
        t_headers = parse_headers(t_headers_raw)
    else:
        t_headers = {}

    if t_data_raw:
        t_data = {
            key: values[0]
            for key, values in parse_qs(t_data_raw).items()
        }
    else:
        t_data = {}

    try:
        if get:
            req = rq.get(t_url, headers=t_headers, data=t_data, timeout=10)
        else:
            req = rq.post(t_url, headers=t_headers, data=t_data, timeout=10)
    except rq.exceptions.RequestException as e:
        print(f"request failed for word '{word}': {e}")
        continue

    code = req.status_code
    if str(code) not in blacklist:
        print(f"{code} : FART -> {word}")