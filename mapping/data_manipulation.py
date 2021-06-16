"""
Create an data structure based on an hierarchical tree to map the comments and the
proposals of two distinct csv like files
"""
import csv
import os
import pandas as pd

HASH_PROP = {}
HASH_COMS = {}


class Node:
    """
    Class that will be used to instantiate a tree structure from the initial data :
    proposals : roots
    comments : leaves
    children system : dependency between comments and proposals used
    to link the comment to the proposal
    """
    def __init__(self, title, body, children):
        """
        initialize a Node object
        :param title: proposal title or "Commentaire" for all comments
        :param body: proposal or comment body
        :param children: list of all Node that link this object
        """
        self.title = title
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
        print(indent + "title : {}".format(self.title))
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
        file.write(indent + self.title + '\n')
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
        node_list.append(self.title)
        node_list.append(self.body)
        for child in self.children:
            child.get_attributes_as_list(node_list)
        clean_list = list(filter(None, node_list))
        clean_list = list(filter(lambda l: l != "Commentaire", clean_list))
        return clean_list


def create_parent_prop(dataframe_prop, commentable_id, comment_object):
    """
    Create a proposal parent Node when it is not already stored in HASH_PROP
    :param dataframe_prop: data structure containing all proposals
    :param commentable_id: identifier stored in comments pointing to a proposal identifier
    :param comment_object: Node object created from a comment -> will be the child in the parent
    node
    """
    specific_row = dataframe_prop.loc[dataframe_prop["id"] == commentable_id]
    prop_node = Node(title=specific_row["title"].values[0], body=specific_row["body"].values[0],
                     children=[comment_object])
    HASH_PROP[int(specific_row["id"].values[0])] = prop_node


def create_parent_comments(dataframe_comments, commentable_id, comment_object):
    """
    Create a comment parent Node when it is not already stored in HASH_COMS
    :param dataframe_comments: data structure containing all comments
    :param commentable_id: identifier stored in comments pointing to another comment identifier
    :param comment_object: Node object created from a comment -> will be the child in the parent
    node
    """
    specific_row = dataframe_comments.loc[dataframe_comments["id"] == commentable_id]
    comments_node = Node(title="", body=specific_row["body"].values[0], children=[comment_object])
    HASH_COMS[int(specific_row["id"].values[0])] = comments_node


def init_index(proposals_dataframe, comments_dataframe):
    """
    This algorithm will iterate on all the comments and map them in two distinct dictionaries
    with their respective parents. It will create a tree data structure where all the proposals
    are the roots of the tree and the comments are the leaves.
    Mapping is done thanks to the children argument in the Node class
    :param proposals_dataframe: data structure containing all proposals
    :param comments_dataframe: data structure containing all comments

    """
    for com in comments_dataframe.iterrows():
        id_com = com[1]["id"]
        if id_com in HASH_COMS.keys():
            comment = HASH_COMS[id_com]
        else:
            comment = Node(title="Commentaire", body=com[1]["body"], children=[])
            HASH_COMS[id_com] = comment
        if com[1]["depth"] == 0:
            if com[1]['commentable_id'] in HASH_PROP.keys():
                parent = HASH_PROP[com[1]['commentable_id']]
                parent.children.append(comment)
            else:
                create_parent_prop(proposals_dataframe, commentable_id=com[1]['commentable_id'],
                                   comment_object=comment)

        else:
            if com[1]["commentable_id"] in HASH_COMS.keys():
                parent = HASH_COMS[com[1]['commentable_id']]
                parent.children.append(comment)
            else:
                create_parent_comments(comments_dataframe, commentable_id=com[1]["commentable_id"],
                                       comment_object=comment)


def init_txt():
    """
    This function will call the Node.write_txt() method to output a .txt file of all the proposals
    and their respective comments.
    """
    with open(os.path.join(os.getcwd(), "test_data/mapping_proposals_comments.txt"),
              'w', encoding="utf-8") as txt_file:
        for proposal in HASH_PROP.values():
            txt_file.write("NOUVELLE PROPOSITION\n")
            proposal.write_txt(0, txt_file)
            txt_file.write('\n\n\n\n\n\n\n')


def init_csv():
    """
    This function will create a .csv file which will display on a single row the
    relative information to a proposal and its comments
    """
    row_list = []
    node_list = []
    row_list.append(["titre", "body", "commentaires"])
    for proposal in HASH_PROP.values():
        row_list.append(proposal.get_attributes_as_list(node_list))
    with open(os.path.join(os.getcwd(), "test_data/mapping_proposals_comments.csv"),
              'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerows(row_list)


if __name__ == '__main__':
    if os.path.basename(os.path.normpath(os.getcwd())) != "comments_mapping":
        os.chdir("..")
    df_comments = pd.read_excel(os.path.join(os.getcwd(), "test_data/comments_custom.xls"))
    df_proposals = pd.read_excel(os.path.join(os.getcwd(), "test_data/proposals_custom.xls"))
    init_index(proposals_dataframe=df_proposals, comments_dataframe=df_comments)
    init_csv()
    init_txt()
