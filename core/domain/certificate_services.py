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

"""Commands that can be used to operate on certificate assessment offerings."""

from __future__ import annotations

from core.domain import certificate_domain
from core.platform import models

from typing import List, Optional

MYPY = False
if MYPY:  # pragma: no cover
    from mypy_imports import certificate_models

(certificate_models,) = models.Registry.import_models(
    [models.Names.CERTIFICATE]
)


def _get_certificate_assessment_offering_from_model(
    offering_model: certificate_models.CertificateAssessmentOfferingModel,
) -> certificate_domain.CertificateAssessmentOffering:
    """Returns a CertificateAssessmentOffering domain object from a model.

    Args:
        offering_model: CertificateAssessmentOfferingModel. The model object.

    Returns:
        CertificateAssessmentOffering. The domain object.
    """
    return certificate_domain.CertificateAssessmentOffering(
        offering_model.id,
        offering_model.name,
        offering_model.description,
        offering_model.classroom_id,
        offering_model.attached_skill_ids,
        offering_model.time_limit_in_minutes,
        offering_model.version,
    )


def get_certificate_assessment_offering_by_id(
    offering_id: str, strict: bool = True
) -> Optional[certificate_domain.CertificateAssessmentOffering]:
    """Returns a domain object representing a certificate offering.

    Args:
        offering_id: str. The ID of the offering.
        strict: bool. Whether to fail noisily if no offering exists.

    Returns:
        CertificateAssessmentOffering or None. The domain object.
    """
    offering_model = certificate_models.CertificateAssessmentOfferingModel.get(
        offering_id, strict=strict
    )
    if offering_model:
        return _get_certificate_assessment_offering_from_model(offering_model)
    return None


def save_certificate_assessment_offering(
    committer_id: str,
    offering: certificate_domain.CertificateAssessmentOffering,
    commit_message: str,
) -> None:
    """Saves a certificate offering domain object to the datastore.

    Args:
        committer_id: str. The ID of the user making the commit.
        offering: CertificateAssessmentOffering. The domain object to save.
        commit_message: str. The commit message.
    """
    offering.validate()

    offering_model = certificate_models.CertificateAssessmentOfferingModel.get(
        offering.id, strict=False
    )
    is_new = False

    if offering_model is None:
        offering_model = (
            certificate_models.CertificateAssessmentOfferingModel.create(
                offering.id,
                offering.name,
                offering.description,
                offering.classroom_id,
                offering.attached_skill_ids,
                offering.time_limit_in_minutes,
            )
        )
        is_new = True
    else:
        offering_model.name = offering.name
        offering_model.description = offering.description
        offering_model.classroom_id = offering.classroom_id
        offering_model.attached_skill_ids = offering.attached_skill_ids
        offering_model.time_limit_in_minutes = offering.time_limit_in_minutes

    commit_cmd = {'cmd': 'create_new'} if is_new else {'cmd': 'edit_offering'}

    offering_model.commit(committer_id, commit_message, [commit_cmd])


def get_certificate_assessment_offerings_by_classroom_id(
    classroom_id: str,
) -> List[certificate_domain.CertificateAssessmentOffering]:
    """Returns a list of certificate offerings for a classroom.

    Args:
        classroom_id: str. The ID of the classroom.

    Returns:
        list(CertificateAssessmentOffering). A list of certificate offerings.
    """
    offering_models = (
        certificate_models.CertificateAssessmentOfferingModel.get_all()
        .filter(
            certificate_models.CertificateAssessmentOfferingModel.classroom_id
            == classroom_id
        )
        .fetch()
    )
    return [
        _get_certificate_assessment_offering_from_model(model)
        for model in offering_models
    ]


def get_all_certificate_assessment_offerings() -> (
    List[certificate_domain.CertificateAssessmentOffering]
):
    """Returns all certificate offerings.

    Returns:
        list(CertificateAssessmentOffering). A list of all certificate offerings.
    """
    offering_models = (
        certificate_models.CertificateAssessmentOfferingModel.get_all().fetch()
    )
    return [
        _get_certificate_assessment_offering_from_model(model)
        for model in offering_models
    ]
