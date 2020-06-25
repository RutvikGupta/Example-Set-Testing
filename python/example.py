import re

"""/* EXAMPLE FIELDS */"""
DEF_E_frequency = 1.0


class Example:
    """ Example class. The object which stores information related to one example of the
    ExampleSet and has a list of events which will be executed by the neural network

    :param name: name of Example
    :type name: str
    :param: num:
    :type num: int
    :param num_events:
    :type num_events: int
    :param event: list of Events in this example
    :type event: List[Event]
    :param set: the ExampleSet in which this example belows to
    :type set: ExampleSet
    :param next: next example
    :type next: Example
    """

    name = None  #: str
    num = 0  # : int
    num_events = 0  #: int
    event = []  #: List[Event]
    set = None  #: ExampleSet
    next = None  #: Example
    # float replaces real
    frequency: float
    probability = 0.0  #: float
    events_data = []
    event_headers = []
    proc = None

    # proc function is defined in the C macros

    def __init__(self, S, frequency=DEF_E_frequency):
        self.frequency = frequency
        self.set = S
        self.event = []
        self.events_data = []
        self.event_headers = []

        # initExampleExtension(E)

    def parse_example_arguments(self, example_array: str) -> str:
        """ Parse through example_array to find Example arguments and set the values
        in Example accordingly

        :param example_array:
        :type example_array:
        :return: new example array after the parsed parameters are removed
        """

        if "name:" in example_array:
            index = example_array.find("name:")
            find_newline = example_array[index:].find("\n") + index
            example_name = example_array[index + len("name:"): find_newline].strip()
            if example_name == "":
                self.name = self.set.example.index(self)
            else:
                self.name = example_name
                example_array = example_array.replace(example_array[index: find_newline + 1], '')

        if "freq:" in example_array:
            index = example_array.find("freq:")
            find_newline = example_array[index:].find("\n") + index
            example_freq = example_array[index + len("freq:"): find_newline]
            p = re.compile("([0-9]+\.[0-9]+)|[0-9]+")
            if p.match(example_freq):
                self.frequency = float(example_freq)
                example_array = example_array.replace(example_array[index: find_newline + 1], '')
            else:
                return self.set.parseError("missing value after \"freq:\" in header of example " + str(
                        self.example.set.example.index(self.example)))

        if "proc:" in example_array:
            index = example_array.find("proc:")
            find_newline = example_array[index:].find("\n") + index
            example_proc = example_array[index + len("proc:"): find_newline]
            self.proc = example_proc
            example_array = example_array.replace(example_array[index: find_newline + 1], '')

        regex = re.compile("(^|\\n)[0-9]+(\\n|$)")
        matched = regex.search(example_array)
        if matched is not None:
            start = matched.start()
            end = matched.end()
            num = example_array[start: end].strip()
            if num.isdigit():
                self.num_events = int(num)
                example_array = example_array.replace(example_array[start: end], '')

        return example_array

    def parse_example_string(self, example_array: str):
        """ Sorts the string of an Example, example_array, into event headers and event dada
        :param example_array: The string of an Example
        :type example_array: str
        :return:
        """
        self.event_headers = re.findall(r'\[(.+)\]', example_array)
        if len(self.event_headers) == 0:
            self.num_events = 1
        else:
            self.num_events = len(self.event_headers)
            self.events_data = re.split(r'\[.+\]', example_array)

    def print_out(self):
        self.print_out_example()

    def print_out_example(self, printing=True, tabs=0):
        """ Prints out the instance variables of an Example and of its Events
        This function is a work in progress for testing purposes.
        Each new layer of composition is indicated by indent.

        If calling this function directly, please leave
        printing=True and tabs=0 to their default values.
        """
        ex = self
        L = [("Obj", "Example"), ("name", ex.name), ("num", ex.num)]
        if ex.next is not None:
            next_name = ex.next.name
        else:
            next_name = None
        s = ""
        L.extend([("numEvents", ex.num_events), ("set.name", ex.set.name), ("next.name", next_name),
                  ("frequency", ex.frequency), ("probability", ex.probability)])
        s += format_object_line(L, tabs)
        for event_num in range(len(ex.event)):
            ev = ex.event[event_num]
            s += ev.print_out_event(False, tabs + 1)
        if printing:
            print(s)
        return s


def tab(n=1):
    return "     " * n


def format_object_line(L, num_tabs=0, row_size=10):
    s = tab(num_tabs)
    size = row_size
    for item in L:
        s += item[0] + " = " + str(item[1]) + ", "
        # if row_size == 0:
        #     s += "\n" + tab(num_tabs)
        #     row_size = size
        # row_size -= 1
    return s + "\n"
