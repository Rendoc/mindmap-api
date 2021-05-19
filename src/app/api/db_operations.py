from sqlalchemy import and_

from .models import MindMapRequestBody, MindMapEntry, MindMapLeafRequestBody, MindMap
from ..database import mindmap, database


async def post_map(body: MindMapRequestBody) -> int:
    """
    Database operation insert map
    Args:
        body (MindMapRequestBody): Content of the map to insert

    Returns:
        (int) uuid of the newly added row
    """
    query = mindmap.insert().values(id=body.id)
    return await database.execute(query=query)


async def post_leaf(map_id: str, body: MindMapLeafRequestBody):
    """
    Database operation insert map, with leaf data
    Args:
        map_id (str): in which map to add leaf
        body (MindMapRequestBody): Content of the map to insert

    Returns:
        (int) uuid of the newly added row
    """
    query = mindmap.insert().values(id=map_id, leaf=body.path, leaf_message=body.text)
    return await database.execute(query=query)


async def put_leaf(map_id: str, body: MindMapLeafRequestBody):
    """
    Database operation update leaf text from map with leaf_path
    Args:
        map_id (str): in which map to add leaf
        body (MindMapRequestBody): Content of the map to insert
    """
    query = (mindmap
             .update()
             .where(and_(mindmap.c.id == map_id, mindmap.c.leaf == body.path))
             .values(leaf_message=body.text)
             )
    await database.execute(query=query)


async def get_map(map_id: str) -> MindMap:
    """
    Database operation get all content of map
    Args:
        map_id (str): which map to retrieve content
    Returns:
        (MindMap) MindMap object with all the leafs
    """
    query = (mindmap
             .select()
             .where(mindmap.c.id == map_id)
             )
    result = await database.fetch_all(query=query)
    if result:
        mind_map = MindMap(map_id=map_id, leafs=[MindMapEntry(**row) for row in result])
        return mind_map
    else:
        return None


async def get_leaf(map_id: str, leaf_path: str) -> str:
    """
    Database operation get leaf text from leaf path
    Args:
        map_id (str): which map to retrieve content
        leaf_path (str): path of the leaf

    Returns:
        (str) leaf text
    """
    query = (mindmap
             .select()
             .where(and_(mindmap.c.id == map_id, mindmap.c.leaf == leaf_path))
             )
    return await database.fetch_one(query=query)


async def delete_leaf(map_id: str, leaf_path: str):
    """
    Database operation delete leaf from map by leaf path
    Args:
        map_id (str): which map to delete from
        leaf_path (str): path of the leaf
    """
    query = (mindmap
             .delete()
             .where(and_(mindmap.c.id == map_id, mindmap.c.leaf == leaf_path))
             )
    await database.execute(query=query)


async def delete_map(map_id: str):
    """
    Database operation delete map
    Args:
        map_id (str): which map to delete
    """
    query = (mindmap
             .delete()
             .where(mindmap.c.id == map_id)
             )
    await database.execute(query=query)
