import re

from pyzork.yarn_spinner.yarn_node import YarnNode

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
re_command_kvp = r'^{re_whitespace_sans_newline}*{re_command_scope_open}(?P<{re_group_command_name}>{re_token_identifier}) (?P<{re_group_command_param}>{re_token_identifier}){re_command_scope_close}{re_whitespace_sans_newline}*$'


# Markup parsing
re_group_markup_tag_name = 'tag_name'
re_group_markup_tag_param = 'tag_param'
re_group_markup_tag_inclosed = 'tag_inclosed'
# TODO support nested markup tags.  (I'm literally so close, but I can't regex anymore today)
re_markup_tag = fr'\[(?P<{re_group_markup_tag_name}>(?:(?!]|=|]).)+)=?(?P<{re_group_markup_tag_param}>(?<==)(?:(?!]|=|/]).)+)?(?:(?:(?P<{re_group_markup_tag_inclosed}>(?:(?![|=|\\[]).)+)\[/\1\])|(?:/]))'


# Node metastructure parsing
re_group_node_header_value = 'node_header_value'
re_group_node_header_key = 'node_header_key'
re_node_header_delimiter = r'^---$'
re_node_footer_delimiter = r'^===$'
re_node_header_kvp = fr'^(?P<{re_group_node_header_key}>{re_token_identifier}):{re_whitespace_sans_newline}*(?P<{re_group_node_header_key}>{re_token_value}){re_whitespace_sans_newline}*$'


# Node body parsing
re_group_actor = 'actor_name'
re_group_dialog_value = 'dialog'
re_dialogue_line = fr"^(?P<{re_group_actor}>{re_token_identifier}):{re_whitespace_sans_newline}*(?P<{re_group_dialog_value}>{re_token_dialog})$"

"""
    Actual parsing.

    Even though I tend to write with a lot of verbosity,
    I would hope that the .yarn files are never large enough I'd need to stream these in.
"""
def parse_yarn(yarn_text):
    """
    Converts a string of yarn text into a dictionary of yarn_nodes
    Accepts any style of EOL.

    DOESN'T DO ANY ERROR CHECKING.  Assumes valid Yarn, and will be undefined behavior if not valid.

    * TODO handle Yarn's "option shortcuts".  E.G. "-->"
    * TODO handle Yarn's "hashtag meta keys"  E.G. how they did localization: "#line:0faf7c"
    * TODO add at least basic support for Yarn's if/else system.
    * TODO add at least basic support for Yarn's visited node system.
    * TODO add support for nested markup tags
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

    # TODO actually return a Yarn() class containing dict of nodes, entry point, & metadata
    return nodes

def strip_comments(line):
    re.sub(re_comment, '', line)

def get_nodes(line_list):

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
        else :
            pass    #Uh, let's just not worry about getting the node body for now.
