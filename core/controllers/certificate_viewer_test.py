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

"""Tests for the certificate viewer controller."""

from __future__ import annotations
import datetime

from core.domain import certificate_domain
from core.domain import certificate_services
from core.platform import models
from core.tests import test_utils

(assessment_models,) = models.Registry.import_models([models.Names.ASSESSMENT])


class CertificateViewerPageTest(test_utils.GenericTestBase):
    """Tests for the CertificateViewerPage."""

    def setUp(self) -> None:
        super().setUp()
        self.signup(self.VIEWER_EMAIL, self.VIEWER_USERNAME)
        self.login(self.VIEWER_EMAIL)

        # Create an offering.
        self.offering = certificate_domain.CertificateAssessmentOffering(
            'offering_1', 'Math Mastery', 'Desc', 'class_1', ['skill_1'], 60, 1
        )
        certificate_services.save_certificate_assessment_offering(
            self.VIEWER_USERNAME, self.offering, 'Created offering'
        )

    def test_get_certificate_viewer_page(self) -> None:
        """Tests the GET request for certificate viewer page."""
        # Create a successful attempt model.
        viewer_id = self.get_user_id_from_email(self.VIEWER_EMAIL)
        now = datetime.datetime.utcnow()
        attempt_model = assessment_models.AssessmentAttemptModel(
            id='attempt_1',
            user_id=viewer_id,
            offering_id='offering_1',
            offering_version=1,
            start_time=now,
            end_time=now,
            passed=True,
            score_percentage=100.0,
        )
        attempt_model.update_timestamps()
        attempt_model.put()

        response = self.get_html_response('/certificate_viewer/attempt_1')
        self.assertIn('Math Mastery', response)
        self.assertIn(self.VIEWER_USERNAME, response)

    def test_get_certificate_viewer_page_with_invalid_id_raises_404(
        self,
    ) -> None:
        """Tests that invalid attempt ID raises 404."""
        self.get_html_response(
            '/certificate_viewer/invalid_id', expected_status_int=404
        )

    def test_get_certificate_viewer_page_with_failed_attempt_raises_404(
        self,
    ) -> None:
        """Tests that failed attempt ID raises 404."""
        # Create a failed attempt model.
        viewer_id = self.get_user_id_from_email(self.VIEWER_EMAIL)
        now = datetime.datetime.utcnow()
        attempt_model = assessment_models.AssessmentAttemptModel(
            id='attempt_2',
            user_id=viewer_id,
            offering_id='offering_1',
            offering_version=1,
            start_time=now,
            end_time=now,
            passed=False,
            score_percentage=20.0,
        )
        attempt_model.update_timestamps()
        attempt_model.put()

        self.get_html_response(
            '/certificate_viewer/attempt_2', expected_status_int=404
        )
