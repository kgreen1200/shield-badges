import requests
import os
import json
from pathlib import Path

SLUGS_URL = "https://raw.githubusercontent.com/simple-icons/simple-icons/develop/slugs.md"
JSON_URL = "https://raw.githubusercontent.com/simple-icons/simple-icons/develop/_data/simple-icons.json"
BLACK_LOGOS = Path(os.path.dirname(os.path.realpath(__file__))) / "black_logos.txt"

def main():
    """Quick and dirty way to get a tab generated with the badges. Don't judge pls"""
    slugs = requests.get(SLUGS_URL)
    slugs_dict = json.loads((requests.get(JSON_URL)).text)

    with open(BLACK_LOGOS, "r", encoding="utf8") as f:
        black_logo_names = f.read().splitlines()

    with open("slugs.md", "w", encoding="utf8") as f:
        f.write((slugs.text))

    with open("badges_list.md", "w", encoding="utf8") as badges_list:
        badges_list.write("# Generated Brand Shields\n")
        badges_list.write("| Name | Badge | URL |\n| ---: | :---: | :--- |\n")
        with open("slugs.md", "r", encoding="utf8") as f:
            for line in f.readlines():
                line = line.strip()
                if line.startswith("| `"):
                    name = line.split("|")[1].strip(" `")
                    slug = line.split("|")[2].strip(" `")
                    source = None
                    color = "white"
                    if slug in black_logo_names:
                        color = "black"
                    for logo in slugs_dict["icons"]:
                        if logo["title"] == name:
                            hex = logo["hex"]
                            if "source" in logo:
                                source = logo["source"]
                            break
                    formatted_name = name.replace(" ", "_").replace("-", "_")
                    badge_url = f"https://img.shields.io/badge/-{formatted_name}-{hex}?style=for-the-badge&logo={slug}&logoColor={color}"
                    if source is None:
                        badges_list.write(f"| {name} | ![{name}]({badge_url}) | `{badge_url}` |\n")
                    else:
                        badges_list.write(f"| {name} | [![{name}]({badge_url})]({source}) | `{badge_url}` |\n")
    print("DONE!")

if __name__ == "__main__":
    main()