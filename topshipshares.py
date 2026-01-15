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

def get_character_count(tag_slug):
    url = f"https://archiveofourown.org/tags/{tag_slug}/works"

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
            ships[row["ship"]] = [
                int(row["amount"]),
            ]  
        for ship in ships:
            chars = ship.split('/')
            omega1 = get_character_count("Omega%20" + chars[0].replace(" ", "%20"))
            print(f"Omega {chars[0]} = {omega1}")
            omega2 = get_character_count("Omega%20" + chars[1].replace(" ", "%20"))
            print(f"Omega {chars[1]} = {omega2}")
            alpha1 = get_character_count("Alpha%20" + chars[0].replace(" ", "%20"))
            print(f"Alpha {chars[0]} = {alpha1}")
            alpha2 = get_character_count("Alpha%20" + chars[1].replace(" ", "%20"))
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
