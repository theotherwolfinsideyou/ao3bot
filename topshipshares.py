import requests
import random
import time
from bs4 import BeautifulSoup
import csv

HEADERS = {
    "User-Agent": "AO3OmegaverseStatsBot (personal, non-commercial, NOT for ai purposes)"
}

INPUT_FILE = "topships.csv"
OUTPUT_FILE = "topshipssorted.csv"
DELAY_SECONDS = 5

ships = {}
percentages = {}

def get_character_count(char,ship):
    url = f"https://archiveofourown.org/works?commit=Sort+and+Filter&work_search%5Bsort_column%5D=revised_at&work_search%5Bother_tag_names%5D={char}&work_search%5Bexcluded_tag_names%5D=&work_search%5Bcrossover%5D=&work_search%5Bcomplete%5D=&work_search%5Bwords_from%5D=&work_search%5Bwords_to%5D=&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bquery%5D=&work_search%5Blanguage_id%5D=&tag_id={ship}"

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
    with open(INPUT_FILE, newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            ships[row["ship"]] = int(row["amount"])
        for ship in ships:
            chars = ship.split('/')
            shipreader = ship[:]
            shipreader.replace(" ", "+")
            shipreader.replace("/","*s")
            omega1 = get_character_count("Omega+" + chars[0].replace(" ", "+"),shipreader)
            print(f"Omega {chars[0]} = {omega1}")
            omega2 = get_character_count("Omega+" + chars[1].replace(" ", "+"),shipreader)
            print(f"Omega {chars[1]} = {omega2}")
            alpha1 = get_character_count("Alpha+" + chars[0].replace(" ", "+"),shipreader)
            print(f"Alpha {chars[0]} = {alpha1}")
            alpha2 = get_character_count("Alpha+" + chars[1].replace(" ", "+"),shipreader)
            print(f"Alpha {chars[1]} = {alpha2}")
            char1gender = ""
            char2gender = ""
            char1percent = 0.0
            char2percent = 0.0
            if omega1 > alpha1:
                char1gender = "Omega"
                char1percent = round(omega1 / ships[ship],2) * 100
            if alpha1 > omega1:
                char1gender = "Alpha"
                char1percent = round(alpha1 / ships[ship],2) * 100
            if omega1 > alpha1:
                char2gender = "Omega"
                char2percent = round(omega2 / ships[ship],2) * 100
            if alpha1 > omega1:
                char2gender = "Alpha"
                char2percent = round(alpha2 / ships[ship],2) * 100
            percentages[ship] = [char1gender, char1percent,char2gender,char2percent]
            print(f"{ship},{char1gender},{char1percent},{char2gender},{char2percent}")
            
        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file_output:
            writer = csv.writer(file_output)
            writer.writerow(["ship","char1gender","char1percent","char2gender","char2percent"])
            for ship, values in ships.items():
                writer.writerow([name, *values])        


if __name__ == "__main__":
    main()
