from playwright.sync_api import sync_playwright
from pathlib import Path

URL = "https://inposdom.gob.do/#lospaises"

OUTPUT = Path("DominicanRepublic_countries.txt")


def get_countries():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()
        
        page.goto(URL, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)

        # Click "Mostrar más" until all countries are loaded
        for _ in range(20):
            button = page.get_by_text("Mostrar más", exact=False)

            if button.count() == 0:
                break

            try:
                button.first.scroll_into_view_if_needed()
                button.first.click()
                page.wait_for_timeout(2000)
            except Exception:
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
