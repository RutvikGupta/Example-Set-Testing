import net_defaults
import numpy as np
from output_transforms.activation import Activation
from output_transforms.sigmoid import Sigmoid
from output_transforms.hard_clamp import Hard_Clamp
from inputs.input_transform import Input_Transform
from inputs.dot_product import Dot_Product
from link import Link

class Group:
    # links will hold incoming input data to initialize weight matrices
    link = None

    # initialize basic properties of all groups
    num_units = 0
    group_type = 0
    input_matrix = None
    output_matrix = None
    input_transforms = []
    output_transforms = []
    input_set = False

    # lookup table matching different transforms to their respective classes
    activations = {"sigmoid":Sigmoid, "hard_clamp":Hard_Clamp}
    input_types = {"dot":Dot_Product}

    def __init__(self, num_units, group_type, input_transforms, output_transforms):
        self.num_units = num_units
        self.output_transforms = output_transforms
        self.group_type = group_type
        self.input_transforms = input_transforms

        # initialize arrays
        self.input_matrix = np.zeros(num_units)
        self.output_matrix = np.zeros(num_units)

        # if the group is an input group, it doesn't apply any transforms (i.e. what you input, will be outputted)
        if (self.group_type == "input"):
            self.output_transforms.append("hard_clamp")
        
    """
    This function will link the preceding group to itself, building a weight matrix to compute input transforms with the incoming
    inputs
    """
    def link_groups(self, prev_units):
        self.link = Link(prev_units, self.num_units)

    """
    This function sets the input matrix

    TENTATIVE: this could hypothetically be moved to the links class, that way data is moved across connections 
    Pros: intuitive structure of networks for visualization purposes
    Cons: may become overwhelming/confusing when we get into large nets/lots of data to be moving around so frequently
    """
    def incoming_input(self, input_matrix):
        if (not self.input_set):
            self.input_matrix = np.array(input_matrix)
            self.input_set = True

    """
    Iterates through the input transforms provided in the group initialization and applies each transform

    E.G. Applying the dot product between the weight matrix and the incoming matrix to input data in the group
    """
    def input(self):
        if (self.group_type != "input"):
            for transform in self.input_transforms:
                transform_class = self.input_types[transform]()
                self.input_matrix = transform_class.compute(self.link.weights, self.input_matrix)

    """
    Iterates through the output transforms and applies each one

    E.G. Takes the input from the previous step and sends it through the Sigmoid transform function 
    """
    def output(self):
        for transform in self.output_transforms:
            transform_class = self.activations[transform]()
            self.output_matrix = transform_class.forward(self.output_matrix)   
    
    """
    Computes the forward pass in succession of where data should flow,
    Starting at the input, moves the data to the output and then back to the net

    E.G. Data comes in -> Input transforms are applied (dot product, clipping, noise etc.)
    -> Input data is passed to activation function & other output transforms (Sigmoid, clipping) -> return to net.
    """
    def forward(self):
        self.input()
        self.output_matrix = self.input_matrix
        self.output()
        return self.output_matrix