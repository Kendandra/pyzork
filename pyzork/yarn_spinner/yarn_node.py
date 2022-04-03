

class YarnNode:
    """
    Data structure for a Yarn Spinner node.  Kinda.
    """
    def __init__(self, header_dict, threads_list, raw_parse_text) -> None:
        self.raw_parse_text = raw_parse_text

        self.header = header_dict
        self.threads = threads_list

        try:
            self.title = header_dict["title"]
        except:
            raise Exception("YarnNode didn't have a title.", raw_parse_text)

