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

"""Models for storing the certificate assessment attempts and responses."""

from __future__ import annotations

import datetime

from core import utils
from core.platform import models

from typing import Dict, List, Optional, cast

MYPY = False
if MYPY:  # pragma: no cover
    from mypy_imports import base_models, datastore_services

(base_models,) = models.Registry.import_models([models.Names.BASE_MODEL])

datastore_services = models.Registry.import_datastore_services()


class AssessmentAttemptModel(base_models.BaseModel):
    """Model to store a learner's attempt at a certificate assessment."""

    # The user ID of the learner.
    user_id = datastore_services.StringProperty(required=True, indexed=True)
    # The ID of the certificate offering attempted.
    offering_id = datastore_services.StringProperty(required=True, indexed=True)
    # The version of the certificate offering attempted.
    offering_version = datastore_services.IntegerProperty(
        required=True, indexed=True
    )
    # Time when the attempt started.
    start_time = datastore_services.DateTimeProperty(
        required=True, indexed=True
    )
    # Time when the attempt ended (optional until submitted).
    end_time = datastore_services.DateTimeProperty(indexed=True)
    # Whether the attempt was passed (optional until submitted).
    passed = datastore_services.BooleanProperty(indexed=True)
    # The score percentage (optional until submitted).
    score_percentage = datastore_services.FloatProperty(indexed=True)

    @staticmethod
    def get_deletion_policy() -> base_models.DELETION_POLICY:
        """Model contains data directly corresponding to a user."""
        return base_models.DELETION_POLICY.DELETE

    @staticmethod
    def get_model_association_to_user() -> (
        base_models.MODEL_ASSOCIATION_TO_USER
    ):
        """Model contains user data."""
        return base_models.MODEL_ASSOCIATION_TO_USER.MULTIPLE_INSTANCES_PER_USER

    @classmethod
    def get_export_policy(cls) -> Dict[str, base_models.EXPORT_POLICY]:
        """Model export policy for Takeout."""
        return dict(
            super(cls, cls).get_export_policy(),
            **{
                'user_id': base_models.EXPORT_POLICY.NOT_APPLICABLE,
                'offering_id': base_models.EXPORT_POLICY.EXPORTED,
                'offering_version': base_models.EXPORT_POLICY.EXPORTED,
                'start_time': base_models.EXPORT_POLICY.EXPORTED,
                'end_time': base_models.EXPORT_POLICY.EXPORTED,
                'passed': base_models.EXPORT_POLICY.EXPORTED,
                'score_percentage': base_models.EXPORT_POLICY.EXPORTED,
            },
        )

    @classmethod
    def apply_deletion_policy(cls, user_id: str) -> None:
        """Deletes all AssessmentAttemptModel instances associated with the
        given user_id.

        Args:
            user_id: str. The user_id to delete data for.
        """
        datastore_services.delete_multi(
            cls.query(cls.user_id == user_id).fetch(keys_only=True)
        )

    @classmethod
    def has_reference_to_user_id(cls, user_id: str) -> bool:
        """Check whether AssessmentAttemptModel references the given user.

        Args:
            user_id: str. The ID of the user whose data should be checked.

        Returns:
            bool. Whether any models refer to the given user ID.
        """
        return cls.query(cls.user_id == user_id).get(keys_only=True) is not None

    @classmethod
    def export_data(cls, user_id: str) -> Dict[str, Dict[str, str]]:
        """Exports the data from AssessmentAttemptModel associated with the
        given user_id.

        Args:
            user_id: str. The user_id to export data for.

        Returns:
            dict. The exported data.
        """
        user_data = {}
        # Here we use cast because Mypy is unable to infer the correct type
        # for datastore query results.
        attempt_models = cast(
            List[AssessmentAttemptModel],
            cls.query(cls.user_id == user_id).fetch(),
        )
        for attempt_model in attempt_models:
            user_data[attempt_model.id] = {
                'offering_id': attempt_model.offering_id,
                'offering_version': str(attempt_model.offering_version),
                'start_time': utils.get_time_in_millisecs(
                    attempt_model.start_time
                ),
                'end_time': (
                    utils.get_time_in_millisecs(attempt_model.end_time)
                    if attempt_model.end_time
                    else None
                ),
                'passed': (
                    str(attempt_model.passed)
                    if attempt_model.passed is not None
                    else None
                ),
                'score_percentage': (
                    str(attempt_model.score_percentage)
                    if attempt_model.score_percentage is not None
                    else None
                ),
            }
        return user_data

    @classmethod
    def create(
        cls,
        attempt_id: str,
        user_id: str,
        offering_id: str,
        offering_version: int,
        start_time: datetime.datetime,
    ) -> AssessmentAttemptModel:
        """Creates a new AssessmentAttemptModel entry."""
        if cls.get_by_id(attempt_id):
            raise Exception(
                'An AssessmentAttemptModel with the given ID already exists.'
            )

        entity = cls(
            id=attempt_id,
            user_id=user_id,
            offering_id=offering_id,
            offering_version=offering_version,
            start_time=start_time,
        )
        entity.update_timestamps()
        entity.put()
        return entity


class AssessmentQuestionResponseModel(base_models.BaseModel):
    """Model to store a learner's response to an assessment question."""

    # The attempt ID.
    attempt_id = datastore_services.StringProperty(required=True, indexed=True)
    # Note: user_id isn't directly needed here if we rely on attempt_id, but useful for deletion.
    user_id = datastore_services.StringProperty(required=True, indexed=True)
    # The question ID.
    question_id = datastore_services.StringProperty(required=True, indexed=True)
    # The question version.
    question_version = datastore_services.IntegerProperty(
        required=True, indexed=True
    )
    # The skill ID.
    skill_id = datastore_services.StringProperty(required=True, indexed=True)
    # The skill version.
    skill_version = datastore_services.IntegerProperty(
        required=True, indexed=True
    )
    # The learner's answer.
    learner_answer_html = datastore_services.TextProperty()
    # Whether the answer was correct.
    is_correct = datastore_services.BooleanProperty(required=True, indexed=True)

    @staticmethod
    def get_deletion_policy() -> base_models.DELETION_POLICY:
        """Model contains data directly corresponding to a user."""
        return base_models.DELETION_POLICY.DELETE

    @staticmethod
    def get_model_association_to_user() -> (
        base_models.MODEL_ASSOCIATION_TO_USER
    ):
        """Model contains user data."""
        return base_models.MODEL_ASSOCIATION_TO_USER.MULTIPLE_INSTANCES_PER_USER

    @classmethod
    def get_export_policy(cls) -> Dict[str, base_models.EXPORT_POLICY]:
        """Model export policy for Takeout."""
        return dict(
            super(cls, cls).get_export_policy(),
            **{
                'attempt_id': base_models.EXPORT_POLICY.EXPORTED,
                'user_id': base_models.EXPORT_POLICY.NOT_APPLICABLE,
                'question_id': base_models.EXPORT_POLICY.EXPORTED,
                'question_version': base_models.EXPORT_POLICY.EXPORTED,
                'skill_id': base_models.EXPORT_POLICY.EXPORTED,
                'skill_version': base_models.EXPORT_POLICY.EXPORTED,
                'learner_answer_html': base_models.EXPORT_POLICY.EXPORTED,
                'is_correct': base_models.EXPORT_POLICY.EXPORTED,
            },
        )

    @classmethod
    def apply_deletion_policy(cls, user_id: str) -> None:
        """Deletes all instances for user."""
        datastore_services.delete_multi(
            cls.query(cls.user_id == user_id).fetch(keys_only=True)
        )

    @classmethod
    def has_reference_to_user_id(cls, user_id: str) -> bool:
        """Checks if model refers to user."""
        return cls.query(cls.user_id == user_id).get(keys_only=True) is not None

    @classmethod
    def export_data(cls, user_id: str) -> Dict[str, Dict[str, str]]:
        """Exports the user data."""
        user_data = {}
        # Here we use cast because Mypy is unable to infer the correct type
        # for datastore query results.
        response_models = cast(
            List[AssessmentQuestionResponseModel],
            cls.query(cls.user_id == user_id).fetch(),
        )
        for response_model in response_models:
            user_data[response_model.id] = {
                'attempt_id': response_model.attempt_id,
                'question_id': response_model.question_id,
                'question_version': str(response_model.question_version),
                'skill_id': response_model.skill_id,
                'skill_version': str(response_model.skill_version),
                'learner_answer_html': (
                    response_model.learner_answer_html
                    if response_model.learner_answer_html
                    else ''
                ),
                'is_correct': str(response_model.is_correct),
            }
        return user_data

    @classmethod
    def create(
        cls,
        response_id: str,
        attempt_id: str,
        user_id: str,
        question_id: str,
        question_version: int,
        skill_id: str,
        skill_version: int,
        learner_answer_html: Optional[str],
        is_correct: bool,
    ) -> AssessmentQuestionResponseModel:
        """Creates a new AssessmentQuestionResponseModel entry."""
        if cls.get_by_id(response_id):
            raise Exception(
                'An AssessmentQuestionResponseModel with the given ID already exists.'
            )

        entity = cls(
            id=response_id,
            attempt_id=attempt_id,
            user_id=user_id,
            question_id=question_id,
            question_version=question_version,
            skill_id=skill_id,
            skill_version=skill_version,
            learner_answer_html=learner_answer_html,
            is_correct=is_correct,
        )
        entity.update_timestamps()
        entity.put()
        return entity


class CertificateMasteryStatsModel(base_models.BaseModel):
    """Model to store aggregated stats for a certificate offering."""

    # The ID of the certificate offering.
    offering_id = datastore_services.StringProperty(required=True, indexed=True)
    # Total number of attempts.
    total_attempts = datastore_services.IntegerProperty(
        required=True, default=0, indexed=True
    )
    # Total number of passing attempts.
    total_passes = datastore_services.IntegerProperty(
        required=True, default=0, indexed=True
    )
    # Average score percentage.
    average_score = datastore_services.FloatProperty(
        required=True, default=0.0, indexed=True
    )

    @staticmethod
    def get_deletion_policy() -> base_models.DELETION_POLICY:
        """Model does not contain user data."""
        return base_models.DELETION_POLICY.NOT_APPLICABLE

    @staticmethod
    def get_model_association_to_user() -> (
        base_models.MODEL_ASSOCIATION_TO_USER
    ):
        """Model does not contain user data."""
        return base_models.MODEL_ASSOCIATION_TO_USER.NOT_CORRESPONDING_TO_USER

    @classmethod
    def get_export_policy(cls) -> Dict[str, base_models.EXPORT_POLICY]:
        """Model export policy for Takeout."""
        return dict(
            super(cls, cls).get_export_policy(),
            **{
                'offering_id': base_models.EXPORT_POLICY.NOT_APPLICABLE,
                'total_attempts': base_models.EXPORT_POLICY.NOT_APPLICABLE,
                'total_passes': base_models.EXPORT_POLICY.NOT_APPLICABLE,
                'average_score': base_models.EXPORT_POLICY.NOT_APPLICABLE,
            },
        )
