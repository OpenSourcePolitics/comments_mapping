"""
Create a data structure based on an hierarchical tree to map the comments and the
proposals of two distinct csv like files
"""
import csv
import os
import docx
import pandas as pd
from mapping.utils.node_proposal import NodeProposal
from mapping.utils.node_comment import NodeComment


def get_data(json_object):
    """
    Parse a json object to retrieve the proposal data and the comment data
    """
    df_proposals = pd.DataFrame.from_dict(json_object["proposals_file"], orient='index')
    df_comments = pd.DataFrame.from_dict(json_object["comments_file"], orient='index')
    return df_proposals, df_comments


def keep_fr_local(df_props):
    """
    Renames the body/fr, title/fr, category/name/fr columns in body, title, category => only the french local
    will be kept for mapping
    :param df_props: dataframe structure storing the proposals
    :return:updated dataframe
    """
    for column in df_props.columns:
        if column == "title/fr":
            df_props = df_props.rename(columns={"title/fr": "title"})
        elif column == "body/fr":
            df_props = df_props.rename(columns={"body/fr": "body"})
        elif column == "category/name/fr":
            df_props = df_props.rename(columns={"category/name/fr": "category"})
    return df_props


def column_cleaning(df_props):
    """
    rename the column storing the supports into endorsements to deal
    with the different versions of decidim
    :param df_props: dataframe structure storing the proposals
    :return:updated dataframe
    """
    df_props = keep_fr_local(df_props)
    for column in df_props.columns:
        if column.startswith("endorsements"):
            df_props = df_props.rename(columns={column: "endorsements"})
    return df_props


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
                             supports=specific_row["endorsements"].values[0],
                             nb_comments=specific_row["comments"].values[0],
                             category=specific_row["category"].values[0])
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
    :return: list storing all parent objects -> proposals object
    :rtype: list
    """
    proposals_dataframe = column_cleaning(proposals_dataframe)
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


def sort_proposal_objects(hash_proposals, sorting_attribute):
    """
    sort the objects based on the argument given by the user : either supports or "comments".
    the most commented proposals or the most supported will be displayed first
    :param hash_proposals: list storing all parent objects -> proposals object
    :param sorting_attribute: either "supports" or "comments"
    :return: sorted list
    :rtype: list
    """
    if sorting_attribute == "supports":
        sorted_list = sorted(hash_proposals, key=lambda x: x.supports, reverse=True)
    elif sorting_attribute == "comments":
        sorted_list = sorted(hash_proposals, key=lambda x: x.nb_comments, reverse=True)
    return sorted_list


def init_txt(hash_proposals, sorting_attribute=None):
    """
    This function will call the Node.write_txt() method to output a .txt file of all the proposals
    and their respective comments.
    :param hash_proposals: list of parent objects
    :param sorting_attribute: either "supports" or "comments"
    """
    if sorting_attribute is None:
        sorting_attribute = "comments"
    sorted_hash_proposals = sort_proposal_objects(hash_proposals, sorting_attribute=sorting_attribute)
    with open(os.path.join(os.getcwd(), "dist/mapping_proposals_comments.txt"),
              'w', encoding="utf-8") as txt_file:
        for proposal in sorted_hash_proposals:
            txt_file.write("NEW PROPOSAL\n")
            proposal.write_txt(0, txt_file)
            txt_file.write('\n\n\n\n\n\n\n')
            txt_file.write('\f')


def init_csv(hash_proposals, sorting_attribute=None):
    """
    This function will create a .csv file which will display on a single row the
    relative information to a proposal and its comments
    :param hash_proposals: list of parent objects
    :param sorting_attribute: either "supports" or "comments"
    :return: structured dataframe
    """
    if sorting_attribute is None:
        sorting_attribute = "comments"
    sorted_hash_proposals = sort_proposal_objects(hash_proposals, sorting_attribute=sorting_attribute)
    row_list = [["title", "body", "category", "supports", "amount of comments", "comments list"]]
    for proposal in sorted_hash_proposals:
        node_list = []
        row_list.append(proposal.get_attributes_as_list(node_list))
        if os.path.basename(os.path.normpath(os.getcwd())) != "comments_mapping":
            os.chdir('..')
        with open(os.path.join(os.getcwd(), "dist/mapping_proposals_comments.csv"),
                  'w', newline="") as file:
            writer = csv.writer(file)
            writer.writerows(row_list)

    dataframe = pd.DataFrame(row_list)
    return dataframe


def init_docx(hash_proposals, sorting_attribute=None):
    """
    This function will create a docx file that will display each proposal on a new page with
    some layout for readability
    :param hash_proposals: list of parent objects
    :param sorting_attribute: either "supports" or "comments"
    """
    if sorting_attribute is None :
        sorting_attribute = "comments"
    sorted_hash_proposals = sort_proposal_objects(hash_proposals, sorting_attribute=sorting_attribute)
    document = docx.Document()
    for proposal in sorted_hash_proposals:
        proposal.write_docx(0, document)
        document.add_page_break()
    document.save(os.path.join(os.getcwd(), "dist/mapping_proposals_comments.docx"))
