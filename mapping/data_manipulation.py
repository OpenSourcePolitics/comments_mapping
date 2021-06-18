"""
Create a data structure based on an hierarchical tree to map the comments and the
proposals of two distinct csv like files
"""
import csv
import os
import pandas as pd
from mapping.utils.node_proposal import NodeProposal
from mapping.utils.node_comment import NodeComment


def get_data(comment_file_path, proposal_file_path):
    """
    This function is a temporary. It deals with file reading and convert it to a pandas dataframe
    used in tests and for local execution
    :param comment_file_path: path to the comment file
    :type comment_file_path: str
    :param proposal_file_path: path to the proposal file
    :type proposal_file_path: str
    :return: two dataframes : one storing the proposal and the other storing the comments
    :rtype: tuple
    """
    df_coms = pd.read_excel(comment_file_path)
    df_props = pd.read_excel(proposal_file_path)
    return df_props, df_coms


def create_parent_prop(dataframe_prop, commentable_id, comment_object, hash_proposals):
    """
    Create a proposal parent Node when it is not already stored in HASH_PROP
    :param dataframe_prop: data structure containing all proposals
    :param commentable_id: identifier stored in comments pointing to a proposal identifier
    :param comment_object: Node object created from a comment -> will be the child in the parent
    node
    :param hash_proposals:
    """
    specific_row = dataframe_prop.loc[dataframe_prop["id"] == commentable_id]
    prop_node = NodeProposal(title=specific_row["title"].values[0],
                             body=specific_row["body"].values[0],
                             children=[comment_object],
                             supports=specific_row["endorsements/total_count"].values[0])
    hash_proposals[int(specific_row["id"].values[0])] = prop_node
    return hash_proposals


def create_parent_comments(dataframe_comments, commentable_id, comment_object, hash_comments):
    """
    Create a comment parent Node when it is not already stored in hash_comments
    :param dataframe_comments: data structure containing all comments
    :param commentable_id: identifier stored in comments pointing to another comment identifier
    :param comment_object: Node object created from a comment -> will be the child in the parent
    node
    :param hash_comments:
    """
    specific_row = dataframe_comments.loc[dataframe_comments["id"] == commentable_id]
    comments_node = NodeComment(body=specific_row["body"].values[0], children=[comment_object])
    hash_comments[int(specific_row["id"].values[0])] = comments_node
    return hash_comments


def init_index(proposals_dataframe, comments_dataframe):
    """
    This algorithm will iterate on all the comments and map them in two distinct dictionaries
    with their respective parents. It will create a tree data structure where all the proposals
    are the roots of the tree and the comments are the leaves.
    Mapping is done thanks to the children argument in the Node class
    :param proposals_dataframe: data structure containing all proposals
    :param comments_dataframe: data structure containing all comments
    :return: dictionary storing all parent objects -> proposals object
    :rtype: dict
    """
    hash_proposals = {}
    hash_comments = {}
    for com in comments_dataframe.iterrows():
        id_com = com[1]["id"]
        if id_com in hash_comments.keys():
            comment = hash_comments[id_com]
        else:
            comment = NodeComment(body=com[1]["body"], children=[])
            hash_comments[id_com] = comment
        if com[1]["depth"] == 0:
            if com[1]['commentable_id'] in hash_proposals.keys():
                parent = hash_proposals[com[1]['commentable_id']]
                parent.children.append(comment)
            else:
                hash_proposals = create_parent_prop(proposals_dataframe,
                                                    commentable_id=com[1]['commentable_id'],
                                                    comment_object=comment,
                                                    hash_proposals=hash_proposals)

        else:
            if com[1]["commentable_id"] in hash_comments.keys():
                parent = hash_comments[com[1]['commentable_id']]
                parent.children.append(comment)
            else:
                create_parent_comments(comments_dataframe, commentable_id=com[1]["commentable_id"],
                                       comment_object=comment, hash_comments=hash_comments)
    return list(hash_proposals.values())


def init_txt(hash_proposals):
    """
    This function will call the Node.write_txt() method to output a .txt file of all the proposals
    and their respective comments.
    """
    with open(os.path.join(os.getcwd(), "test_data/mapping_proposals_comments.txt"),
              'w', encoding="utf-8") as txt_file:
        for proposal in hash_proposals:
            txt_file.write("NOUVELLE PROPOSITION\n")
            proposal.write_txt(0, txt_file)
            txt_file.write('\n\n\n\n\n\n\n')


def init_csv(hash_proposals):
    """
    This function will create a .csv file which will display on a single row the
    relative information to a proposal and its comments
    """
    row_list = []
    row_list.append(["titre", "body", "soutiens", "commentaires"])
    for proposal in hash_proposals:
        node_list = []
        row_list.append(proposal.get_attributes_as_list(node_list))
        if os.path.basename(os.path.normpath(os.getcwd())) != "comments_mapping":
            os.chdir('..')
        with open(os.path.join(os.getcwd(), "test_data/mapping_proposals_comments.csv"),
                  'w', newline="") as file:
            writer = csv.writer(file)
            writer.writerows(row_list)

    dataframe = pd.DataFrame(row_list)
    return dataframe
