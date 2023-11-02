from bcolors import BashColors, colored_print
import os
import json


def write_json(path: str = None, value: any = None):
    if not path or not value:
        colored_print("Não foi possível encontrar o arquivo json", BashColors.WARNING)
        colored_print("Cancelando...", BashColors.FAIL)
        os._exit(0)

    else:
        current_json_data = []
        with open(f"not_written/{path}", encoding="utf8") as config_json:
            current_json_data = json.load(config_json)
        current_json_data.append(value)
        json_object = json.dumps(current_json_data, indent=4)

        # Writing to sample.json
        with open(f"not_written/{path}", "w") as outfile:
            outfile.write(json_object)
