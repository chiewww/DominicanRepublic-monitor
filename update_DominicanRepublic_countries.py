from playwright.sync_api import sync_playwright
from pathlib import Path

URL = "https://inposdom.gob.do/#lospaises"
OUTPUT = Path("DominicanRepublic_countries.txt")


def get_countries():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page(viewport={"width": 1280, "height": 2000})

        page.goto(URL, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)

        # Click "Mostrar más" repeatedly
        for i in range(30):
            buttons = page.locator("button")

            clicked = False

            for j in range(buttons.count()):
                text = buttons.nth(j).inner_text()

                if "Mostrar" in text:
                    buttons.nth(j).scroll_into_view_if_needed()
                    buttons.nth(j).click()
                    page.wait_for_timeout(2000)
                    clicked = True
                    break

            if not clicked:
                break

        # Extract countries
        countries = page.locator(
            "h3.pde-country-card__name"
        ).all_inner_texts()

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
