from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.models import Module


router = APIRouter()



@router.post("/modules")
async def create_module(
    data: dict,
    db: Session = Depends(get_db)
):


    name = data.get("name")
    url = data.get("url")


    if not name or not url:

        raise HTTPException(
            status_code=400,
            detail="name and url are required"
        )



    existing = (
        db.query(Module)
        .filter(
            Module.name == name
        )
        .first()
    )



    if existing:

        raise HTTPException(
            status_code=400,
            detail="Module already exists"
        )



    module = Module(

        name=name,

        url=url,

        description=data.get(
            "description"
        ),

        active=data.get(
            "active",
            True
        ),

        priority=data.get(
            "priority",
            100
        ),

        timeout=data.get(
            "timeout",
            30
        )

    )



    db.add(module)

    db.commit()

    db.refresh(module)



    return {

        "success": True,

        "module": {

            "id": module.id,

            "name": module.name,

            "url": module.url,

            "description": module.description,

            "active": module.active,

            "priority": module.priority,

            "timeout": module.timeout

        }

    }





@router.get("/modules")
async def get_modules(
    db: Session = Depends(get_db)
):


    modules = (
        db.query(Module)
        .order_by(
            Module.priority.asc()
        )
        .all()
    )



    return {

        "success": True,

        "modules": [

            {

                "id": module.id,

                "name": module.name,

                "url": module.url,

                "description": module.description,

                "active": module.active,

                "priority": module.priority,

                "timeout": module.timeout,

                "created_at": module.created_at,

                "updated_at": module.updated_at

            }

            for module in modules

        ]

    }





@router.get("/modules/{module_id}")
async def get_module(
    module_id: int,
    db: Session = Depends(get_db)
):


    module = (
        db.query(Module)
        .filter(
            Module.id == module_id
        )
        .first()
    )



    if not module:

        raise HTTPException(
            status_code=404,
            detail="Module not found"
        )



    return {

        "success": True,

        "module": {

            "id": module.id,

            "name": module.name,

            "url": module.url,

            "description": module.description,

            "active": module.active,

            "priority": module.priority,

            "timeout": module.timeout,

            "created_at": module.created_at,

            "updated_at": module.updated_at

        }

    }





@router.put("/modules/{module_id}")
async def update_module(
    module_id: int,
    data: dict,
    db: Session = Depends(get_db)
):


    module = (
        db.query(Module)
        .filter(
            Module.id == module_id
        )
        .first()
    )



    if not module:

        raise HTTPException(
            status_code=404,
            detail="Module not found"
        )



    module.name = data.get(
        "name",
        module.name
    )

    module.url = data.get(
        "url",
        module.url
    )

    module.description = data.get(
        "description",
        module.description
    )

    module.active = data.get(
        "active",
        module.active
    )

    module.priority = data.get(
        "priority",
        module.priority
    )

    module.timeout = data.get(
        "timeout",
        module.timeout
    )



    db.commit()

    db.refresh(module)



    return {

        "success": True,

        "module": {

            "id": module.id,

            "name": module.name,

            "url": module.url,

            "description": module.description,

            "active": module.active,

            "priority": module.priority,

            "timeout": module.timeout

        }

    }





@router.patch("/modules/{module_id}/activate")
async def activate_module(
    module_id: int,
    data: dict,
    db: Session = Depends(get_db)
):


    module = (
        db.query(Module)
        .filter(
            Module.id == module_id
        )
        .first()
    )



    if not module:

        raise HTTPException(
            status_code=404,
            detail="Module not found"
        )



    module.active = data.get(
        "active",
        True
    )



    db.commit()

    db.refresh(module)



    return {

        "success": True,

        "module": {

            "id": module.id,

            "name": module.name,

            "active": module.active

        }

    }





@router.delete("/modules/{module_id}")
async def delete_module(
    module_id: int,
    db: Session = Depends(get_db)
):


    module = (
        db.query(Module)
        .filter(
            Module.id == module_id
        )
        .first()
    )



    if not module:

        raise HTTPException(
            status_code=404,
            detail="Module not found"
        )



    db.delete(module)

    db.commit()



    return {

        "success": True,

        "message": "Module deleted"

    }