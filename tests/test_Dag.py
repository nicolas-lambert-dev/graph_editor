import pytest

from grapheditor.core.graph.dag import DirectedAcyclicGraph
from grapheditor.core.graph.graph import IGraph
from grapheditor.core.graph.node import Node


@pytest.fixture
def dag_empty() -> IGraph:
    return DirectedAcyclicGraph()


@pytest.fixture
def nodes_10():
    node_names = ["node {}".format(index) for index in range(10)]
    nodes = [Node.new(node_name) for node_name in node_names]
    return nodes


@pytest.fixture
def dag_10_nodes(nodes_10):
    dag = DirectedAcyclicGraph()
    for node in nodes_10:
        dag.add_node(node)
    return dag


def test_construction(dag_empty):
    assert dag_empty


def test_add_node(dag_empty):
    node_1 = Node.new("node 1")
    dag_empty.add_node(node_1)
    assert len(dag_empty.get_nodes()) == 1
    assert dag_empty.get_nodes()[0] == node_1

    node_2 = Node.new("node 2")
    dag_empty.add_node(node_2)
    assert len(dag_empty.get_nodes()) == 2

    # no duplicated nodes allowed
    dag_empty.add_node(node_2)
    assert len(dag_empty.get_nodes()) == 2
    dag_empty.add_node(node_1)
    assert len(dag_empty.get_nodes()) == 2


def test_remove_node(dag_10_nodes, nodes_10):
    assert len(dag_10_nodes.nodes) > 0
    assert True is dag_10_nodes.remove_node(nodes_10[0])

    assert 9 == len(dag_10_nodes.nodes)

    # Removing an non existing node should return False
    node_not_in_dag = Node.new("not in dag")
    assert False is dag_10_nodes.remove_node(node_not_in_dag)
    assert 9 == len(dag_10_nodes.nodes)


def test_dag_should_be_able_to_add_node_connections(dag_10_nodes, nodes_10):
    dag_10_nodes.connect(dag_10_nodes[0], dag_10_nodes[5])


def test_connecting_a_node_to_ancestor_should_throw_an_exception():
    dag = DirectedAcyclicGraph()
    ancestor = dag.add_node(Node("ancestor"))
    child = dag.add_node(Node("child"))
    dag.connect(ancestor, child)

    with pytest.raises(Exception):
        dag.connect(child, ancestor)