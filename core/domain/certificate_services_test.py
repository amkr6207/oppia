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

"""Tests for certificate offering services."""

from __future__ import annotations

from core.domain import certificate_domain, certificate_services
from core.tests import test_utils


class CertificateServicesUnitTest(test_utils.GenericTestBase):
    """Tests for certificate services."""

    def test_save_and_get_offering(self) -> None:
        """Tests saving and getting a certificate offering."""
        offering = certificate_domain.CertificateAssessmentOffering(
            'offering_1', 'Name', 'Desc', 'class_1', ['skill_1'], 60, 1
        )
        certificate_services.save_certificate_assessment_offering(
            'user_1', offering, 'Created offering'
        )

        retrieved_offering = (
            certificate_services.get_certificate_assessment_offering_by_id(
                'offering_1'
            )
        )
        assert retrieved_offering is not None
        self.assertEqual(retrieved_offering.name, 'Name')
        self.assertEqual(retrieved_offering.time_limit_in_minutes, 60)

    def test_update_offering(self) -> None:
        """Tests updating a certificate offering."""
        offering = certificate_domain.CertificateAssessmentOffering(
            'offering_1', 'Name', 'Desc', 'class_1', ['skill_1'], 60, 1
        )
        certificate_services.save_certificate_assessment_offering(
            'user_1', offering, 'Created offering'
        )

        offering.time_limit_in_minutes = 90
        certificate_services.save_certificate_assessment_offering(
            'user_1', offering, 'Updated time limit'
        )

        retrieved_offering = (
            certificate_services.get_certificate_assessment_offering_by_id(
                'offering_1'
            )
        )
        assert retrieved_offering is not None
        self.assertEqual(retrieved_offering.time_limit_in_minutes, 90)

    def test_get_nonexistent_offering_returns_none(self) -> None:
        """Tests getting a nonexistent offering returns None."""
        retrieved_offering = (
            certificate_services.get_certificate_assessment_offering_by_id(
                'nonexistent', strict=False
            )
        )
        self.assertIsNone(retrieved_offering)
