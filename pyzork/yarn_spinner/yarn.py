from .yarn_node import YarnNode
from itertools import chain



class Yarn():
    """
    Top level python representation of a Yarn conversation.
    Includes a node list, and an entry point.  Meant to be read by the Spinner
    """
    def __init__(self, nodes_iter, name, source_file) -> None:

        entry_node = next(nodes_iter, None)

        if not entry_node:
            raise Exception("Nodes iter was empty when creating a yarn", name)

        self._source_file = source_file
        self._name = name
        self._entry_key = entry_node.title

        self._nodes = {node.title:node for node in chain([entry_node], nodes_iter)}

    @property
    def name(self):
        return self._name

    def __str__(self) -> str:
        return self._name + '\n' + '\n'.join([YarnNode.get_debug_str(node) for (_, node) in self._nodes.items()])
