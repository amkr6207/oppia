# coding: utf-8
#
# Copyright 2025 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Domain models for learner assessment attempts and responses."""

from __future__ import annotations

import datetime

from core import utils
from core.domain import question_domain

from typing import Optional, TypedDict


class AssessmentAttemptDict(TypedDict):
    """Dict representation of an assessment attempt."""

    id: str
    user_id: str
    offering_id: str
    offering_version: int
    start_time: float
    end_time: Optional[float]
    score_percentage: Optional[float]
    passed: Optional[bool]
    offering_name: Optional[str]


class AssessmentAttempt:
    """Domain object for a certificate assessment attempt."""

    def __init__(
        self,
        attempt_id: str,
        user_id: str,
        offering_id: str,
        offering_version: int,
        start_time: datetime.datetime,
        end_time: Optional[datetime.datetime] = None,
        passed: Optional[bool] = None,
        score_percentage: Optional[float] = None,
        offering_name: Optional[str] = None,
    ) -> None:
        self.id = attempt_id
        self.user_id = user_id
        self.offering_id = offering_id
        self.offering_version = offering_version
        self.start_time = start_time
        self.end_time = end_time
        self.passed = passed
        self.score_percentage = score_percentage
        self.offering_name = offering_name

    def validate(self) -> None:
        """Validates the properties of the attempt."""
        if not isinstance(self.id, str):
            raise utils.ValidationError('ID must be a string')
        if not isinstance(self.user_id, str):
            raise utils.ValidationError('User ID must be a string')
        if not isinstance(self.offering_id, str):
            raise utils.ValidationError('Offering ID must be a string')
        if not isinstance(self.offering_version, int):
            raise utils.ValidationError('Offering version must be an integer')
        if not isinstance(self.start_time, datetime.datetime):
            raise utils.ValidationError('Start time must be a datetime')
        if self.end_time is not None and not isinstance(
            self.end_time, datetime.datetime
        ):
            raise utils.ValidationError('End time must be a datetime')
        if self.end_time is not None and self.end_time < self.start_time:
            raise utils.ValidationError('End time cannot be before start time')
        if self.passed is not None and not isinstance(self.passed, bool):
            raise utils.ValidationError('Passed must be a boolean')
        if self.score_percentage is not None:
            if not isinstance(self.score_percentage, (float, int)):
                raise utils.ValidationError('Score percentage must be a float')
            if self.score_percentage < 0 or self.score_percentage > 100:
                raise utils.ValidationError(
                    'Score percentage must be between 0 and 100'
                )

    def to_dict(self) -> AssessmentAttemptDict:
        """Returns a dict representation of the attempt."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'offering_id': self.offering_id,
            'offering_version': self.offering_version,
            'start_time': utils.get_time_in_millisecs(self.start_time),
            'end_time': (
                utils.get_time_in_millisecs(self.end_time)
                if self.end_time
                else None
            ),
            'passed': self.passed,
            'score_percentage': self.score_percentage,
            'offering_name': self.offering_name,
        }


class QuestionWithMetadataDict(question_domain.QuestionDict):
    """Dict representation of a question with skill metadata."""

    skill_id: str
    skill_difficulty: float


class AssessmentResponseDict(TypedDict):
    """Dict representation of an assessment response."""

    id: str
    attempt_id: str
    user_id: str
    question_id: str
    question_version: int
    skill_id: str
    skill_version: int
    learner_answer_html: Optional[str]
    is_correct: bool


class AssessmentQuestionResponse:
    """Domain object for a response to an assessment question."""

    def __init__(
        self,
        response_id: str,
        attempt_id: str,
        user_id: str,
        question_id: str,
        question_version: int,
        skill_id: str,
        skill_version: int,
        learner_answer_html: Optional[str],
        is_correct: bool,
    ) -> None:
        self.id = response_id
        self.attempt_id = attempt_id
        self.user_id = user_id
        self.question_id = question_id
        self.question_version = question_version
        self.skill_id = skill_id
        self.skill_version = skill_version
        self.learner_answer_html = learner_answer_html
        self.is_correct = is_correct

    def validate(self) -> None:
        """Validates the properties of the response."""
        if not isinstance(self.id, str):
            raise utils.ValidationError('Response ID must be a string')
        if not isinstance(self.attempt_id, str):
            raise utils.ValidationError('Attempt ID must be a string')
        if not isinstance(self.user_id, str):
            raise utils.ValidationError('User ID must be a string')
        if not isinstance(self.question_id, str):
            raise utils.ValidationError('Question ID must be a string')
        if not isinstance(self.question_version, int):
            raise utils.ValidationError('Question version must be an integer')
        if not isinstance(self.skill_id, str):
            raise utils.ValidationError('Skill ID must be a string')
        if not isinstance(self.skill_version, int):
            raise utils.ValidationError('Skill version must be an integer')
        if self.learner_answer_html is not None and not isinstance(
            self.learner_answer_html, str
        ):
            raise utils.ValidationError('Learner answer must be a string')
        if not isinstance(self.is_correct, bool):
            raise utils.ValidationError('is_correct must be a boolean')

    def to_dict(self) -> AssessmentResponseDict:
        """Returns a dict representation of the response."""
        return {
            'id': self.id,
            'attempt_id': self.attempt_id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'question_version': self.question_version,
            'skill_id': self.skill_id,
            'skill_version': self.skill_version,
            'learner_answer_html': self.learner_answer_html,
            'is_correct': self.is_correct,
        }
