# delimiter:Tag
#

import re

class ParsingRule:

    @staticmethod
    def parse_wildcard_id_selector(string: str):
        target_id = ""
        id = string.index("#")

        print(string)

        target_id = string[id:]
        tag = string[:id]

        d_index = re.search('\+|~|,| |>',target_id).start(0)
        target_id = target_id[:d_index]
        conc = target_id[d_index:]


        strings = target_id.split("*")

        out = ""

        out += tag+ "[id^=\"" + strings[0][1:] + "\"]"+conc + ","

        for substring in strings[1:-1]:
            out += tag+"[id*=\"" + substring + "\"]"+conc + ","

        out += tag+"[id$=\"" + substring + "\"]"+conc + ","

        print("out : " + out)

    def __init__(self):
        parseDict = []


ParsingRule.parse_wildcard_id_selector("tr#item_unit_*_*_it+span")
