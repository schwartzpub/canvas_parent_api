import logging

from .canvas_api_client import CanvasApiClient, CourseResponse,ObserverResponse

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
        
        def observees(self) -> list[ObserverResponse]:
            my_observees = self._api_client.get_observees()
            observees = [ObserverResponse(response) for response in my_observees]
            return observees