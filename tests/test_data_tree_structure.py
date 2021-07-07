"""
Test data structure
"""
import os

import filecmp
import pytest
from mapping.data_manipulation import init_index, get_data, init_csv, init_txt
from mapping.utils.node_proposal import NodeProposal
from mapping.utils.node_comment import NodeComment

df_prop_config1, df_coms_config1 = get_data("./../test_data/comments_config1.xls",
                                            "./../test_data/proposals_config1.xls")
df_prop_config2, df_coms_config2 = get_data("./../test_data/comments_config2.xls",
                                            "./../test_data/proposals_config2.xls")
df_prop_config3, df_coms_config3 = get_data("./../test_data/comments_config3.xls",
                                            "./../test_data/proposals_config3.xls")


def nodes_equal(node1, node2):
    is_equal = node1.body == node2.body
    for child_node_1, child_node_2 in zip(node1.children, node2.children):
        is_equal = is_equal and nodes_equal(child_node_1, child_node_2)
    return is_equal


CONFIG_1 = [NodeProposal(title="P0 titre",
                         body="P0 body",
                         category="cat",
                         supports=12,
                         nb_comments=4,
                         children=[NodeComment(body="C1",
                                               children=[NodeComment(body="C0",
                                                                     children=[NodeComment(body="R1",
                                                                                           children=[])]),
                                                         NodeComment(body="R2", children=[])])])]

CONFIG_2 = [NodeProposal(title="P0 titre",
                         body="P0",
                         category="cat",
                         supports=12,
                         nb_comments=4,
                         children=[NodeComment(body='C0', children=[]),
                                   NodeComment(body='C1', children=[]),
                                   NodeComment(body='C2', children=[]),
                                   NodeComment(body='C3', children=[])]),
            NodeProposal(title="P1 titre",
                         body="P1",
                         category="cat",
                         supports=5,
                         nb_comments=1,
                         children=[NodeComment(body='C4', children=[])])]

CONFIG_3 = [NodeProposal(title="P0 titre",
                         body="P0",
                         category="cat",
                         supports=12,
                         nb_comments=6,
                         children=[NodeComment(body='C1',
                                               children=[NodeComment(body="R1",
                                                                     children=[NodeComment(body="R2",
                                                                                           children=[NodeComment(body="R3", children=[])])])]),
                                   NodeComment(body='C2', children=[NodeComment(body="R4", children=[])])]),
            NodeProposal(title="P1 titre",
                         body="P1",
                         category="cat",
                         supports=5,
                         nb_comments=0,
                         children=[])]

TEST_CASES_STRUCTURE = [(df_prop_config1, df_coms_config1, CONFIG_1),
                        (df_prop_config2, df_coms_config2, CONFIG_2),
                        (df_prop_config3, df_coms_config3, CONFIG_3)]

TEST_TXT_OUTPUT = [(df_prop_config1, df_coms_config1, os.path.join(os.getcwd(),
                                                                   "../test_data/mapping_result_config1.txt")),
                   (df_prop_config2, df_coms_config2, os.path.join(os.getcwd(),
                                                                   "../test_data/mapping_result_config2.txt")),
                   (df_prop_config3, df_coms_config3, os.path.join(os.getcwd(),
                                                                   "../test_data/mapping_result_config3.txt"))]


@pytest.mark.parametrize("proposals_dataframe, comments_dataframe, output ", TEST_CASES_STRUCTURE)
def test_tree_structure(proposals_dataframe, comments_dataframe, output):
    nodes = init_index(proposals_dataframe, comments_dataframe)
    for node_test, node_validation in zip(nodes, output):
        assert nodes_equal(node_test, node_validation)


@pytest.mark.parametrize("proposals_dataframe, comments_dataframe, output ", TEST_CASES_STRUCTURE)
def test_csv_integrity(proposals_dataframe, comments_dataframe, output):
    hash_prop = init_index(proposals_dataframe, comments_dataframe)
    for elem in output:
        if len(elem.children) == 0:
            output.remove(elem)
    df_test = init_csv(hash_prop)
    assert len(df_test)-1 == len(output)


@pytest.mark.parametrize("proposals_dataframe, comments_dataframe, output", TEST_TXT_OUTPUT)
def test_txt_integrity(proposals_dataframe, comments_dataframe, output):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    hash_prop = init_index(proposals_dataframe, comments_dataframe)
    init_txt(hash_prop)
    assert filecmp.cmp(os.path.join(dir_path, "../dist/mapping_proposals_comments.txt"), output)
