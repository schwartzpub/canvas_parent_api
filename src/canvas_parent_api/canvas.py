import logging

from .models.Observee import Observee
from .models.Course import Course
from .canvas_api_client import CanvasApiClient, ObserveeResponse, CourseResponse

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)

class Canvas(object):
    def __init__(
        self,
        base_url,
        api_key,
        path: str = None,
        debug = False,
    ):
        self._api_client = CanvasApiClient(base_url,api_key,path,debug)

        if debug:
            _LOGGER.setLevel(logging.DEBUG)
        
    async def observees(self) -> list[Observee]:
        my_observees = await self._api_client.get_observees()
        observees = [Observee(response) for response in my_observees]
        return observees