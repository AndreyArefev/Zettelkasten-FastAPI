from typing import List

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from .. import models
from ..services.auth import get_current_user
from ..services.ideas import IdeasService


router = APIRouter(
    prefix='/ideas',
    tags=['ideas'],
)

@router.get(
    '/',
    response_model=List[models.IdeaSchema],
)
def get_ideas(
    user: models.User = Depends(get_current_user),
    ideas_service: IdeasService = Depends(),
):
    return ideas_service.get_many(user.id)

@router.post(
    '/',
    response_model=List[models.IdeaSchema],
    status_code=status.HTTP_201_CREATED,
)
def create_idea(
    idea_data: models.IdeaCreate,
    user: models.User = Depends(get_current_user),
    ideas_service: IdeasService = Depends(),
):
    return ideas_service.create(
        user.id,
        idea_data,
    )


@router.get(
    '/{idea_id}',
    response_model=models.IdeaSchema,
)
def get_idea(
    idea_id: int,
    user: models.User = Depends(get_current_user),
    ideas_service: IdeasService = Depends(),
):
    return ideas_service.get(
        user.id,
        idea_id,
    )

@router.get(
    '/{tag_name}',
    response_model=models.TagSchema,
)
def get_by_tag(
    tag_name: str,
    user: models.User = Depends(get_current_user),
    ideas_service: IdeasService = Depends(),
):
    return ideas_service.get_by_tag(
        user.id,
        tag_name,
    )

@router.get(
    '/{word}',
    response_model=models.IdeaSchema,
)
def get_by_word(
        word: str,
        user: models.User = Depends(get_current_user),
        ideas_service: IdeasService = Depends(),
):
    return ideas_service.get_by_tag(
        user.id,
        word,
    )


@router.put(
    '/{idea_id}',
    response_model=models.IdeaSchema,
)
def update_idea(
    idea_id: int,
    idea_data: models.IdeaUpdate,
    user: models.User = Depends(get_current_user),
    ideas_service: IdeasService = Depends(),
):
    return ideas_service.update(
        user.id,
        idea_id,
        idea_data,
    )


@router.delete(
    '/{idea_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_idea(
    idea_id: int,
    user: models.User = Depends(get_current_user),
    ideas_service: IdeasService = Depends(),
):
    ideas_service.delete(
        user.id,
        idea_id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)