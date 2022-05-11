import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from grapheditor.core.graph.graph import IGraph
from grapheditor.core.graph.node import INode, Node

scenarios("../features/dag.feature")


def str_to_node(arg: str, graph: IGraph) -> INode:
    return Node(uid=arg, data=arg, graph=graph)


@given(parsers.parse("the dag have {nb_nodes:d} nodes"), target_fixture="graph")
def create_graph(nb_nodes: int = 0) -> IGraph:
    from grapheditor.core.graph.dag import DirectedAcyclicGraph
    dag = DirectedAcyclicGraph()
    for i in range(0, nb_nodes):
        dag.add_node(str_to_node(f"node_{i}", dag))
    return dag


@given("the dag contains node_1,node_2,node_3", target_fixture="graph")
def graph_with_node_1_2_3():
    graph = create_graph(0)
    graph.add_node(str_to_node("node_1", graph))
    graph.add_node(str_to_node("node_2", graph))
    graph.add_node(str_to_node("node_3", graph))
    return graph


@when(parsers.parse("{nb_nodes:d} nodes are added to the dag"))
def add_node_to_dag(graph, nb_nodes):
    for i in range(0, nb_nodes):
        graph.add_node(str_to_node(f"node_{i}", graph))


@then(parsers.parse("the dag contains {total_nodes:d} nodes"))
def dag_contains_the_good_number_of_nodes(graph, total_nodes):
    assert len(graph.nodes) == total_nodes


@when(parsers.parse("{node_id} is added"))
def when_add_specific_node(graph, node_id):
    graph.add_node(str_to_node(node_id, graph))


@when(parsers.parse("removing {node}"))
def dag_remove_node(graph, node):
    graph.remove_node(str_to_node(node, graph).uid)


@then(parsers.parse("removing {node} should raise an Exception"))
def dag_remove_node(graph, node):
    with pytest.raises(Exception):
        graph.remove_node(node)


@given("a subscriber print on change")
def add_node_listener_to_dag(graph: IGraph, mocker):
    mocker.patch('builtins.print')
    graph.nodes.subscribe(lambda event: print(event))


@then("the terminal should print")
def listener_should_print(mocker):
    assert print.assert_called_once()
