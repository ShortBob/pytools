"""
Designed to be used in command line to prettyfy a json raw text.

usage: main.py [-h] [-v] [-o] [-i [INDENT]] [-l LIMIT] [-f] JSON

positional arguments:
  JSON                  The JSON textual value. Can be a file if --file.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbosity       Increase the verbosity level. Accumulate short option
                        to raise.
  -o, --ordered         Order elements when printing.
  -i [INDENT], --indent [INDENT]
                        Indent elements when printing.
  -l LIMIT, --limit LIMIT
                        Only show a subpart of the Json object. Split on char
                        '>'.
  -f, --file            Use JSON as a file to open and load

"""

import argparse
import json
import logging


# OPTIONS
OPTION_VERBOSITY = "verbosity"
OPTION_VERBOSITY_SHORT = OPTION_VERBOSITY[0:1]

OPTION_ORDERED = "ordered"
OPTION_ORDERED_SHORT = OPTION_ORDERED[0:1]

OPTION_INDENT = "indent"
OPTION_INDENT_SHORT = OPTION_INDENT[0:1]
OPTION_INDENT_DEFAULT = 4

OPTION_LIMIT = "limit"
OPTION_LIMIT_SHORT = OPTION_LIMIT[0:1]

OPTION_FROM_FILE = "file"
OPTION_FROM_FILE_SHORT = OPTION_FROM_FILE[0:1]

# VALUES
JSON_TEXT_TO_PARSE = "JSON"


def build_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-" + OPTION_VERBOSITY_SHORT,
        "--" + OPTION_VERBOSITY,
        help="Increase the verbosity level. Accumulate short option to raise.",
        action="count",
        default=0
    )
    parser.add_argument(
        "-" + OPTION_ORDERED_SHORT,
        "--" + OPTION_ORDERED,
        help="Order elements when printing.",
        action="store_true",
    )
    parser.add_argument(
        "-" + OPTION_INDENT_SHORT,
        "--" + OPTION_INDENT,
        nargs="?",
        type=int,
        help="Indent elements when printing.",
        default=OPTION_INDENT_DEFAULT
    )
    parser.add_argument(
        "-" + OPTION_LIMIT_SHORT,
        "--" + OPTION_LIMIT,
        help="Only show a subpart of the Json object. Split on char '>'.",
    )
    parser.add_argument(
        "-" + OPTION_FROM_FILE_SHORT,
        "--" + OPTION_FROM_FILE,
        help="Use JSON as a file to open and load",
        action="store_true"
    )
    parser.add_argument(
        JSON_TEXT_TO_PARSE,
        help="The JSON textual value. Can be a file if --file."
    )
    return vars(parser.parse_args())


def configure_log_level(parsed):
    log_level_num = parsed[OPTION_VERBOSITY]

    if log_level_num <= 0:
        log_level = logging.CRITICAL
    elif log_level_num == 1:
        log_level = logging.INFO
    else:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level)
    logging.debug(
        "Logging level configured to {name}({numeric})".format(
            numeric=log_level,
            name=logging.getLevelName(log_level),
        )
    )


def read_from_file_if_needed(parsed):
    if parsed[OPTION_FROM_FILE]:
        logging.info("Reading from file {}...".format(parsed[JSON_TEXT_TO_PARSE]))
        with open(parsed[JSON_TEXT_TO_PARSE], 'r', encoding='UTF-8') as source:
            json_text = ''.join(source)
            logging.info("Read !")
        return json_text
    else:
        logging.debug("No need to read from file")
        return parsed[JSON_TEXT_TO_PARSE]


def to_pretty(loaded, order, indent_count):
    logging.debug("Building output with INDENT SIZE={} and ORDERING={}".format(indent_count, order))
    indent = ''.join((' ' for _ in range(0, indent_count)))
    return json.dumps(
        loaded,
        sort_keys=order,
        indent=indent
    )


def limit_json_object_to_if_needed(loaded):
    json_limiter = parsed[OPTION_LIMIT]
    if json_limiter:
        logging.info("LIMIT TO SUBTREE '{}'".format(json_limiter))
        to_keep = loaded
        for level in json_limiter.split('>'):
            to_keep = to_keep[level]
        return to_keep
    logging.debug("NO SUBTREE DEFINED. All Json will be printed.")
    return loaded


if __name__ == '__main__':
    parsed = build_parser()
    configure_log_level(parsed)

    logging.info("VALUES PARSED : {}".format(parsed))

    text_to_load_as_json = read_from_file_if_needed(parsed)
    loaded_json = json.loads(text_to_load_as_json)
    loaded_json = limit_json_object_to_if_needed(loaded_json)
    pretty = to_pretty(loaded_json, parsed[OPTION_ORDERED], parsed[OPTION_INDENT], )

    print(pretty)
