Feature: Dag
  This is a directed acyclic graph (dag)
  As a user, I want to manage nodes and edges using the common features a directed acyclic graph can leverage

  Scenario: Adding nodes to the Dag
    Given the dag have 0 nodes
    When 3 nodes are added to the dag
    Then the dag contains 3 nodes

  Scenario: Adding an existing node should be forbidden
    Given the dag contains node_1,node_2,node_3
    Then the dag contains 3 nodes
    When node_2 is added
    Then the dag contains 3 nodes

  Scenario: Removing an existing node
    Given the dag contains node_1,node_2,node_3
    When removing node_2
    Then the dag contains 2 nodes
    
  Scenario: Removing an non existing node should not change the Dag
    Given the dag contains node_1,node_2,node_3
    Then removing node_4 should raise an Exception

