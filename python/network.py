from python.group import Group
from python.example_set import ExampleSet


class Network:
    name = None
    time_intervals = 0
    input_groups = []
    output_groups = []
    groups = []
    learningRate = 0.5

    # array of example objects to iterate through
    example_sets = []

    def __init__(self, name, time_intervals=1):
        self.name = name
        self.time_intervals = time_intervals

        self.num_groups = 0
        self.num_units = 0
        self.num_inputs = 0
        self.num_outputs = 0

    def add_group(self, num_units, group_type, input_transforms, output_transforms):
        # instantiate a new group object, append it to master list of groups
        new_group = Group(num_units, group_type, input_transforms, output_transforms)
        self.groups.append(new_group)
        self.num_groups += 1
        self.num_units += num_units

        # check if the group is of input or output type, and append it to appropriate array
        if (group_type == "input"):
            self.input_groups.append(new_group)
        elif (group_type == "output"):
            self.output_groups.append(new_group)

        # if type is not input, link it to the group prior to it and initialize incoming weight matrix
        if (group_type != "input"):
            new_group.link_groups(self.groups[self.num_groups - 2].numUnits)

    def forward(self):
        prev_output = None

        # iterate through all of the groups and compute the forward pass for each
        for group in self.groups:
            group.incoming_input(prev_output)
            prev_output = group.forward()

        return prev_output

    def load_example(self, input_matrix):
        # TENTATIVE: sets the first group (input) to what is passed in
        self.groups[0].incoming_input(input_matrix)

    def load_example_set(self, example_set_name: str, file_name: str, default_input=0,
                         active_input=1, default_target=0, active_target=1):
        new_example_set = ExampleSet(self, example_set_name, file_name, default_input,
                                     active_input, default_target, active_target)
        self.example_sets.append(new_example_set)


if __name__ == "__main__":
    mynet = Network("mynet")  # default time intervals (1) ->
    mynet.load_example_set("XOR", "xor_dense.ex")
    mynet.example_sets[0].print_out()

    # mynet.add_group(2, "input", [], [])
    # mynet.add_group(3, None, ["dot"], ["sigmoid"])
    # mynet.add_group(1, "output", ["dot"], ["sigmoid"])
    # mynet.load_example([2,1])
    # print(mynet.forward())
