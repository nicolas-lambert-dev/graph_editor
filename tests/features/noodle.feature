Feature: Noodle
  Noodle is in charge of sorting the execution of connected nodes, taking care of they dependencies

  Scenario: Some nodes are connected together and we want to execute them in the right dependency order
    Given a noodle instance
    And is having a current graph node_1->node_2->node_3->result
    When we execute node_2 it should execute node_2->node3->result