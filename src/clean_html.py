import datetime
import re

import markdownify
from bs4 import BeautifulSoup, Tag


def find_specific_tables(soup: BeautifulSoup, column_mapping: dict) -> list[Tag]:
    # Get all tables
    tables = soup.find_all("table")
    matching_tables = []

    for table in tables:
        # Find tbody (some tables might not have it explicitly)
        tbody = table.find("tbody")
        if not tbody:
            continue

        first_row = tbody.find("tr")
        if not first_row:
            continue

        # Example: Check if first row has specific columns
        columns = first_row.find_all("td")
        column_names = [col.text.strip() for col in columns]
        # Check for your specific shape/structure
        if (
            len(column_names) == 3  # Example: checking for 3 columns
            and "DATA" in column_names[0]
            and "ESTABELECIMENTO" in column_names[1]
        ):

            if column_mapping:
                # Apply renaming
                for i, header in enumerate(column_names):
                    if header in column_mapping:
                        # Find the td element and update its text
                        columns[i].string = column_mapping[header]

            matching_tables.append(table)

    return matching_tables


def find_total(soup: BeautifulSoup) -> str:
    document_value_text_el = soup.find("p", string="Limite total de crédito:")

    if not document_value_text_el:
        return "0,00"

    total_value_el = document_value_text_el.find_next()

    if not isinstance(total_value_el, Tag):
        return "0,00"

    value = total_value_el.string or "0,00"
    pattern = r"[\d.,]+"

    matched_value = re.search(pattern, value)
    if matched_value:
        return matched_value.group()

    return "0,00"


def find_date(soup: BeautifulSoup) -> str:
    expiration_value_text_el = soup.find("p", string="Vencimento")
    default_date = datetime.datetime.now().date().isoformat()

    if not expiration_value_text_el:
        return default_date

    date_value_el = expiration_value_text_el.find_next()

    if not isinstance(date_value_el, Tag):
        return default_date

    return date_value_el.string or default_date


def create_el(soup: BeautifulSoup, tag_type: str, text: str):
    el = soup.new_tag(tag_type)
    el.string = text
    return el


def parse_html(text: str):
    soup = BeautifulSoup(text, "html.parser")
    tables = find_specific_tables(soup, {"VALOR EM R$": "VALOR", "R$": "VALOR"})
    expiration_date = find_date(soup)
    total_value = find_total(soup)

    new_soup = BeautifulSoup("", "html.parser")
    html = soup.new_tag("html")
    soup.append(html)
    body = soup.new_tag("body")
    html.append(body)

    title = create_el(soup, "h1", "fatura")
    body.append(title)

    metadata = create_el(soup, "h2", "metadata")
    date_of_emission = create_el(soup, "p", f"Data de expiração: {expiration_date}")
    total_amount = create_el(soup, "p", f"Valor total: {total_value}")
    body.append(metadata)
    body.append(date_of_emission)
    body.append(total_amount)

    expenses = create_el(soup, "h2", "expenses")
    body.append(expenses)
    body.extend(tables)

    new_soup.append(html)

    return markdownify.MarkdownConverter().convert_soup(new_soup)


def parse_file(filename: str):
    with open(filename) as file:
        text = file.read()
    result = parse_html(text)
    with open(f"parsed1_{filename.replace('html','md')}", "w+") as file:
        file.write(result)


if __name__ == "__main__":
    filename = "fatura.html"
    parse_file(filename)
