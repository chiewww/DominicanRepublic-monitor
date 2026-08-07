from playwright.sync_api import sync_playwright
from pathlib import Path

URL = "https://inposdom.gob.do/#lospaises"
OUTPUT = Path("DominicanRepublic_countries.txt")


def get_countries():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page(viewport={"width": 1280, "height": 2000})

        page.goto(URL, wait_until="domcontentloaded")

        # Wait for JavaScript rendering
        page.wait_for_timeout(10000)

        # Click Mostrar más repeatedly
        for i in range(30):
            button = page.get_by_text("Mostrar más", exact=False)

            clicked = False

            for n in range(button.count()):
                current = button.nth(n)

                try:
                    if current.is_visible():
                        current.click(force=True)
                        page.wait_for_timeout(3000)
                        clicked = True
                        break
                except:
                    pass

            if not clicked:
                break

        # Wait again after all clicks
        page.wait_for_timeout(5000)

        countries = page.locator(
            "h3.pde-country-card__name"
        ).all_inner_texts()

        # Debug output
        print("Countries found:", len(countries))

        browser.close()

    return countries


def main():
    countries = get_countries()

    if not countries:
        raise Exception("No countries found")

    countries = sorted(set(countries))

    OUTPUT.write_text(
        "\n".join(countries) + "\n",
        encoding="utf-8"
    )

    print(f"Saved {len(countries)} countries")


if __name__ == "__main__":
    main()
