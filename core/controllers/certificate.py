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

"""Controllers for certificate assessment offerings."""

from __future__ import annotations

from core.controllers import acl_decorators, base
from core.domain import certificate_domain, certificate_services

from typing import Dict


class CertificateOfferingHandler(
    base.BaseHandler[Dict[str, str], Dict[str, str]]
):
    """Handler for certificate assessment offerings."""

    GET_HANDLER_ERROR_RETURN_TYPE = 'json'
    URL_PATH_ARGS_SCHEMAS: Dict[str, str] = {}
    HANDLER_ARGS_SCHEMAS = {
        'GET': {'offering_id': {'schema': {'type': 'unicode'}}},
        'POST': {
            'offering_id': {'schema': {'type': 'unicode'}},
            'name': {'schema': {'type': 'unicode'}},
            'description': {'schema': {'type': 'unicode'}},
            'classroom_id': {'schema': {'type': 'unicode'}},
            'attached_skill_ids': {
                'schema': {'type': 'list', 'items': {'type': 'unicode'}}
            },
            'time_limit_in_minutes': {'schema': {'type': 'int'}},
        },
    }

    @acl_decorators.can_access_topics_and_skills_dashboard
    def get(self) -> None:
        """Handles GET requests to fetch certificate offerings."""
        offering_id = self.normalized_request.get('offering_id')
        offering = (
            certificate_services.get_certificate_assessment_offering_by_id(
                offering_id, strict=False
            )
        )
        if offering:
            self.render_json({'offering': offering.to_dict()})
        else:
            self.render_json({'offering': None})

    @acl_decorators.can_access_topics_and_skills_dashboard
    def post(self) -> None:
        """Handles POST requests to create a new certificate offering."""
        offering_id = self.normalized_payload.get('offering_id')
        name = self.normalized_payload.get('name')
        description = self.normalized_payload.get('description')
        classroom_id = self.normalized_payload.get('classroom_id')
        attached_skill_ids = self.normalized_payload.get('attached_skill_ids')
        time_limit_in_minutes = self.normalized_payload.get(
            'time_limit_in_minutes'
        )

        offering = certificate_domain.CertificateAssessmentOffering(
            offering_id,
            name,
            description,
            classroom_id,
            attached_skill_ids,
            time_limit_in_minutes,
            1,
        )
        certificate_services.save_certificate_assessment_offering(
            self.user_id, offering, 'Created new offering.'
        )
        self.render_json({'offering': offering.to_dict()})
