from example import Example
from typing import Optional, List
import random

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
        self.example = S.example
        self.num_examples = len(self.example_set.example)
        self.index_list = []
        self.sort_examples()
        # self.index_list = self.example_set.example_index
        print(self.index_list)
        self.iter_list = []
        self.cycle_num = 0
        self.link_up_index_list()
        # self.reset_example_list()

    def link_up_index_list(self):
        for i in range(self.num_examples):
            self.iter_list.append(ExampleIndex(self.index_list[i]))

        for i in range(1, self.num_examples):
            self.iter_list[i - 1].next = self.iter_list[i]
        for i in range(self.num_examples - 2, -1, -1):
            self.iter_list[i + 1].prev = self.iter_list[i]
        self.curr = self.iter_list[0]

    def iterate_example(self) -> Optional[Example]:
        """ Returns the example at index self.curr_ex_index and increments self.curr_ex_index
        of self.example_sorted. If the index is the last index of the list, re-sort the list.
        :return: next example
        :rtype: Example
        """
        ex = self.example[self.curr.value]
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
        self.sort_examples()
        self.link_up_index_list()
        self.cycle_num += 1

    def print_out_examples(self):
        s = ""
        for e in self.iter_list:
            s += " -> "
            s += self.example_set.example[e.value].name + " i=" + str(e)
        print(s)

    def sort_examples(self):
        """ Fills self.example_sorted, which is the list of indexes in self.examples
        but sorted by self.sort_mode
        In ORDERED mode, which is the default, examples will be presented in the order in
        which they were found in the example file.
        In RANDOMIZED mode, examples will be selected at random with replacement,
        each having the same probability of selection. Note that this differs from
        PERMUTED because it uses replacement. It differs from PROBABILISTIC because it
        ignores the example frequency.
        In PERMUTED mode, examples will be selected at random without replacement,
        each having the same probability of selection. A different order will be
        computed for each pass through the set.
        In PROBABILISTIC mode, examples are selected based on their given frequency.
        Specified frequency values will be normalized over all examples and this
        distribution used for selection. If example sets are concatenated, the distribution
        will be recalculated based on the specified frequencies. An example with no
        frequency specified is given a value of 1.0.
        PIPE mode is used for example sets that are reading from a pipe. The next example
        will be read from the pipe and stored temporarily in the example set's pipeExample
        field. This mode can only be used with example sets for which a pipe was opened
        with "loadExamples ... -m PIPE". If the pipe is exhausted and the example set's
        pipeLoop flag is set to TRUE, which is the default, the pipe will be re-opened
        automatically. If an example set contains both stored examples and an open pipe,
        you can switch between them by changing from PIPE mode to another mode.
        CUSTOM mode allows you to write a procedure that generates the index of the next example. When it's time to
        choose the next example, the example set's chooseExample procedure will be called. This should return an integer
         between 0 and one less than the number of examples, inclusive.
        """
        mode = self.example_set.sort_mode
        self.index_list = []
        if mode == "ORDERED":
            for i in range(self.num_examples):
                self.index_list.append(i)
        elif mode == "RANDOMIZED":
            for _ in range(self.num_examples):
                random_index = random.randint(0, self.num_examples - 1)
                self.index_list.append(random_index)
        elif mode == "PERMUTED":
            for i in range(self.num_examples):
                self.index_list.append(i)
            random.shuffle(self.index_list)
        elif mode == "PROBABILISTIC":
            total_freq = 0.0
            freq_cum = [0.0]
            # cumulative frequency of all previous examples parsed. the greater the frequency
            # of an example, the greater the increment over the previous value.
            for e in self.example:
                if isinstance(e.frequency, float):
                    total_freq += e.frequency
                else:
                    total_freq += 0.0
                    # return self.parseError("error reading frequency")
                freq_cum.append(total_freq)
            for _ in range(self.num_examples):
                random_choice = random.random() * total_freq
                index = 0
                while freq_cum[index + 1] < random_choice:
                    index += 1
                self.index_list.append(index)
        elif mode == "PIPE":
            # TODO
            pass
        elif mode == "CUSTOM":
            # TODO
            pass
        else:
            return self.example_set.parseError("invalid sort mode")