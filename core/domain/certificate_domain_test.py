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

"""Tests for certificate assessment offering domain objects."""

from __future__ import annotations

from core import utils
from core.domain import certificate_domain
from core.tests import test_utils


class CertificateAssessmentOfferingDomainUnitTest(test_utils.GenericTestBase):
    """Tests for the CertificateAssessmentOffering domain object."""

    def test_initialization(self) -> None:
        offering = certificate_domain.CertificateAssessmentOffering(
            'offering_1', 'Name', 'Desc', 'class_1', ['skill_1'], 60, 1
        )
        self.assertEqual(offering.id, 'offering_1')
        self.assertEqual(offering.name, 'Name')
        self.assertEqual(offering.description, 'Desc')

    def test_validation(self) -> None:
        offering = certificate_domain.CertificateAssessmentOffering(
            'offering_1', 'Name', 'Desc', 'class_1', ['skill_1'], 60, 1
        )
        offering.validate()

        offering.time_limit_in_minutes = -5
        with self.assertRaisesRegex(
            utils.ValidationError, 'Time limit must be positive'
        ):
            offering.validate()

        offering.time_limit_in_minutes = 60
        offering.attached_skill_ids = []
        with self.assertRaisesRegex(
            utils.ValidationError, 'Attached skill IDs cannot be empty'
        ):
            offering.validate()

    def test_to_dict(self) -> None:
        offering = certificate_domain.CertificateAssessmentOffering(
            'offering_1', 'Name', 'Desc', 'class_1', ['skill_1'], 60, 1
        )
        self.assertEqual(
            offering.to_dict(),
            {
                'id': 'offering_1',
                'name': 'Name',
                'description': 'Desc',
                'classroom_id': 'class_1',
                'attached_skill_ids': ['skill_1'],
                'time_limit_in_minutes': 60,
                'version': 1,
            },
        )
