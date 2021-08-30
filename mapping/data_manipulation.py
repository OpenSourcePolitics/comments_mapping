"""
Create a data structure based on an hierarchical tree to map the comments and the
proposals of two distinct csv like files
"""
import os
import csv
import json
import docx
import pandas as pd
from mapping.utils.node_proposal import NodeProposal
from mapping.utils.node_comment import NodeComment

DATA_MANIPULATION_PATH = os.path.split(os.path.realpath(__file__))[0]


def read_local_json_data(json_file_path):
    """
    Used to read json file saved locally containing the data as such :
    {
    "proposals_file": {PROPOSAL_DATA},
    "comments_file": {COMMENTS_DATA},
    }
    This function loads the content and returns it to be parsed by
    other functions.
    :param json_file_path: path to the data to be mapped
    :type json_file_path: str
    :return: dictionary storing the data
    :rtype: dict
    """
    with open(json_file_path, encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data


def get_data(post_request_json_object=None, local_json_file_path=None):
    """
    Parse a json object to retrieve the proposal data and the comment data. Can be used
    to parse either the result of a post request (json) send by the client or to parse
    local data.
    In either way the data should be formatted in the same way.
    :param post_request_json_object: result of the post request received by the API
    :type post_request_json_object: dict
    :param local_json_file_path: path to the local data to be loaded and parsed
    :type local_json_file_path: str
    :return: tuple of pandas dataframe storing first the proposals and then the comments
    :rtype: tuple
    """
    if post_request_json_object is None:
        post_request_json_object = read_local_json_data(local_json_file_path)
    df_proposals = pd.DataFrame.from_dict(post_request_json_object["Proposals"], orient='index')
    df_comments = pd.DataFrame.from_dict(post_request_json_object["Comments"], orient='index')
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
    with open(os.path.join(DATA_MANIPULATION_PATH, "../dist/mapping_proposals_comments.txt"),
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
        if os.path.basename(os.path.normpath(DATA_MANIPULATION_PATH)) != "comments_mapping":
            os.chdir('..')
        with open(os.path.join(DATA_MANIPULATION_PATH, "../dist/mapping_proposals_comments.csv"),
                  'w', newline="", encoding="utf-8") as file:
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
    if sorting_attribute is None:
        sorting_attribute = "comments"
    sorted_hash_proposals = sort_proposal_objects(hash_proposals, sorting_attribute=sorting_attribute)
    document = docx.Document()
    for proposal in sorted_hash_proposals:
        proposal.write_docx(0, document)
        document.add_page_break()
    document.save(os.path.join(DATA_MANIPULATION_PATH, "../dist/mapping_proposals_comments.docx"))
