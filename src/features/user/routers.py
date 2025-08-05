import logging
from fastapi import APIRouter

router = APIRouter(tags=["user"])
logger = logging.getLogger(__name__)
