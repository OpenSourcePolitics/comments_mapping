"""
This file defines the child class NodeProposal which inherits from the class Node
"""
from mapping.utils.node import Node


class NodeProposal(Node):
    """
    Child class that inherits from the Node class. It is used to manage the information
    specific to proposals.
    """

    def __init__(self, title, body, children, supports):
        Node.__init__(self, body, children)
        self.title = title
        self.supports = supports

    def write_txt(self, indent_num, file):
        """
        Recursive function that will iterate on a proposal and all of its children in order
        to write down all the information in a structured way on a txt file
        :param indent_num: initial indentation value
        :type indent_num: int
        :param file: opened file cf- init_txt()
        """
        indent = 2 * indent_num * " "
        file.write(indent + 'Titre : ' + self.title + '\n')
        file.write(indent + 'Corps de contribution : ' + self.body + '\n')
        file.write(indent + 'Soutiens : ' + str(self.supports) + '\n\n')
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
        node_list.append(self.title)
        node_list.append(self.body)
        node_list.append(self.supports)
        for child in self.children:
            child.get_attributes_as_list(node_list)
        return node_list
