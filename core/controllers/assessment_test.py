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

"""Tests for the assessment controller."""

from __future__ import annotations

from core.domain import certificate_domain, certificate_services
from core.tests import test_utils


class AssessmentAttemptHandlerTest(test_utils.GenericTestBase):
    """Tests for the AssessmentAttemptHandler and AssessmentSubmitHandler."""

    def setUp(self) -> None:
        super().setUp()
        self.signup(self.VIEWER_EMAIL, self.VIEWER_USERNAME)
        self.login(self.VIEWER_EMAIL)

        # Create an offering.
        offering = certificate_domain.CertificateAssessmentOffering(
            'offering_1', 'Name', 'Desc', 'class_1', ['skill_1'], 60, 1
        )
        certificate_services.save_certificate_assessment_offering(
            self.VIEWER_USERNAME, offering, 'Created offering'
        )

    def test_start_and_submit_attempt(self) -> None:
        """Tests starting and submitting an assessment attempt."""
        csrf_token = self.get_new_csrf_token()

        # Start Attempt.
        start_payload = {'offering_id': 'offering_1'}
        response = self.post_json(
            '/assessment_attempt_handler', start_payload, csrf_token=csrf_token
        )
        attempt_id = response['attempt']['id']
        self.assertEqual(response['attempt']['offering_id'], 'offering_1')

        # We don't have questions mapped to skill_1 in the test DB,
        # so questions might be empty.
        self.assertIn('questions', response)

        # Submit Attempt.
        submit_payload = {
            'attempt_id': attempt_id,
            'responses': [
                {
                    'id': 'resp1',
                    'question_id': 'q1',
                    'question_version': 1,
                    'skill_id': 'skill_1',
                    'skill_version': 1,
                    'learner_answer_html': '<p>Answer</p>',
                    'is_correct': True,
                }
            ],
        }
        submit_response = self.post_json(
            '/assessment_submit_handler', submit_payload, csrf_token=csrf_token
        )

        self.assertEqual(submit_response['attempt']['score_percentage'], 100.0)
        self.assertTrue(submit_response['attempt']['passed'])
