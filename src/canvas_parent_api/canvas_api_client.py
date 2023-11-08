"""Canvas API Client."""
import json
import logging

from urllib.parse import urljoin

import aiohttp
from multidict import MultiDict

from canvas_parent_api.errors.canvas_error import CanvasError

from .models.base import ObserveeResponse, CourseResponse, AssignmentResponse, SubmissionResponse

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)


def _enable_debug_logging():
    _LOGGER.setLevel(logging.DEBUG)


class CanvasApiClient():
    """Canvas Parent API Client."""
    def __init__(
        self,
        base_url,
        api_key,
        path: str = None,
        debug=False,
    ):
        if debug:
            _enable_debug_logging()

        if path:
            self._base_url = f"{base_url}/api/v1/users/{path}"
        else:
            self._base_url = f"{base_url}/api/v1/"

        _LOGGER.debug(f"generated base url: {self._base_url}")

        self._api_key = api_key
        self._headers = {"accept": "application/json", "Authorization": f"Bearer {self._api_key}"}

    async def _get_request(self, end_url: str):
        """Perform GET request to API endpoint."""
        request_url = urljoin(self._base_url, end_url)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{request_url}", headers=self._headers) as resp:
                response = resp
                responsetext = await resp.text()
                if response.status >= 400:
                    raise CanvasError(response.status, responsetext)
                return response

    def sanitize_observee_data(self, json_data):
        return [ObserveeResponse(**resp) for resp in json_data]

    def sanitize_courses_data(self, json_data):
        sanitized_data = []
        for course in json_data:
            if 'name' not in course.keys():
                continue
            if 'error' in course['course_progress'].keys():
                course['course_progress'] = {
                    'requirement_count': None,
                    'requirement_completed_count': None,
                    'next_requirement_url': None,
                    'completed_at': None
                }
            sanitized_data.append(course)
        return [CourseResponse(**resp) for resp in sanitized_data]

    def sanitize_assignments_data(self, json_data):
        return [AssignmentResponse(**resp) for resp in json_data]

    def sanitize_submissions_data(self, json_data):
        return [SubmissionResponse(**resp) for resp in json_data]

    async def get_response_data(self, endpoint, response_type):
        response = await self._get_request(endpoint)
        parsed_json = await response.json()
        next = MultiDict(response.links.get('next', ''))
        if next:
            nextpage = await self._get_request(str(next.get('url')).replace(self._base_url, ''))
            parsed_json.extend(await nextpage.json())
        if response:
            if response_type == 'observees':
                return self.sanitize_observee_data(parsed_json)
            if response_type == 'courses':
                return self.sanitize_courses_data(parsed_json)
            if response_type == 'assignments':
                return self.sanitize_assignments_data(parsed_json)
            if response_type == 'submissions':
                return self.sanitize_submissions_data(parsed_json)
        return []

    async def get_observees(self) -> list[ObserveeResponse]:
        """Get Canvas Observees (students)."""
        endpoint = "users/self/observees"
        return await self.get_response_data(endpoint, 'observees')

    async def get_courses(self, student_id: int) -> list[CourseResponse]:
        """Get Canvas Courses."""
        endpoint = (f"users/{student_id}/courses"
                    f"?include[]=term"
                    f"&include[]=current_grading_period_scores"
                    f"&include[]=total_scores"
                    f"&include[]=syllabus_body"
                    f"&include[]=public_description"
                    f"&include[]=grading_periods"
                    f"&include[]=course_progress"
                    f"&include[]=concluded"
                    f"&include[]=needs_grading_count"
                    f"&per_page=50")
        return await self.get_response_data(endpoint, 'courses')

    async def get_assignments(self, student_id: int, course_id: int) -> list[AssignmentResponse]:
        """Get Canvas Courses."""
        endpoint = (f"users/{student_id}/courses/{course_id}/assignments"
                    f"?include[]=submission"
                    f"&include[]=observed_users"
                    f"&per_page=50")
        return await self.get_response_data(endpoint, 'assignments')

    async def get_submissions(self, student_id: int, course_id: int) -> list[SubmissionResponse]:
        """Get Canvas Courses."""
        endpoint = f"courses/{course_id}/students/submissions?student_ids[]={student_id}&per_page=50"
        return await self.get_response_data(endpoint, 'submissions')
