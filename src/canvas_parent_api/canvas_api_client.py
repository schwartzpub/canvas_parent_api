import json
import logging
from turtle import st
import aiohttp

from urllib.parse import urljoin
from typing import List,Optional
from pydantic import BaseModel, Extra, Field, root_validator, validator

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)

def _enable_debug_logging():
    _LOGGER.setLevel(logging.DEBUG)

class ObserveeResponse(BaseModel):
    id: int
    name: str
    created_at: str
    sortable_name: str
    short_name: str
    observation_link_root_account: Optional[list[int]] = None

class CourseResponse(BaseModel):
    id: int
    sis_course_id: Optional[int]
    uuid: str
    integration_id: Optional[int]
    sis_import_id: Optional[int]
    name: str
    course_code: str
    original_name: str
    workflow_state: str
    account_id: int
    root_account_id: int
    enrollment_term_id: int
    grading_periods: Optional[list]
    grading_standard_id: int
    grade_passback_setting: str
    created_at: str
    start_at: str
    end_at: str
    locale: str
    enrollments: Optional[list]
    total_students: Optional[int]
    calendar: str
    default_view: str
    syllabus_body: Optional[str]
    needs_grading_count: Optional[int]
    term: Optional[int]
    course_progress: Optional[int]
    apply_assignment_group_weights: bool
    permissions: Optional[dict]
    is_public: bool
    is_public_to_auth_users: bool
    public_syllabus: bool
    public_syllabus_to_auth: bool
    public_description: Optional[str]
    storage_quota_mb: int
    storage_quota_used_mb: int
    hide_final_grades: bool
    license: str
    allow_student_assignment_edits: bool
    allow_wiki_comments: bool
    allow_student_forum_attachments: bool
    open_enrollment: bool
    self_enrollment: bool
    restrict_enrollments_to_course_dates: bool
    course_format: str
    access_restricted_by_date: Optional[bool]
    time_zone: str
    blueprint: Optional[bool]
    blueprint_restrictions: Optional[dict]
    blueprint_restrictions_by_object_type: Optional[dict]
    template: bool

class CanvasApiClient(object):
    """Canvas Parent API Client."""
    def __init__(
        self,
        base_url,
        api_key,
        path: str = None,
        debug = False,
    ):
        if debug:
            _enable_debug_logging()

        if path:
            self._base_url = "{}/api/v1/users/{}".format(base_url,path)
        else:
            self._base_url = "{}/api/v1/".format(base_url)

        _LOGGER.debug(f"generated base url: {self._base_url}")

        self._api_key = api_key
        self._headers = {"accept": "application/json","Authorization": f"Bearer {self._api_key}"}

        async def _get_request(self, end_url: str, query_filters: list[str] = None):
            request_url = urljoin(self._base_url,end_url)
            params = None
            async with aiohttp.ClientSession() as session:
                async with session.get("{}".format(request_url), headers=self._headers) as studentresp:
                    response = await studentresp.json()
                    if response.status_code >= 400:
                        return response                   
                    return response

        def get_observees(self) -> list[ObserveeResponse]:
            """Get Canvas Observees (students)."""
            parsed_response = self._get_request("self/observees")
            if parsed_response:
                return [ObserveeResponse(**response) for response in parsed_response]
            return []

        def get_courses(self, student_id: int) -> list[CourseResponse]:
            """Get Canvas Courses."""
            parsed_response = self._get_request(f"{student_id}/courses?include[]=term")
            if parsed_response:
                return [CourseResponse(**response) for response in parsed_response]
            return []