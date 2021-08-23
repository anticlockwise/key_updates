import spacy
import datetime
import re
from spacy.language import Language

from spacy.pipeline import EntityRuler


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
MONTHS_INDEX = {month: index + 1 for index, month in enumerate(MONTHS[:12])}
MONTHS_REGEX_TEXT = "|".join(MONTHS)
MONTHS_REGEX = re.compile(MONTHS_REGEX_TEXT, re.IGNORECASE)
MONTHS_ABBR_REGEX = re.compile("({})(\s+|\.\s+|\/)".format("|".join(MONTHS_ABBR)))

# For cleaning Q1. into Q1
QUARTERS_REGEX = re.compile(r"(Q[1-4]).+\s+")
YEAR_CLEANING_REGEX = re.compile(r"'([0-9]{2})")

NEW_YEAR_TEXT_REGEX = re.compile(r"the(\searly)? new year")

ADDITIONAL_DATE_PATTERNS = [
    {
        "label": "DATE",
        "pattern": [{"TEXT": {"REGEX": "^Q[1-4]$"}}, {"TEXT": {"REGEX": "^\d{4}$"}}],
    },
    {
        "label": "DATE",
        "pattern": [
            {"TEXT": {"REGEX": "^{}/$".format(MONTHS_REGEX_TEXT)}},
            {"TEXT": {"REGEX": "^{}$".format(MONTHS_REGEX_TEXT)}},
        ],
    },
    {
        "label": "DATE",
        "pattern": [
            {"LOWER": "mid"},
            {"TEXT": "/"},
            {"LOWER": "late"},
            {"TEXT": {"REGEX": "^{}$".format(MONTHS_REGEX_TEXT)}},
        ],
    },
]


@Language.factory("date_extractor")
def date_extractor(nlp, name):
    ruler = EntityRuler(nlp, validate=True)
    ruler.add_patterns(ADDITIONAL_DATE_PATTERNS)
    return ruler


nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("date_extractor", first=True)


def extract_shipping_date(text):
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
            text_arr.append(text[start_index : month_abbr_match.start()])
            month_full_name = MONTHS_MAPPING[month_abbr_match.group(1)]
            text_arr.append(month_full_name)

            next_char = month_abbr_match.group(2)
            if next_char == "/":
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

    # Add extra year if doesn't exist already
    year_text = extract_year(normalized_text)
    if year_text:
        normalized_text = normalized_text + " " + str(year_text)

    today = datetime.date.today()
    current_year = today.year
    normalized_text = NEW_YEAR_TEXT_REGEX.sub(str(current_year), normalized_text)

    return normalized_text


def extract_year(text):
    year_text_match = YEAR_EXTRACTOR.search(text)
    month_text_match = MONTHS_REGEX.search(text)
    if not year_text_match and month_text_match:
        today = datetime.date.today()
        current_month = today.month
        current_year = today.year

        month_text = month_text_match.group(0)
        month = MONTHS_INDEX[month_text]
        if current_month > month:
            return current_year + 1
        return current_year


if __name__ == "__main__":
    text = "These completed production and are on their way to us now! Estimated transit + customs about a month and a half due to the holiday season. Mid/late January should start seeing shipment to customers."
    doc = nlp(text)
    print([ent.text for ent in doc])
    print([(ent.label_, ent.text) for ent in doc.ents])