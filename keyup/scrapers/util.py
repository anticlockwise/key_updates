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
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
MONTHS_INDEX = {month: index for index, month in enumerate(MONTHS)}
MONTHS_REGEX = re.compile("|".join(MONTHS), re.IGNORECASE)

nlp = spacy.load("en_core_web_sm")


def extract_shipping_date(item_title, text):
    text = text.replace(u'\xa0', ' ')
    doc = nlp(text)

    date_candidates = []
    for ent in doc.ents:
        if ent.label_ == "DATE":
            date_candidates.append(ent.text)

    if date_candidates:
        return date_candidates[-1]
    return None


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