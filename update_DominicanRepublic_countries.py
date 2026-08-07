from playwright.sync_api import sync_playwright
from pathlib import Path

URL = "https://inposdom.gob.do/#lospaises"
OUTPUT = Path("DominicanRepublic_countries.txt")


def get_countries():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(URL, wait_until="networkidle")

        # Wait for initial countries
        page.wait_for_selector(
            ".pde-country-card__name",
            timeout=30000
        )

        page.wait_for_timeout(3000)

        # Click Mostrar más while it exists
        for i in range(30):
            buttons = page.locator("text=Mostrar")

            found = False

            for n in range(buttons.count()):
                try:
                    btn = buttons.nth(n)

                    if btn.is_visible():
                        btn.click()
                        page.wait_for_timeout(2000)
                        found = True
                        break

                except Exception:
                    continue

            if not found:
                break

        countries = page.locator(
            ".pde-country-card__name"
        ).all_inner_texts()

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
