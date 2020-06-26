from python.example import Example
from typing import Optional, List


class ExampleIndex:
    def __init__(self, value: int):
        self.next = None
        self.prev = None
        self.value = value


class ExampleIterator:
    curr: ExampleIndex
    iter_list: List[ExampleIndex]
    num_examples: int

    def __init__(self, S, sort_mode: str):
        self.example_set = S
        self.index_list = self.example_set.example_index
        self.num_examples = len(self.example_set.example)
        self.iter_list = []
        self.cycle_num = 0
        self.reset_example_list()

    def link_up_index_list(self):
        for i in range(len(self.num_examples)):
            self.iter_list.append(ExampleIndex(self.index_list[i]))

        for i in range(1, len(self.num_examples)):
            self.iter_list[i - 1].next = self.iter_list[i]
        for i in range(len(self.num_examples) - 2, -1, -1):
            self.iter_list[i + 1].prev = self.iter_list[i]
        self.curr = self.iter_list[0]

    def iterate_example(self) -> Optional[Example]:
        """ Returns the example at index self.curr_ex_index and increments self.curr_ex_index
        of self.example_sorted. If the index is the last index of the list, re-sort the list.
        :return: next example
        :rtype: Example
        """
        ex = self.example_set.example[self.curr.value]
        if self.curr.next is None:
            self.reset_example_list()
        else:
            self.curr = self.curr.next
        return ex

    def current_example(self):
        """ Returns current example
        """
        return self.example_set.example[self.curr.value]

    def first_example(self):
        return self.example_set.example[self.iter_list[0].value]

    def last_example(self):
        return self.example_set.example[self.iter_list[-1].value]

    def next_example(self):
        if self.curr.next is None:
            return None
        else:
            return self.example_set.example[self.curr.next.value]

    def prev_example(self):
        if self.curr.prev is None:
            return None
        else:
            return self.example_set.example[self.curr.prev.value]

    def reset_example_list(self):
        """ Re-sort the example list according to mode and updates first_example,
        last_example and each example.next accordingly.
        """
        if not self.example:
            return
        self.example_set.sort_examples()
        self.link_up_index_list()
        self.cycle_num += 1

    def print_out_examples(self):
        s = ""
        for e in self.iter_list:
            s += " -> "
            s += self.example_set.example[e.value].name + " i=" + str(e)
        print(s)
