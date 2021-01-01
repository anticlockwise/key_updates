import spacy
import datetime
import datefinder
import itertools
import re
import unicodedata


YEAR_EXTRACTOR = re.compile(r"\d{4}")

MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
MONTHS_ABBR = MONTHS[12:]
MONTHS_MAPPING = {month_abbr: MONTHS[i] for i, month_abbr in enumerate(MONTHS_ABBR)}
MONTHS_INDEX = {month: index for index, month in enumerate(MONTHS[:12])}
MONTHS_REGEX = re.compile("|".join(MONTHS), re.IGNORECASE)
MONTHS_ABBR_REGEX = re.compile("({})(\s+|\.\s+|\/)".format("|".join(MONTHS_ABBR)))

# For cleaning Q1. into Q1
QUARTERS_REGEX = re.compile(r"(Q[1-4]).+\s+")
YEAR_CLEANING_REGEX = re.compile(r"'([0-9]{2})")

nlp = spacy.load("en_core_web_sm")


def extract_shipping_date(item_title, text):
    text = text.replace(u"\xa0", " ")
    doc = nlp(text)

    date_candidates = []
    for ent in doc.ents:
        if ent.label_ == "DATE":
            date_candidates.append(ent.text)

    if date_candidates:
        return normalize_date(date_candidates[-1])
    return None


def normalize_date(text):
    """
    To normalize the given date text into either "<Month> <Year>" or "<Quarter> <Year>" format.
    """
    normalized_text = text

    month_abbr_matches = MONTHS_ABBR_REGEX.finditer(text)
    if month_abbr_matches:
        text_arr, start_index = [], 0
        for month_abbr_match in month_abbr_matches:
            text_arr.append(text[start_index:month_abbr_match.start()])
            month_full_name = MONTHS_MAPPING[month_abbr_match.group(1)]
            text_arr.append(month_full_name)

            next_char = month_abbr_match.group(2)
            if next_char == '/':
                text_arr.append("/")
            else:
                text_arr.append(" ")
            start_index = month_abbr_match.end()
        text_arr.append(text[start_index:])
        normalized_text = "".join(text_arr)

    # For cleaning quarters
    normalized_text = QUARTERS_REGEX.sub(r"\1 ", normalized_text)
    # For cleaning '21 into 2021
    normalized_text = YEAR_CLEANING_REGEX.sub(r"20\1", normalized_text)

    return normalized_text


def date_combinations(text):
    months = extract_months(text)
    years = extract_years(text, months)
    return [p for p in itertools.product(months, years)]


def extract_months(text):
    return MONTHS_REGEX.findall(text)


def extract_years(text, months):
    year_candidates = YEAR_EXTRACTOR.findall(text)
    if year_candidates:
        return year_candidates
    elif not months:
        return []

    today = datetime.date.today()
    current_month = today.month
    current_year = today.year

    max_month = max([MONTHS_INDEX[m] for m in months])
    if current_month > max_month:
        return [str(current_year + 1)]
    return [str(current_year)]


if __name__ == "__main__":
    with open("dates") as f:
        lines = f.readlines()
        for line in lines:
            normalize_date(line.strip())