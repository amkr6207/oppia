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

"""Models for storing the certificate assessment offering data."""

from __future__ import annotations

from core.constants import constants
from core.platform import models

from typing import Dict, List, Mapping, Optional

MYPY = False
if MYPY:  # pragma: no cover
    from mypy_imports import base_models, datastore_services

(base_models,) = models.Registry.import_models([models.Names.BASE_MODEL])

datastore_services = models.Registry.import_datastore_services()


class CertificateAssessmentOfferingSnapshotMetadataModel(
    base_models.BaseSnapshotMetadataModel
):
    """Storage model for the metadata for a certificate assessment
    offering snapshot.
    """

    pass


class CertificateAssessmentOfferingSnapshotContentModel(
    base_models.BaseSnapshotContentModel
):
    """Storage model for the content of a certificate assessment
    offering snapshot.
    """

    @staticmethod
    def get_deletion_policy() -> base_models.DELETION_POLICY:
        """Model doesn't contain any data directly corresponding to a user."""
        return base_models.DELETION_POLICY.NOT_APPLICABLE


class CertificateAssessmentOfferingCommitLogEntryModel(
    base_models.BaseCommitLogEntryModel
):
    """Log of commits to certificate assessment offerings.

    A new instance of this model is created and saved every time a commit to
    CertificateAssessmentOfferingModel occurs.

    The id for this model is of the form
    'certificate_assessment_offering-[offering_id]-[version]'.
    """

    # The id of the offering being edited.
    certificate_assessment_offering_id = datastore_services.StringProperty(
        indexed=True, required=True
    )

    @classmethod
    def get_instance_id(cls, offering_id: str, version: int) -> str:
        """This function returns the generated id for the get_commit function
        in the parent class.

        Args:
            offering_id: str. The id of the offering being edited.
            version: int. The version number of the offering after the commit.

        Returns:
            str. The commit id with the offering id and version number.
        """
        return 'certificate_offering-%s-%s' % (offering_id, version)

    @staticmethod
    def get_model_association_to_user() -> (
        base_models.MODEL_ASSOCIATION_TO_USER
    ):
        """The history of commits is not relevant for the purposes of Takeout
        since commits don't contain relevant data corresponding to users.
        """
        return base_models.MODEL_ASSOCIATION_TO_USER.NOT_CORRESPONDING_TO_USER

    @classmethod
    def get_export_policy(cls) -> Dict[str, base_models.EXPORT_POLICY]:
        """Model contains data corresponding to a user, but this isn't exported
        because the history of commits isn't deemed as useful for users since
        commit logs don't contain relevant data corresponding to those users.
        """
        return dict(
            super(cls, cls).get_export_policy(),
            **{
                'certificate_assessment_offering_id': base_models.EXPORT_POLICY.NOT_APPLICABLE
            },
        )


class CertificateAssessmentOfferingModel(base_models.VersionedModel):
    """Model for storing Certificate Assessment Offerings.

    This class should only be imported by the certificate domain services
    and test files.
    """

    SNAPSHOT_METADATA_CLASS = CertificateAssessmentOfferingSnapshotMetadataModel
    SNAPSHOT_CONTENT_CLASS = CertificateAssessmentOfferingSnapshotContentModel
    COMMIT_LOG_ENTRY_CLASS = CertificateAssessmentOfferingCommitLogEntryModel
    ALLOW_REVERT = False

    # The name of the certificate offering.
    name = datastore_services.StringProperty(required=True, indexed=True)
    # The description of the certificate offering.
    description = datastore_services.StringProperty(required=True, indexed=True)
    # The ID of the classroom this offering supports.
    classroom_id = datastore_services.StringProperty(
        required=True, indexed=True
    )
    # A list of skill IDs attached to this offering.
    attached_skill_ids = datastore_services.StringProperty(
        repeated=True, indexed=True
    )
    # Time limit for the assessment in minutes (e.g. 60).
    time_limit_in_minutes = datastore_services.IntegerProperty(
        required=True, indexed=True
    )

    @staticmethod
    def get_deletion_policy() -> base_models.DELETION_POLICY:
        """Model doesn't contain any data directly corresponding to a user."""
        return base_models.DELETION_POLICY.NOT_APPLICABLE

    @staticmethod
    def get_model_association_to_user() -> (
        base_models.MODEL_ASSOCIATION_TO_USER
    ):
        """Model does not contain user data."""
        return base_models.MODEL_ASSOCIATION_TO_USER.NOT_CORRESPONDING_TO_USER

    @classmethod
    def get_export_policy(cls) -> Dict[str, base_models.EXPORT_POLICY]:
        """Model doesn't contain any data directly corresponding to a user."""
        return dict(
            super(cls, cls).get_export_policy(),
            **{
                'name': base_models.EXPORT_POLICY.NOT_APPLICABLE,
                'description': base_models.EXPORT_POLICY.NOT_APPLICABLE,
                'classroom_id': base_models.EXPORT_POLICY.NOT_APPLICABLE,
                'attached_skill_ids': base_models.EXPORT_POLICY.NOT_APPLICABLE,
                'time_limit_in_minutes': base_models.EXPORT_POLICY.NOT_APPLICABLE,
            },
        )

    def compute_models_to_commit(
        self,
        committer_id: str,
        commit_type: str,
        commit_message: Optional[str],
        commit_cmds: base_models.AllowedCommitCmdsListType,
        additional_models: Mapping[str, base_models.BaseModel],
    ) -> base_models.ModelsToPutDict:
        """Record the event to the commit log after the model commit."""
        models_to_put = super().compute_models_to_commit(
            committer_id,
            commit_type,
            commit_message,
            commit_cmds,
            additional_models,
        )

        commit_log_entry = (
            CertificateAssessmentOfferingCommitLogEntryModel.create(
                self.id,
                self.version,
                committer_id,
                commit_type,
                commit_message,
                commit_cmds,
                constants.ACTIVITY_STATUS_PUBLIC,
                False,
            )
        )
        commit_log_entry.certificate_assessment_offering_id = self.id
        return {
            'snapshot_metadata_model': models_to_put['snapshot_metadata_model'],
            'snapshot_content_model': models_to_put['snapshot_content_model'],
            'commit_log_model': commit_log_entry,
            'versioned_model': models_to_put['versioned_model'],
        }

    @classmethod
    def create(
        cls,
        offering_id: str,
        name: str,
        description: str,
        classroom_id: str,
        attached_skill_ids: List[str],
        time_limit_in_minutes: int,
    ) -> 'CertificateAssessmentOfferingModel':
        """Creates a new CertificateAssessmentOfferingModel entry.

        Args:
            offering_id: str. ID of the newly-created offering.
            name: str. The name of the offering.
            description: str. The description.
            classroom_id: str. The classroom this belongs to.
            attached_skill_ids: list(str). The skill IDs covered.
            time_limit_in_minutes: int. Time limit.

        Returns:
            CertificateAssessmentOfferingModel. The newly created instance.

        Raises:
            Exception. A model with the given ID already exists.
        """
        if cls.get_by_id(offering_id):
            raise Exception(
                'A certificate assessment offering with the given ID '
                'already exists.'
            )

        entity = cls(
            id=offering_id,
            name=name,
            description=description,
            classroom_id=classroom_id,
            attached_skill_ids=attached_skill_ids,
            time_limit_in_minutes=time_limit_in_minutes,
        )
        return entity
