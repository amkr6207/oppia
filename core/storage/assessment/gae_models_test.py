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

"""Tests for assessment attempt and response models."""

from __future__ import annotations

import datetime

from core.platform import models
from core.tests import test_utils

MYPY = False
if MYPY:  # pragma: no cover
    from mypy_imports import base_models

(
    base_models,
    assessment_models,
) = models.Registry.import_models(
    [models.Names.BASE_MODEL, models.Names.ASSESSMENT]
)


class AssessmentAttemptModelUnitTest(test_utils.GenericTestBase):
    """Tests for the AssessmentAttemptModel class."""

    def setUp(self) -> None:
        super().setUp()
        self.start_time = datetime.datetime.utcnow()

    def test_create_and_get_model(self) -> None:
        """Tests creating and getting an AssessmentAttemptModel."""
        model = assessment_models.AssessmentAttemptModel.create(
            attempt_id='attempt_1',
            user_id='user_1',
            offering_id='offering_1',
            offering_version=1,
            start_time=self.start_time,
        )
        self.assertEqual(model.user_id, 'user_1')
        retrieved_model = assessment_models.AssessmentAttemptModel.get(
            'attempt_1'
        )
        assert retrieved_model is not None
        self.assertEqual(retrieved_model.offering_id, 'offering_1')

    def test_create_duplicate_model_raises_error(self) -> None:
        """Tests that creating a duplicate model raises an error."""
        assessment_models.AssessmentAttemptModel.create(
            attempt_id='attempt_1',
            user_id='user_1',
            offering_id='offering_1',
            offering_version=1,
            start_time=self.start_time,
        )

        with self.assertRaisesRegex(
            Exception,
            'An AssessmentAttemptModel with the given ID already exists.',
        ):
            assessment_models.AssessmentAttemptModel.create(
                attempt_id='attempt_1',
                user_id='user_2',
                offering_id='offering_2',
                offering_version=1,
                start_time=self.start_time,
            )

    def test_apply_deletion_policy(self) -> None:
        """Tests applying deletion policy for a user."""
        assessment_models.AssessmentAttemptModel.create(
            attempt_id='attempt_1',
            user_id='user_1',
            offering_id='offering_1',
            offering_version=1,
            start_time=self.start_time,
        )
        assessment_models.AssessmentAttemptModel.create(
            attempt_id='attempt_2',
            user_id='user_1',
            offering_id='offering_2',
            offering_version=1,
            start_time=self.start_time,
        )
        assessment_models.AssessmentAttemptModel.create(
            attempt_id='attempt_3',
            user_id='user_2',
            offering_id='offering_1',
            offering_version=1,
            start_time=self.start_time,
        )

        self.assertTrue(
            assessment_models.AssessmentAttemptModel.has_reference_to_user_id(
                'user_1'
            )
        )
        assessment_models.AssessmentAttemptModel.apply_deletion_policy('user_1')
        self.assertFalse(
            assessment_models.AssessmentAttemptModel.has_reference_to_user_id(
                'user_1'
            )
        )
        self.assertTrue(
            assessment_models.AssessmentAttemptModel.has_reference_to_user_id(
                'user_2'
            )
        )

    def test_export_data(self) -> None:
        """Tests exporting user data."""
        assessment_models.AssessmentAttemptModel.create(
            attempt_id='attempt_1',
            user_id='user_1',
            offering_id='offering_1',
            offering_version=1,
            start_time=self.start_time,
        )
        user_data = assessment_models.AssessmentAttemptModel.export_data(
            'user_1'
        )
        self.assertIn('attempt_1', user_data)
        self.assertEqual(user_data['attempt_1']['offering_id'], 'offering_1')

    def test_get_deletion_policy(self) -> None:
        """Tests the deletion policy."""
        self.assertEqual(
            assessment_models.AssessmentAttemptModel.get_deletion_policy(),
            base_models.DELETION_POLICY.DELETE,
        )

    def test_get_model_association_to_user(self) -> None:
        """Tests the model association to user."""
        self.assertEqual(
            assessment_models.AssessmentAttemptModel.get_model_association_to_user(),
            base_models.MODEL_ASSOCIATION_TO_USER.MULTIPLE_INSTANCES_PER_USER,
        )

    def test_get_export_policy(self) -> None:
        """Tests the export policy."""
        self.assertEqual(
            assessment_models.AssessmentAttemptModel.get_export_policy()[
                'offering_id'
            ],
            base_models.EXPORT_POLICY.EXPORTED,
        )


class AssessmentQuestionResponseModelUnitTest(test_utils.GenericTestBase):
    """Tests for the AssessmentQuestionResponseModel class."""

    def test_create_and_get_model(self) -> None:
        """Tests creating and getting a response model."""
        model = assessment_models.AssessmentQuestionResponseModel.create(
            response_id='response_1',
            attempt_id='attempt_1',
            user_id='user_1',
            question_id='question_1',
            question_version=1,
            skill_id='skill_1',
            skill_version=1,
            learner_answer_html='<p>4</p>',
            is_correct=True,
        )
        self.assertEqual(model.attempt_id, 'attempt_1')
        retrieved_model = assessment_models.AssessmentQuestionResponseModel.get(
            'response_1'
        )
        assert retrieved_model is not None
        self.assertEqual(retrieved_model.learner_answer_html, '<p>4</p>')

    def test_create_duplicate_model_raises_error(self) -> None:
        """Tests that creating a duplicate response model raises error."""
        assessment_models.AssessmentQuestionResponseModel.create(
            response_id='response_1',
            attempt_id='attempt_1',
            user_id='user_1',
            question_id='q1',
            question_version=1,
            skill_id='s1',
            skill_version=1,
            learner_answer_html='',
            is_correct=False,
        )

        with self.assertRaisesRegex(
            Exception,
            'An AssessmentQuestionResponseModel with the given ID already exists.',
        ):
            assessment_models.AssessmentQuestionResponseModel.create(
                response_id='response_1',
                attempt_id='attempt_2',
                user_id='user_1',
                question_id='q1',
                question_version=1,
                skill_id='s1',
                skill_version=1,
                learner_answer_html='',
                is_correct=False,
            )

    def test_apply_deletion_policy(self) -> None:
        """Tests applying deletion policy for responses."""
        assessment_models.AssessmentQuestionResponseModel.create(
            response_id='response_1',
            attempt_id='attempt_1',
            user_id='user_1',
            question_id='q1',
            question_version=1,
            skill_id='s1',
            skill_version=1,
            learner_answer_html='',
            is_correct=False,
        )
        self.assertTrue(
            assessment_models.AssessmentQuestionResponseModel.has_reference_to_user_id(
                'user_1'
            )
        )
        assessment_models.AssessmentQuestionResponseModel.apply_deletion_policy(
            'user_1'
        )
        self.assertFalse(
            assessment_models.AssessmentQuestionResponseModel.has_reference_to_user_id(
                'user_1'
            )
        )

    def test_export_data(self) -> None:
        """Tests exporting user data for responses."""
        assessment_models.AssessmentQuestionResponseModel.create(
            response_id='response_1',
            attempt_id='attempt_1',
            user_id='user_1',
            question_id='q1',
            question_version=1,
            skill_id='s1',
            skill_version=1,
            learner_answer_html='<p>my answer</p>',
            is_correct=False,
        )
        user_data = (
            assessment_models.AssessmentQuestionResponseModel.export_data(
                'user_1'
            )
        )
        self.assertIn('response_1', user_data)
        self.assertEqual(
            user_data['response_1']['learner_answer_html'], '<p>my answer</p>'
        )

    def test_get_deletion_policy(self) -> None:
        """Tests the deletion policy for responses."""
        self.assertEqual(
            assessment_models.AssessmentQuestionResponseModel.get_deletion_policy(),
            base_models.DELETION_POLICY.DELETE,
        )

    def test_get_model_association_to_user(self) -> None:
        """Tests the model association to user for responses."""
        self.assertEqual(
            assessment_models.AssessmentQuestionResponseModel.get_model_association_to_user(),
            base_models.MODEL_ASSOCIATION_TO_USER.MULTIPLE_INSTANCES_PER_USER,
        )

    def test_get_export_policy(self) -> None:
        """Tests the export policy for responses."""
        self.assertEqual(
            assessment_models.AssessmentQuestionResponseModel.get_export_policy()[
                'question_id'
            ],
            base_models.EXPORT_POLICY.EXPORTED,
        )
