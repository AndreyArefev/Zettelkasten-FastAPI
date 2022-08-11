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
    response_model=List[models.Idea],
)
def get_ideas(
    user: models.User = Depends(get_current_user),
    ideas_service: IdeasService = Depends(),
):
    return ideas_service.get_many(user.id)



@router.post(
    '/',
    response_model=models.Idea,
    status_code=status.HTTP_201_CREATED,
)
def create_idea(
    idea_data: models.IdeaCreate,
    user: models.User = Depends(get_current_user),
    ideas_service: IdeasService = Depends(),
):
    return ideas_service.create_idea(
        user.id,
        idea_data,
    )


@router.get(
    '/{idea_id}',
    response_model=models.Idea,
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
    '/tags/{tag_name}',
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
    '/search_word/{word}',
    response_model=List[models.Idea],
)
def get_by_word(
        word: str,
        user: models.User = Depends(get_current_user),
        ideas_service: IdeasService = Depends(),
):
    return ideas_service.get_by_word(
        user.id,
        word,
    )

@router.get(
    '/search_name/{name}',
    response_model=models.Idea,
)
def get_by_name(
        name: str,
        user: models.User = Depends(get_current_user),
        ideas_service: IdeasService = Depends(),
):
    return ideas_service.get_by_name(
        user.id,
        name,
    )

@router.put(
    '/{idea_id}',
    response_model=models.IdeaUpdate,
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