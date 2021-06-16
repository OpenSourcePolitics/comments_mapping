"""
This file defines the parent class Node
"""


class Node:
    """
    Class that will be used to instantiate a tree structure from the initial data :
    proposals : roots
    comments : leaves
    children system : dependency between comments and proposals used
    to link the comment to the proposal
    """

    def __init__(self, body, children):
        """
        initialize a Node object
        :param body: proposal or comment body
        :param children: list of all Node that link this object
        """
        self.body = body
        self.children = children

    def debug(self, indent_num):
        """
        debug function that will print a vertical output of the data structure
        :param indent_num: initial indentation value
        :type indent_num: int
        """
        indent = 2 * indent_num * " "
        print(indent + "Node")
        print(indent + "body: {}".format(self.body))
        for child in self.children:
            child.debug(indent_num + 1)

    def write_txt(self, indent_num, file):
        """
        Recursive function that will iterate on a proposal and all of its children in order
        to write down all the information in a structured way on a txt file
        :param indent_num: initial indentation value
        :type indent_num: int
        :param file: opened file cf- init_txt()
        """
        indent = 2 * indent_num * " "
        file.write(indent + self.body + '\n')
        for child in self.children:
            child.write_txt(indent_num + 1, file)

    def get_attributes_as_list(self, node_list):
        """
        Function that will iterate from a proposal through all of its children to
        retrieve the information stored in the object and append it successively to a list
        :param node_list: list that will be progressively filled
        :type node_list: list
        :return: [proposal title, proposal body, comment 1, ..., comment n]
        :rtype: list
        """
        node_list.append(self.body)
        for child in self.children:
            child.get_attributes_as_list(node_list)
        return node_list
