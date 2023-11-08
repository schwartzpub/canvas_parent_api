"""Course Model Definition."""
from canvas_parent_api.base import DataModel
from canvas_parent_api.canvas_api_client import CourseResponse


class Course(DataModel):
    """Define Course Model."""
    def __init__(self, course_resp: CourseResponse):
        self._id = course_resp.id
        self._name = course_resp.name
        self._score = course_resp.enrollments[0]['computed_current_score']
        self._grade = self._compute_letter_grade()
        self._course_code = course_resp.course_code
        self._enrollment_term_id = course_resp.enrollment_term_id
        self._grading_standard_id = course_resp.grading_standard_id
        self._created_at = course_resp.term['created_at']
        self._start_at = course_resp.term['start_at']
        self._end_at = course_resp.term['end_at']
        self._enrollments = course_resp.enrollments
        self._calendar = course_resp.calendar
        self._term = course_resp.term
        self._course_progress = course_resp.course_progress
        self._public_syllabus = course_resp.public_syllabus
        self._time_zone = course_resp.time_zone

    @property
    def id(self) -> int:
        """Property Definition."""
        return self._id

    @property
    def name(self) -> str:
        """Property Definition."""
        return self._name

    @property
    def score(self) -> str:
        """Property Definition."""
        return self._score

    @property
    def grade(self) -> str:
        """Property Definition."""
        return self._grade

    @property
    def course_code(self) -> str:
        """Property Definition."""
        return self._course_code

    @property
    def enrollment_term_id(self) -> int:
        """Property Definition."""
        return self._enrollment_term_id

    @property
    def grading_standard_id(self) -> int:
        """Property Definition."""
        return self._grading_standard_id

    @property
    def created_at(self) -> str:
        """Property Definition."""
        return self._created_at

    @property
    def start_at(self) -> str:
        """Property Definition."""
        return self._start_at

    @property
    def end_at(self) -> str:
        """Property Definition."""
        return self._end_at

    @property
    def enrollments(self) -> list:
        """Property Definition."""
        return self._enrollments

    @property
    def calendar(self) -> dict:
        """Property Definition."""
        return self._calendar

    @property
    def term(self) -> dict:
        """Property Definition."""
        return self._term

    @property
    def course_progress(self):
        """Property Definition"""
        return self._course_progress

    @property
    def public_syllabus(self) -> bool:
        """Property Definition."""
        return self._public_syllabus

    @property
    def time_zone(self) -> str:
        """Property Definition."""
        return self._time_zone

    def _compute_letter_grade(self) -> str:
        grades = {
            93: 'A+', 97: 'A', 90: 'A-',
            87: 'B+', 83: 'B', 80: 'B-',
            77: 'C+', 73: 'C', 70: 'C-',
            67: 'D+', 63: 'D', 60: 'D-'
        }
        for score, letter in grades.items():
            if self.score >= score:
                return letter
        return 'F'
