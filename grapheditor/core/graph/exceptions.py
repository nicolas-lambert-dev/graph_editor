from grapheditor.core.graph.graph_object import IGraphObject


class DagException(Exception):
    """
    All graph exception should inherit from this class.

    """
    def __int__(self, msg: str):
        super().__init__(msg)


class ConnectionException(DagException):
    message: str = ""

    def __int__(self, source: IGraphObject, target: IGraphObject):
        super().__init__(f"Trying to connect {source} --> {target} failed. Reason: {self.message}")


class DependencyCycleException(ConnectionException):

    message = "This connection create a dependency cycle"