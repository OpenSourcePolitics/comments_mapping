"""
Create an data structure based on an hierarchical tree to map the comments and the
proposals of two distinct csv like files
"""
import pandas as pd

HASH_PROP = {}
HASH_COMS = {}


class Node:
    def __init__(self, title, body, children):
        self.title = title
        self.body = body
        self.children = children

    def debug(self, indent_num):
        indent = 2 * indent_num * " "
        print(indent + "Node")
        print(indent + "title : {}".format(self.title))
        print(indent + "body: {}".format(self.body))
        for child in self.children:
            child.debug(indent_num + 1)


def create_parent_prop(dataframe_prop, commentable_id, comment_id):
    specific_row = dataframe_prop.loc[dataframe_prop["id"] == commentable_id]
    prop_node = Node(title=specific_row["title"].values[0], body=specific_row["body"].values[0],
                     children=[comment_id])
    HASH_PROP[int(specific_row["id"].values[0])] = prop_node


def create_parent_comments(dataframe_comments, commentable_id, comment_object):
    specific_row = dataframe_comments.loc[dataframe_comments["id"] == commentable_id]
    comments_node = Node(title="", body=specific_row["body"].values[0], children=[comment_object])
    HASH_COMS[int(specific_row["id"].values[0])] = comments_node


def init_index(proposals_dataframe, comments_dataframe):
    for com in comments_dataframe.iterrows():
        id_com = com[1]["id"]
        if id_com in HASH_COMS.keys():
            comment = HASH_COMS[id_com]
        else:
            comment = Node(title=com[1]["id"], body=com[1]["body"], children=[])
            HASH_COMS[id_com] = comment
        if com[1]["depth"] == 0:
            if com[1]['commentable_id'] in HASH_PROP.keys():
                parent = HASH_PROP[com[1]['commentable_id']]
                parent.children.append(comment)
            else:
                create_parent_prop(proposals_dataframe, commentable_id=com[1]['commentable_id'],
                                   comment_id=comment)

        else:
            if com[1]["commentable_id"] in HASH_COMS.keys():
                parent = HASH_COMS[com[1]['commentable_id']]
                parent.children.append(comment)
            else:
                create_parent_comments(comments_dataframe, commentable_id=com[1]["commentable_id"],
                                       comment_object=comment)


def init_txt():
    with open("mapping_proposals_comments.txt", 'w', encoding="utf-8") as file:
        for proposal in HASH_PROP.values():
            file.write(proposal.title.values[0] + '\n')
            file.write(proposal.body.values[0] + '\n')
            file.write('Commentaires : \n')
            for comments in proposal.children:
                file.write(comments.body)
            file.write('\n\n\n\n\n\n\n')


def init_csv():
    pass


if __name__ == '__main__':
    df_comments = pd.read_excel("./../test_data/comments_FEAMP.xls")
    df_proposals = pd.read_excel("./../test_data/proposals_FEAMP.xls")
    init_index(proposals_dataframe=df_proposals, comments_dataframe=df_comments)
    prop = HASH_PROP[1567]
    prop.debug(0)
