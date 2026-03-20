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

"""Tests for certificate assessment offering models."""

from __future__ import annotations

from core.platform import models
from core.tests import test_utils

MYPY = False
if MYPY:  # pragma: no cover
    from mypy_imports import base_models

(
    base_models,
    certificate_models,
) = models.Registry.import_models(
    [models.Names.BASE_MODEL, models.Names.CERTIFICATE]
)


class CertificateAssessmentOfferingModelUnitTest(test_utils.GenericTestBase):
    """Tests for the CertificateAssessmentOfferingModel class."""

    def test_create_and_get_model(self) -> None:
        """Tests creating and getting a CertificateAssessmentOfferingModel."""
        model = certificate_models.CertificateAssessmentOfferingModel.create(
            offering_id='offering_1',
            name='Test Offering',
            description='Test Description',
            classroom_id='classroom_1',
            attached_skill_ids=['skill_1', 'skill_2'],
            time_limit_in_minutes=60,
        )
        model.commit(
            committer_id='user_A',
            commit_message='Created offering',
            commit_cmds=[{'cmd': 'create_new'}],
        )

        retrieved_model = (
            certificate_models.CertificateAssessmentOfferingModel.get(
                'offering_1'
            )
        )
        # Ruling out the possibility of None for mypy type checking.
        assert retrieved_model is not None
        self.assertEqual(retrieved_model.name, 'Test Offering')
        self.assertEqual(retrieved_model.description, 'Test Description')
        self.assertEqual(retrieved_model.classroom_id, 'classroom_1')
        self.assertEqual(
            retrieved_model.attached_skill_ids, ['skill_1', 'skill_2']
        )
        self.assertEqual(retrieved_model.time_limit_in_minutes, 60)

    def test_create_duplicate_model_raises_error(self) -> None:
        """Tests that duplicate model creation raises error."""
        certificate_models.CertificateAssessmentOfferingModel.create(
            offering_id='offering_1',
            name='Test Offering',
            description='Test Description',
            classroom_id='classroom_1',
            attached_skill_ids=['skill_1', 'skill_2'],
            time_limit_in_minutes=60,
        ).commit(
            committer_id='user_A',
            commit_message='Created offering',
            commit_cmds=[{'cmd': 'create_new'}],
        )

        with self.assertRaisesRegex(
            Exception,
            'A certificate assessment offering with the given ID already exists.',
        ):
            certificate_models.CertificateAssessmentOfferingModel.create(
                offering_id='offering_1',
                name='Test Offering 2',
                description='Test Description 2',
                classroom_id='classroom_1',
                attached_skill_ids=['skill_1'],
                time_limit_in_minutes=30,
            )

    def test_get_deletion_policy_not_applicable(self) -> None:
        """Tests that deletion policy is NOT_APPLICABLE."""
        self.assertEqual(
            certificate_models.CertificateAssessmentOfferingModel.get_deletion_policy(),
            base_models.DELETION_POLICY.NOT_APPLICABLE,
        )
        self.assertEqual(
            certificate_models.CertificateAssessmentOfferingSnapshotContentModel.get_deletion_policy(),
            base_models.DELETION_POLICY.NOT_APPLICABLE,
        )

    def test_get_model_association_to_user_not_corresponding_to_user(
        self,
    ) -> None:
        """Tests model association to user is NOT_CORRESPONDING_TO_USER."""
        self.assertEqual(
            certificate_models.CertificateAssessmentOfferingModel.get_model_association_to_user(),
            base_models.MODEL_ASSOCIATION_TO_USER.NOT_CORRESPONDING_TO_USER,
        )
        self.assertEqual(
            certificate_models.CertificateAssessmentOfferingCommitLogEntryModel.get_model_association_to_user(),
            base_models.MODEL_ASSOCIATION_TO_USER.NOT_CORRESPONDING_TO_USER,
        )

    def test_get_export_policy_not_applicable(self) -> None:
        """Tests that export policy is NOT_APPLICABLE."""
        self.assertEqual(
            certificate_models.CertificateAssessmentOfferingModel.get_export_policy()[
                'name'
            ],
            base_models.EXPORT_POLICY.NOT_APPLICABLE,
        )
        self.assertEqual(
            certificate_models.CertificateAssessmentOfferingCommitLogEntryModel.get_export_policy()[
                'certificate_assessment_offering_id'
            ],
            base_models.EXPORT_POLICY.NOT_APPLICABLE,
        )

    def test_get_instance_id_for_commit_log(self) -> None:
        """Tests get_instance_id for the commit log entry model."""
        self.assertEqual(
            certificate_models.CertificateAssessmentOfferingCommitLogEntryModel.get_instance_id(
                'offering_1', 1
            ),
            'certificate_offering-offering_1-1',
        )
