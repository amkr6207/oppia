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

"""Tests for learner assessment domain objects."""

from __future__ import annotations

import datetime

from core import utils
from core.domain import assessment_domain
from core.tests import test_utils


class AssessmentAttemptDomainUnitTest(test_utils.GenericTestBase):
    """Tests for the AssessmentAttempt domain object."""

    def test_initialization_and_validation(self) -> None:
        """Tests initialization and validation of AssessmentAttempt."""
        start_time = datetime.datetime.utcnow()
        attempt = assessment_domain.AssessmentAttempt(
            'attempt_1', 'user_1', 'offering_1', 1, start_time
        )
        attempt.validate()

        attempt.score_percentage = 150.0
        with self.assertRaisesRegex(
            utils.ValidationError, 'Score percentage must be between 0 and 100'
        ):
            attempt.validate()

    def test_to_dict(self) -> None:
        """Tests to_dict method of AssessmentAttempt."""
        start_time = datetime.datetime.utcnow()
        attempt = assessment_domain.AssessmentAttempt(
            'attempt_1', 'user_1', 'offering_1', 1, start_time
        )
        self.assertIn('id', attempt.to_dict())


class AssessmentQuestionResponseDomainUnitTest(test_utils.GenericTestBase):
    """Tests for the AssessmentQuestionResponse domain object."""

    def test_initialization_and_validation(self) -> None:
        """Tests initialization and validation of response."""
        response = assessment_domain.AssessmentQuestionResponse(
            'resp_1', 'attempt_1', 'user_1', 'q_1', 1, 's_1', 1, 'A', True
        )
        response.validate()

        # Here we use MyPy ignore because we are intentionally setting
        # a wrong type to test validation.
        response.is_correct = 'True'  # type: ignore[assignment]
        with self.assertRaisesRegex(
            utils.ValidationError, 'is_correct must be a boolean'
        ):
            response.validate()

    def test_to_dict(self) -> None:
        """Tests to_dict method of AssessmentQuestionResponse."""
        response = assessment_domain.AssessmentQuestionResponse(
            'resp_1', 'attempt_1', 'user_1', 'q_1', 1, 's_1', 1, 'A', True
        )
        self.assertIn('id', response.to_dict())
