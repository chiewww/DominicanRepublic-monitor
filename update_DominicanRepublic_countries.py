from playwright.sync_api import sync_playwright
from pathlib import Path

URL = "https://inposdom.gob.do/#lospaises"

OUTPUT = Path("DominicanRepublic_countries.txt")


def get_countries():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(URL, wait_until="networkidle")

        # Click "Mostrar más" until no button remains
        while True:
            button = page.locator("text=/Mostrar m[aá]s/")

            if button.count() == 0:
                break

            try:
                button.first.click(timeout=3000)
                page.wait_for_timeout(1000)
            except:
                break

        # Extract country names
        countries = page.locator(
            ".pde-country-card__content h3.pde-country-card__name"
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
