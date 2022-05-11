from grapheditor.core.graph.node import Node


def test_construction():
    assert Node("node 1")


def test_name():
    assert "node 1" == Node("node 1").name


def test_equality():
    node_1 = Node("node 1")
    node_2 = Node("node 2")

    # Reference comparaison
    assert node_1 != node_2

    # Same name doesn't mean same node
    node_3 = Node("node 1")
    assert node_1 != node_3


def test_node_uuid_is_unique():
    node_1 = Node("node_1", None)
    node_2 = Node("node_2", None)

    assert node_1.uid != node_2.uid

    node_1_bis = Node("node_1", None)

    assert node_1.uid != node_1_bis.uid

    node_3 = Node("node 3", "node_3")
    node_3_bis = Node("node 3", "node_3")

    # Creating a node with an existing ID should return the existing reference
    assert node_3 == node_3_bis