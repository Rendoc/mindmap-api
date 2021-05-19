from fastapi import APIRouter, Response, HTTPException

from .models import MindMapRequestBody, MindMapLeafRequestBody
from . import db_operations

router = APIRouter()


@router.post("/map", status_code=201)
async def create_map(body: MindMapRequestBody):
    """
    Create map
    Args:
        body (MindMapRequestBody): Map object to create
    """
    await db_operations.post_map(body)
    response_object = {
        "map_id": body.id
    }
    return response_object


@router.post("/map/{id}", status_code=201)
async def create_leaf(id: str, body: MindMapLeafRequestBody):
    """
    Create leaf
    Args:
        id (str): id of the map
        body (MindMapLeafRequestBody): Leaf object with the leaf path and leaf message
    """
    await db_operations.post_leaf(map_id=id, body=body)
    response_object = {
        "map_id": id,
        "leaf": body.path,
        "leaf_message": body.text
    }
    return response_object


@router.put("/map/{id}", status_code=200)
async def update_leaf(id: str, body: MindMapLeafRequestBody):
    """
    Update text of leaf
    Args:
        id (str): id of the map
        body (MindMapLeafRequestBody): Leaf object with the leaf path and the new leaf message
    """
    leaf = await db_operations.get_leaf(map_id=id, leaf_path=body.path)
    if leaf:
        await db_operations.put_leaf(map_id=id, body=body)
        response_object = {
            "map_id": id,
            "leaf": body.path,
            "leaf_message": body.text
        }
        return response_object
    else:
        raise HTTPException(status_code=404, detail="Leaf not found")


@router.get("/map/{id}", status_code=200)
async def get_map_content(id: str, path: str = None, pretty: bool = True):
    """
    Get content of a map, the whole map or a leaf
    Args:
        id (str): id of the map
        path (Optional[str]): path of the leaf
        pretty (Optional[bool]: pretty the map response

    Returns:
        (response_object) or (str) of the map content
    """
    if path:
        text = await db_operations.get_leaf(map_id=id, leaf_path=path)
        if text:
            response_object = {
                "map_id": id,
                "path": path,
                "text": text.get("leaf_message")
            }
            return response_object
        else:
            raise HTTPException(status_code=404, detail="Leaf not found")

    mind_map = await db_operations.get_map(map_id=id)
    if mind_map:
        if pretty:
            return Response(content=mind_map.pretty(), media_type="text/plain")
        else:
            response_object = {
                "map_id": id,
                "map_content": mind_map
            }
            return response_object
    else:
        raise HTTPException(status_code=404, detail="Mind map not found")


@router.delete("/map/{id}", status_code=200)
async def delete_map_content(id: str, path: str = None):
    """
    Delete map content, the whole map if no leaf path is supplied

    Args:
        id (str): id of the map
        path (Optional[str]): path of the leaf
    """
    if path:
        await db_operations.delete_leaf(map_id=id, leaf_path=path)
        response_object = {
            "map_id": id,
            "path": path,
            "status": "deleted"
        }
        return response_object

    await db_operations.delete_map(map_id=id)
    response_object = {
        "map_id": id,
        "status": "deleted"
    }
    return response_object
