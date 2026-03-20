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

"""Tests for the certificate assessment offering controllers."""

from __future__ import annotations

from core.tests import test_utils


class CertificateOfferingHandlerTest(test_utils.GenericTestBase):
    """Tests for the CertificateOfferingHandler."""

    def setUp(self) -> None:
        super().setUp()
        self.signup(self.CURRICULUM_ADMIN_EMAIL, self.CURRICULUM_ADMIN_USERNAME)
        self.set_curriculum_admins([self.CURRICULUM_ADMIN_USERNAME])
        self.login(self.CURRICULUM_ADMIN_EMAIL)

    def test_create_and_get_offering(self) -> None:
        """Tests creating and getting a certificate offering."""
        payload = {
            'offering_id': 'offering_class1',
            'name': 'Basic Math Cert',
            'description': 'Get certified in basic math',
            'classroom_id': 'math',
            'attached_skill_ids': ['skill1', 'skill2'],
            'time_limit_in_minutes': 60,
        }

        csrf_token = self.get_new_csrf_token()
        response = self.post_json(
            '/certificate_offering_handler', payload, csrf_token=csrf_token
        )
        self.assertEqual(response['offering']['name'], 'Basic Math Cert')

        # Test GET.
        get_response = self.get_json(
            '/certificate_offering_handler',
            params={'offering_id': 'offering_class1'},
        )
        self.assertEqual(get_response['offering']['name'], 'Basic Math Cert')

    def test_get_nonexistent_offering(self) -> None:
        """Tests getting a nonexistent offering."""
        get_response = self.get_json(
            '/certificate_offering_handler',
            params={'offering_id': 'nonexistent'},
        )
        self.assertIsNone(get_response['offering'])
