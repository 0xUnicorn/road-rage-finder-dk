from bs4 import BeautifulSoup
import requests
import re
import sys


URL = "https://bilopslag.nu/nummerplade/"
REGEX_PLATE = r"([a-z]{2})([0-9]{2})([0-9]{1,3})?"
LICENSE_PLATE = sys.argv[1]

def get_webpage(license_plate):
    page = requests.get(URL + license_plate)
    if page.status_code == 200:
        return page
    raise Exception(f"Request error 'status_code:{page.status_code}'")

def generate_sequence(start_seq):
    return [f"{start_seq + n:03d}" for n in range(999 - int(start_seq) + 1)]

def generate_missing_plates(base_plate, start_num):
    if len(start_num) == 1:
        seq = generate_sequence(int(start_num) * 100)
    elif len(start_num) == 2:
        seq = generate_sequence(int(start_num) * 10)
    else:
        seq = generate_sequence(int(start_num))

    return [f"{base_plate + i}" for i in seq]

def process_license_plate(input_plate):
    matches = re.findall(REGEX_PLATE, input_plate)[0]
    if not matches:
        raise Exception(f"No valid matches found in: '{input_plate}'")
    base_plate = matches[0] + matches[1]
    start_num = matches[2]
    return base_plate, start_num

def main():
    base_plate, start_num = process_license_plate(LICENSE_PLATE)
    missing_plates = generate_missing_plates(base_plate, start_num)
    print("\n".join(missing_plates))

if __name__ == "__main__":
    main()
