import json
import re


def extract_json(text):

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if not match:
        raise Exception("No JSON found.")

    return json.loads(match.group())