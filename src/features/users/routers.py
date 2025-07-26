import logging
from fastapi import APIRouter

router = APIRouter(tags=["users"])
logger = logging.getLogger(__name__)
