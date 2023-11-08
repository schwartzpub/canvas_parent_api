"""Submission Model Definition."""
from canvas_parent_api.base import DataModel
from canvas_parent_api.canvas_api_client import SubmissionResponse


class Submission(DataModel):
    """Define Course Model."""
    def __init__(self, submission_resp: SubmissionResponse):
        self._assignment_id = submission_resp.assignment_id
        self._attempt = submission_resp.attempt
        self._body = submission_resp.body
        self._grade = submission_resp.grade
        self._grade_matches_current_submission = submission_resp.grade_matches_current_submission
        self._score = submission_resp.score
        self._submitted_at = submission_resp.submitted_at
        self._late = submission_resp.late
        self._excused = submission_resp.excused
        self._missing = submission_resp.missing
        self._late_policy_status = submission_resp.late_policy_status
        self._points_deducted = submission_resp.points_deducted
        self._workflow_state = submission_resp.workflow_state
        self._seconds_late = submission_resp.seconds_late
        self._preview_url = submission_resp.preview_url

    @property
    def assignment_id(self) -> int:
        """Property Definition."""
        return self._assignment_id

    @property
    def attempt(self) -> int:
        """Property Definition."""
        return self._attempt

    @property
    def body(self) -> str:
        """Property Definition."""
        return self._body

    @property
    def grade(self) -> str:
        """Property Definition."""
        return self._grade

    @property
    def grade_matches_current_submission(self) -> bool:
        """Property Definition."""
        return self._grade_matches_current_submission

    @property
    def score(self) -> float:
        """Property Definition."""
        return self._score

    @property
    def submitted_at(self) -> str:
        """Property Definition."""
        return self._submitted_at

    @property
    def late(self) -> bool:
        """Property Definition."""
        return self._late

    @property
    def excused(self) -> bool:
        """Property Definition."""
        return self._excused

    @property
    def missing(self) -> bool:
        """Property Definition."""
        return self._missing

    @property
    def late_policy_status(self) -> str:
        """Property Definition."""
        return self._late_policy_status

    @property
    def points_deducted(self) -> float:
        """Property Definition."""
        return self._points_deducted

    @property
    def workflow_state(self) -> str:
        """Property Definition."""
        return self._workflow_state

    @property
    def seconds_late(self) -> int:
        """Property Definition"""
        return self._seconds_late

    @property
    def preview_url(self) -> str:
        """Property Definition"""
        return self._preview_url
