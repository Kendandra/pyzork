from email.generator import Generator
import re
from pyzork.yarn_spinner.yarn import Yarn

from pyzork.yarn_spinner.yarn_node import YarnNode
from pyzork.yarn_spinner.yarn_thread import YarnCommand, YarnDialog, YarnToken, YarnTokenKind, YarnTokenScope

"""
    Parseing token regexes
"""
# Shared parsing tokens
re_token_identifier = r'\w[\w_]*'
re_token_value = r'[\w_][\w_,=!:;~&@#%\-\+\|\?\.\(\)\$\^\{\}\"\'\\ ]*'
re_whitespace_sans_newline = r"[^\S\r\n]"
re_token_dialog = r'[^\r\n]+'
re_comment = r'//[^\r\n]*$'


# Command parsing
re_group_command_param = 'command_param'
re_group_command_name = 'command_name'
re_command_scope_open = r'<<'
re_command_scope_close = r'>>'
re_command_kvp = fr'^{re_whitespace_sans_newline}*{re_command_scope_open}(?P<{re_group_command_name}>{re_token_identifier}) (?P<{re_group_command_param}>{re_token_identifier}){re_command_scope_close}{re_whitespace_sans_newline}*$'
"""
    Pick up command only lines in threads

    <<jump Goodbye>>
"""


# Markup parsing
re_group_markup_tag_name = 'tag_name'
re_group_markup_tag_param = 'tag_param'
re_group_markup_tag_inclosed = 'tag_inclosed'
re_group_markup_remainder = 'tag_remainder'
re_markup_tag = fr'^\[(?P<{re_group_markup_tag_name}>(?:(?!(?://\])|=|]).)+)=?(?P<{re_group_markup_tag_param}>(?<==)(?:(?!]|=|(?:\])).)+)?\](?:(?:(?P<{re_group_markup_tag_inclosed}>[^\]].*)?)\[\/\1\])?(?P<{re_group_markup_remainder}>(.*))?$'
"""
    Pick out lines of markup to tokenize like:
    "\[(?P<re_group_markup_tag_name>(?:(?!\]|=|]).)+)=?(?P<re_group_markup_tag_param>(?<==)(?:(?!]|=|]).)+)?\](?:(?:(?P<re_group_markup_tag_inclosed>[^\]].*)?)\[\/\1\])?"mg

    [keyword]ancients[/keyword]
"""


# Node metastructure parsing
re_group_node_header_value = 'node_header_value'
re_group_node_header_key = 'node_header_key'
re_node_header_delimiter = r'^---$'
re_node_footer_delimiter = r'^===$'
re_node_header_kvp = fr'^(?P<{re_group_node_header_key}>{re_token_identifier}):{re_whitespace_sans_newline}*(?P<{re_group_node_header_value}>{re_token_value}){re_whitespace_sans_newline}*$'
"""
    Get header row like:

    title: Arrival
"""


# Node body parsing
re_group_actor = 'actor_name'
re_group_dialog_value = 'dialog'
re_dialogue_line = fr"^(?P<{re_group_actor}>{re_token_identifier}):{re_whitespace_sans_newline}*(?P<{re_group_dialog_value}>{re_token_dialog})$"
"""
    Get a line of dialog like:

    Crow: [mood=normal/]Oh.
"""




"""
    Actual parsing.

    Even though I tend to write with a lot of verbosity,
    I would hope that the .yarn files are never large enough I'd need to stream these in.
"""
def parse_yarn(yarn_text: str, name="Unnamed Yarn", source_file=None) -> Yarn:
    """
    Converts a string of yarn text into a dictionary of yarn_nodes
    Accepts any style of EOL.

    DOESN'T DO ANY ERROR CHECKING.  Assumes valid Yarn, and will be undefined behavior if not valid.

    * TODO handle Yarn's "option shortcuts".  E.G. "-->"
    * TODO handle Yarn's "hashtag meta keys"  E.G. how they did localization: "#line:0faf7c"
    * TODO add at least basic support for Yarn's if/else system.
    * TODO add at least basic support for Yarn's visited node system.
    * TODO add support for two same (non-nested) tags on the same line.
    """

    # First normalize the line endings, then get an array of lines.
    # Really shouldn't HAVE to do this... but...
    # Okay look, I'm writing all these .yarn files and I KNOW because I'm on
    # Windows running in the WSL, and want to eventually pyinstaller this to
    # a standalone app, that, yeah.  I'm gonna mix these line endings up at
    # some point and I don't want the parsing to randomly break because of that.
    line_list = yarn_text.replace('\r\n', '\n').replace('\r', '\n').splitlines()
    line_list = [strip_comments(line) for line in line_list]

    nodes = get_nodes(line_list)

    return Yarn(nodes, name, source_file)

def strip_comments(line: str):
    return re.sub(re_comment, '', line)

def get_nodes(line_list: list):

    header_dict = {}
    thread_list = []

    # Keep this around for parser debugging
    raw_text = []

    header_parse_complete = False

    for raw_line in line_list:
        raw_text.append(raw_line)
        line = raw_line.strip() # TODO eventually we'll need to support indentations for --> option tokens, and strip won't work
                                # Hashtag #justWhiteSpaceLanguage things.

        if len(line) == 0:
            continue

        if re.match(re_node_header_delimiter, line):
            header_parse_complete = True

        if re.match(re_node_footer_delimiter, line):
            if not header_parse_complete:
                raise Exception("Could not parse Yarn.  Node footer found before header delimiter.", line_list)
            else:
                yield YarnNode(header_dict, thread_list, '\n'.join(raw_text))
                header_parse_complete = False
                header_dict = {}
                thread_list = []
                raw_text = []

        if not header_parse_complete:
            node_header_kvp_match = re.match(re_node_header_kvp, line)

            if node_header_kvp_match:
                header_dict.setdefault(
                    node_header_kvp_match.group(re_group_node_header_key),
                    node_header_kvp_match.group(re_group_node_header_value)
                )
        else:
            thread_command_match = re.match(re_command_kvp, line)

            thread = None

            if thread_command_match:
                thread = YarnCommand(thread_command_match.group(re_group_command_name), thread_command_match.group(re_group_command_param), line)
            else:
                thread_dialog_match = re.match(re_dialogue_line, line)

                if thread_dialog_match:
                    thread_actor = thread_dialog_match.group(re_group_actor)
                    thread_dialog = thread_dialog_match.group(re_group_dialog_value)

                    thread_tokens = list(tokenize_dialog_line(thread_dialog))

                    thread = YarnDialog(thread_actor, thread_dialog, thread_tokens, line)

            if thread:
                thread_list.append(thread)


def tokenize_dialog_line(thread_dialog: str):
    thread_dialog_stripped = thread_dialog.strip()

    if not thread_dialog_stripped:
        return

    try:
        str_before_markup = thread_dialog_stripped[:thread_dialog_stripped.index("[")]
    except ValueError:
        yield YarnToken(YarnTokenKind.TEXT, thread_dialog_stripped, YarnTokenScope.INSTANT)
        return

    if str_before_markup:
        yield YarnToken(YarnTokenKind.TEXT, str_before_markup, YarnTokenScope.INSTANT)
        str_remainder = thread_dialog_stripped[len(str_before_markup):]

        if not str_remainder:
            return

    else:
        str_remainder = thread_dialog_stripped

    markup_match = re.match(re_markup_tag, str_remainder)

    if markup_match:
        tag_name = markup_match.group(re_group_markup_tag_name)
        tag_param = markup_match.group(re_group_markup_tag_param)
        tag_inclosed = markup_match.group(re_group_markup_tag_inclosed)
        tag_remainder = markup_match.group(re_group_markup_remainder)

        try:
            kind = YarnTokenKind[tag_name.strip('/').upper()]
        except KeyError:
            kind = YarnTokenKind.UNKNOWN

        if '/' in tag_name or (tag_param and '/' in tag_param):
            yield YarnToken(kind, tag_param.strip('/') if tag_param else None, YarnTokenScope.INSTANT)
        else:
            yield YarnToken(kind, tag_param.strip('/') if tag_param else None, YarnTokenScope.OPEN)

            if tag_inclosed:
                yield from tokenize_dialog_line(tag_inclosed)

            yield YarnToken(kind, tag_param.strip('/') if tag_param else None, YarnTokenScope.CLOSE)

        if tag_remainder:
            yield from tokenize_dialog_line(tag_remainder)

    else:
        yield YarnToken(YarnTokenKind.TEXT, thread_dialog_stripped, YarnTokenScope.INSTANT)
