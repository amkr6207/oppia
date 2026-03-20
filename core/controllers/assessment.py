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

"""Controllers for learner assessment attempts and submissions."""

from __future__ import annotations

from core import feconf
from core.controllers import acl_decorators, base
from core.domain import (
    assessment_domain,
    assessment_services,
    certificate_services,
)

from typing import Dict


class AssessmentAttemptHandler(
    base.BaseHandler[Dict[str, str], Dict[str, str]]
):
    """Handler for starting an assessment attempt."""

    GET_HANDLER_ERROR_RETURN_TYPE = feconf.HANDLER_TYPE_JSON
    URL_PATH_ARGS_SCHEMAS: Dict[str, str] = {}
    HANDLER_ARGS_SCHEMAS = {
        'POST': {'offering_id': {'schema': {'type': 'unicode'}}}
    }

    @acl_decorators.can_access_learner_dashboard
    def post(self) -> None:
        """Handles POST requests to start an assessment attempt."""
        offering_id = self.normalized_payload.get('offering_id')

        # Verify that the offering exists.
        offering = (
            certificate_services.get_certificate_assessment_offering_by_id(
                offering_id, strict=False
            )
        )
        if not offering:
            raise self.PageNotFoundException('Certificate offering not found.')

        attempt = assessment_services.start_assessment_attempt(
            self.user_id, offering_id
        )
        questions = assessment_services.fetch_questions_for_certificate(
            offering_id
        )

        self.render_json({'attempt': attempt.to_dict(), 'questions': questions})


class AssessmentSubmitHandler(base.BaseHandler[Dict[str, str], Dict[str, str]]):
    """Handler for submitting an assessment attempt."""

    GET_HANDLER_ERROR_RETURN_TYPE = feconf.HANDLER_TYPE_JSON
    URL_PATH_ARGS_SCHEMAS: Dict[str, str] = {}
    HANDLER_ARGS_SCHEMAS = {
        'POST': {
            'attempt_id': {'schema': {'type': 'unicode'}},
            'responses': {
                'schema': {
                    'type': 'list',
                    'items': {
                        'type': 'dict',
                        'properties': [
                            {'name': 'id', 'schema': {'type': 'unicode'}},
                            {
                                'name': 'question_id',
                                'schema': {'type': 'unicode'},
                            },
                            {
                                'name': 'question_version',
                                'schema': {'type': 'int'},
                            },
                            {'name': 'skill_id', 'schema': {'type': 'unicode'}},
                            {
                                'name': 'skill_version',
                                'schema': {'type': 'int'},
                            },
                            {
                                'name': 'learner_answer_html',
                                'schema': {'type': 'unicode'},
                            },
                            {'name': 'is_correct', 'schema': {'type': 'bool'}},
                        ],
                    },
                }
            },
        }
    }

    @acl_decorators.can_access_learner_dashboard
    def post(self) -> None:
        """Handles POST requests to submit an assessment attempt."""
        attempt_id = self.normalized_payload.get('attempt_id')
        responses_dicts = self.normalized_payload.get('responses')

        domain_responses = []
        for rd in responses_dicts:
            # Ensure that all properties exist according to domain object.
            resp = assessment_domain.AssessmentQuestionResponse(
                response_id=rd['id'],
                attempt_id=attempt_id,
                user_id=self.user_id,
                question_id=rd['question_id'],
                question_version=rd['question_version'],
                skill_id=rd['skill_id'],
                skill_version=rd['skill_version'],
                learner_answer_html=rd['learner_answer_html'],
                is_correct=rd['is_correct'],
            )
            domain_responses.append(resp)

        attempt = assessment_services.submit_assessment_attempt(
            attempt_id, domain_responses
        )

        self.render_json({'attempt': attempt.to_dict()})


class LearnerCertificatesHandler(
    base.BaseHandler[Dict[str, str], Dict[str, str]]
):
    """Handler for fetching earned certificates for a learner."""

    GET_HANDLER_ERROR_RETURN_TYPE = feconf.HANDLER_TYPE_JSON
    URL_PATH_ARGS_SCHEMAS: Dict[str, str] = {}
    HANDLER_ARGS_SCHEMAS = {'GET': {}}

    @acl_decorators.can_access_learner_dashboard
    def get(self) -> None:
        """Handles GET requests to fetch earned certificates."""
        # The following service method returns successful attempts.
        certificates = assessment_services.get_earned_certificates(self.user_id)

        self.render_json({'certificates': [c.to_dict() for c in certificates]})
