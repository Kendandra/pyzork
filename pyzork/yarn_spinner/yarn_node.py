

from gc import get_debug


class YarnNode:
    """
    Data structure for a Yarn Spinner node.  Kinda.
    """
    def __init__(self, header_dict, threads_list, raw_parse_text) -> None:
        self.raw_parse_text = raw_parse_text

        self._header = header_dict
        self._threads = threads_list

        try:
            self._title = header_dict["title"]
        except:
            raise Exception("YarnNode didn't have a title.", raw_parse_text)

    def __str__(self):
        return self.get_debug_str()

    def get_debug_str(self):
        return (
            '\n'.join([f"  {header.__str__()}" for header in self.header.items()])
            + "\n---\n" + '\n'.join([f"  {thread.__str__()}" for thread in self.threads])
            + "\n===\n"
        )

    @property
    def title(self):
        return self._title

    @property
    def header(self):
        return self._header

    @property
    def threads(self):
        return self._threads
