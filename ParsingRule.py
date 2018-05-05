import re


class ParsingRule:

    @staticmethod
    def parse_wildcard_id_selector(string: str) -> str:
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

        return out



