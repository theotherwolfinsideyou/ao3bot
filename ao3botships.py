import requests
import random
import time
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "AO3OmegaverseStatsBot (personal, non-commercial, NOT for ai purposes)"
}

INPUT_FILE = "ships.txt"
DELAY_SECONDS = 5

def get_ship_count(tag_slug):
    url = f"https://archiveofourown.org/works?commit=Sort+and+Filter&work_search%5Bsort_column%5D=revised_at&work_search%5Bother_tag_names%5D=Alpha%2FBeta%2FOmega+Dynamics&work_search%5Bexcluded_tag_names%5D=&work_search%5Bcrossover%5D=&work_search%5Bcomplete%5D=&work_search%5Bwords_from%5D=&work_search%5Bwords_to%5D=&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bquery%5D=&work_search%5Blanguage_id%5D=&tag_id={tag_slug}"

    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # This selector is stable on AO3
    heading = soup.find("h2", class_="heading")

    if not heading:
        raise ValueError("Could not find works heading")

    # Example text: "Works (5,956)"
    text = heading.get_text(strip=True)
    split_up = text.split(" ")
    count = 0
    if split_up[1] == "-":
        new_text = ''
        for s in split_up[4]:
            if s != ',':
                new_text += s
        count = int(new_text)
    else:
        count = int(split_up[0])
        
    return count

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as infile:

        for line in infile:
            line = line.strip()
            failed = False

            # Skip blank lines or comments
            if not line or line.startswith("#"):
                continue

            try:
                name = quote_plus(line)
                total_count = get_ship_count(name)
                print(f"✓ {line} : {total_count}")

            except Exception as e:
                
                print(f"✗ {line}: {e}")
                failed = True
                
            time.sleep(DELAY_SECONDS + random.uniform(5, 10))


if __name__ == "__main__":
    main()