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

"""Tests for learner assessment services."""

from __future__ import annotations

from core.domain import (
    assessment_domain,
    assessment_services,
    certificate_domain,
    certificate_services,
)
from core.tests import test_utils


class AssessmentServicesUnitTest(test_utils.GenericTestBase):
    """Tests for assessment services."""

    def setUp(self) -> None:
        super().setUp()
        self.offering = certificate_domain.CertificateAssessmentOffering(
            'offering_1', 'Name', 'Desc', 'class_1', ['skill_1'], 60, 1
        )
        certificate_services.save_certificate_assessment_offering(
            'user_1', self.offering, 'Created offering'
        )

    def test_start_attempt(self) -> None:
        """Tests starting a new assessment attempt."""
        attempt = assessment_services.start_assessment_attempt(
            'user_2', 'offering_1'
        )
        self.assertEqual(attempt.user_id, 'user_2')
        self.assertEqual(attempt.offering_id, 'offering_1')
        self.assertIsNotNone(attempt.start_time)
        self.assertIsNone(attempt.end_time)

    def test_submit_passing_attempt(self) -> None:
        """Tests submitting a passing assessment attempt."""
        attempt = assessment_services.start_assessment_attempt(
            'user_2', 'offering_1'
        )

        # Make it 5/5 passing for 100% score.
        responses = [
            assessment_domain.AssessmentQuestionResponse(
                f'r{i}', attempt.id, 'u2', f'q{i}', 1, 's1', 1, 'A', True
            )
            for i in range(5)
        ]

        updated_attempt = assessment_services.submit_assessment_attempt(
            attempt.id, responses
        )
        self.assertIsNotNone(updated_attempt.end_time)
        self.assertEqual(updated_attempt.score_percentage, 100.0)
        self.assertTrue(updated_attempt.passed)

    def test_submit_failing_attempt(self) -> None:
        """Tests submitting a failing assessment attempt."""
        attempt = assessment_services.start_assessment_attempt(
            'user_2', 'offering_1'
        )

        # 1/5 passing = 20%.
        responses = [
            assessment_domain.AssessmentQuestionResponse(
                f'r{i}', attempt.id, 'u2', f'q{i}', 1, 's1', 1, 'A', i == 0
            )
            for i in range(5)
        ]

        updated_attempt = assessment_services.submit_assessment_attempt(
            attempt.id, responses
        )
        self.assertEqual(updated_attempt.score_percentage, 20.0)
        self.assertFalse(updated_attempt.passed)
