import argparse
import json
import re
import textwrap
from collections import OrderedDict
from io import StringIO


def first(iterable):
    for value in iterable:
        return value


type_map = {int: 'int', float: 'float', bool: 'flag'}


def yaml_dump_dict_of_lists(lst):
    # This is hardly bullet-proof, but should mostly work.
    sio = StringIO()
    for dct in lst:
        for i, (key, value) in enumerate(dct.items()):
            value = str(value)
            sio.write(
                '%s%s: %s\n'
                % (
                    ('- ' if i == 0 else '  '),
                    key,
                    (value if '\n' not in value else json.dumps(value)),
                )
            )
    return sio.getvalue()


def convert_parser(ap):
    """
    Convert an argparse ArgumentParser's optional parameters to valohai.yaml `parameters` objects.

    :type ap: argparse.ArgumentParser
    :return: list of dicts that can be YAML serialized
    """
    parameter_defs = []
    for arg in ap._get_optional_actions():
        if isinstance(arg, argparse._HelpAction):
            continue
        longest_option_string = first(sorted(arg.option_strings, key=len, reverse=True))
        type = type_map.get(arg.type)
        parameter_def = OrderedDict(
            [
                ('name', arg.dest.replace('_', ' ')),
                ('pass-as', longest_option_string + '={v}'),
            ]
        )

        if type:
            parameter_def['type'] = type
            if arg.default:
                parameter_def['default'] = arg.default
        else:
            print('Warning: Not sure about the type %s for %s' % (arg.type, arg.dest))

        if arg.help:
            parameter_def['description'] = re.sub(
                r'\s+', ' ', textwrap.dedent(arg.help)
            )

        parameter_defs.append(parameter_def)

    return parameter_defs


def dump_parameter_defs(parameter_defs):
    """
    Dump a list of parameter defs returned by `convert_parser` as YAML.

    For convenience, also accepts the parser object.

    :param parameter_defs: list of dicts or the parser.
    :return: YAML string
    """
    if isinstance(parameter_defs, argparse.ArgumentParser):
        parameter_defs = convert_parser(parameter_defs)

    return yaml_dump_dict_of_lists(parameter_defs)
