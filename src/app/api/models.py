from pydantic import BaseModel
from dataclasses import dataclass


class MindMapRequestBody(BaseModel):
    """
    Representation of MindMap request body for mind map creation
    """
    id: str


class MindMapEntry(MindMapRequestBody):
    """
    Representation of row in the MindMap table
    """
    uuid: int
    leaf: str = None
    leaf_message: str = None


class MindMapLeafRequestBody(BaseModel):
    """
    Representation of MindMap leaf request body for leaf creation
    """
    path: str
    text: str


@dataclass
class MindMap:
    """
    Representation of MindMap object, with array of leaf
    """
    map_id: str
    leafs: [MindMapEntry]

    def pretty(self):
        """
        Using the array of leaf, returns a beautiful string representation of the mindmap tree
        Returns:
            (str) string containing the tree representation
        """
        def _format_tree(tree: dict, ident: int = 0, message: str = "") -> str:
            for k, v in tree.items():
                if k == CONST_END_KEY and v == []:
                    ident += 1
                    continue
                elif k and isinstance(v, dict):
                    message = message + "\n" + "\t" * ident + f"{k}/"
                    message = _format_tree(v, ident, message)
                elif k == CONST_END_KEY and isinstance(v, list):
                    ident += 1
                    for end_key in v:
                        message = message + "\n" + "\t" * ident + f"{end_key}"
            return message

        def _attach(branch: str, tree: dict) -> dict:
            parts = branch.split('/', 1)  # [head_of_path, rest_of_path (if exists)]
            if len(parts) == 1:  # last elem in path
                if parts[0] != "":
                    tree[CONST_END_KEY].append(parts[0])
            else:
                node, others = parts
                if node not in tree:
                    tree[node] = {CONST_END_KEY: []}
                _attach(others, tree[node])
            return tree

        CONST_END_KEY = "END_KEY"
        tree = {CONST_END_KEY: []}
        for elem in self.leafs:
            if elem.leaf:
                tree = _attach(elem.leaf, tree)

        # add root/ because it is not present in the leaf_path but expected in the output
        return "root/" + _format_tree(tree)
