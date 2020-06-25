def sort_examples_by_mode(self, mode="ORDERED"):
    """ Fills self.example_sorted, which is the list of indexes in self.examples
    but sorted by mode.

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
    :param mode:
    :return:
    """
    mode = mode.upper()
    self.sort_mode = mode
    self.example_sorted = []
    self.example_sel = []

    if mode == "ORDERED":
        for i in range(self.num_examples):
            self.example_sorted.append(i)
            self.example_sel.append(self.example[i])
    elif mode == "RANDOMIZED":
        for _ in range(self.num_examples):
            random_index = random.randint(0, self.num_examples - 1)
            self.example_sorted.append(random_index)
            self.example_sel.append(self.example[random_index])
    elif mode == "PERMUTED":
        for i in range(self.num_examples):
            self.example_sorted.append(i)
        random.shuffle(self.example_sorted)
        self.example_sel = copy.copy(self.example)
        random.shuffle(self.example_sel)

    elif mode == "PROBABILISTIC":
        total_freq = 0.0
        freq_cum = [0.0]
        # cumulative frequency of all previous examples parsed. the greater the frequency
        # of an example, the greater the increment over the previous value.
        for e in self.example:
            if isinstance(e.frequency, float):
                total_freq += e.frequency
            else:
                return self.parseError("error reading frequency")
            freq_cum.append(total_freq)
        for _ in range(self.num_examples):
            random_choice = random.random() * total_freq
            example_index = 0
            while freq_cum[example_index + 1] < random_choice:
                example_index += 1
            self.example_sorted.append(example_index)
            self.example_sel.append(self.example[example_index])

    elif mode == "PIPE":
        # TODO
        pass
    elif mode == "CUSTOM":
        # TODO
        pass
    else:
        return self.parseError("invalid example selection mode")


 def iterate_example(self) -> Optional[Example]:
        """ Returns the example at index self.curr_ex_index and increments self.curr_ex_index
        of self.example_sorted. If the index is the last index of the list, re-sort the list.
        :return: next example
        :rtype: Example
        """

        # TODO
        # Note: the current linked list implementation only works when new sorted
        # examples list do not have duplicate examples i.e. permutated

        # TODO for now, please don't use example.next ... instead, get the next index

        original_examples_list_index = self.example_sorted[self.curr_ex_index]
        if self.curr_ex_index == self.num_examples - 1:
            self.reset_example_list(self.sort_mode)
        else:
            self.curr_ex_index += 1
        return self.example[original_examples_list_index]

        # if self.current_example is None:
        #     return None
        # if self.current_example.next is None or self.current_example is self.last_example:
        #     self.reset_example_list()
        # self.current_example = self.current_example.next
        # return self.current_example

    def reset_example_list(self, mode="ORDERED"):
        """ Re-sort the example list according to mode and updates first_example,
        last_example and each example.next accordingly.
        :param mode: mode to sort example
        :type mode: str
        """
        if not self.example:
            return
        self.example_sorted = []
        self.sort_examples_by_mode(mode)
        self.first_example = self.example[self.example_sorted[0]]
        self.current_example = self.first_example
        self.curr_ex_index = 0
        self.last_example = self.example[self.example_sorted[-1]]
        self.last_example.next = None
        # TODO
        # Note: the current linked list implementation only works when new sorted
        # examples list do not have duplicate examples i.e. permutated
        for e in range(self.num_examples - 1):
            this_example = self.example[self.example_sorted[e]]
            next_example = self.example[self.example_sorted[e + 1]]
            this_example.next = next_example
        self.cycle_num += 1