import numpy as np


class UnitGroup:
    """It stores information related to the inputs and targets of event of event class.
    It can be target OR input based on the variable doing_inputs.
    Used to be called Range class.

    ===================================================================================

    :param group_name:
    :type group_name: str
    :param num_units:
    :type num_units: int
    :param first_unit:
    :type first_unit: np
    :param group:
    :type group: np
    :param value:
    :type value: float
    :param unit:
    :type unit: int
    :param event: the Event in which this UnitGroup belongs to
    :type event: Event
    """

    group_name: str  # If null, unit offsets are for the net
    num_units: int
    first_unit: np  # Only used for dense encodings
    # float replaces real
    group: np  # Only used for dense encodings
    # numpy array containing all units in this group

    value: float  # Only used for sparse encodings
    unit: int  # Only used for sparse encodings
    event = None

    def __init__(self, V, num_units: int, group_name=None):
        self.event = V
        self.group_name = group_name
        self.group = np.array([])
        self.num_units = num_units

    def add_units(self, doing_inputs: bool, unit_value=None):
        """ Add unit_value to the group. If unit_value is not given, then a default value
        will be added instead: adds default_input if doing_inputs is true, or else
        adds default_target.

        :param doing_inputs: true if this UnitGroup object is the input of an Event; false otherwise
        :type doing_inputs: bool
        :param unit_value: value of the unit to be added to group
        :type unit_value: str
        """
        if unit_value is not None:  # if value is not given, use default
            if unit_value == "-":
                self.group = np.append(self.group, [float("NaN")])
            elif unit_value.isdigit():
                self.group = np.append(self.group, [unit_value])
            else:
                return False
        else:
            if doing_inputs:  # if the Range is an input
                self.group = np.append(self.group, [self.event.default_input])
            else:
                self.group = np.append(self.group, [self.event.default_target])
        return True

    def check_units_size(self, doing_inputs: bool) -> bool:
        """ Return True if self.group size is the correct number of units. Otherwise, fills self.group
        with default values until it reaches the correct number of units and return False.

        :param doing_inputs: true if this UnitGroup object is the input of an Event; false otherwise
        :type doing_inputs: bool
        :return: true if self.group size is the correct number of unit.
        :rtype: bool
        """
        if self.group.size > self.num_units:
            return False
        elif self.group.size < self.num_units:
            if doing_inputs:
                while self.group.size != self.num_units:
                    self.group = np.append(self.group, [self.event.default_input])
            else:
                while self.group.size != self.num_units:
                    self.group = np.append(self.group, [self.event.default_target])
        if doing_inputs:
            self.event.input_group.append(self.group)
        else:
            self.event.target_group.append(self.group)
        return True
