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

"""Controller for the certificate viewer page."""

from __future__ import annotations

from core.controllers import acl_decorators, base
from core.domain import assessment_services, certificate_services

from typing import Dict


class CertificateViewerPage(base.BaseHandler[Dict[str, str], Dict[str, str]]):
    """Page that displays a certificate for a successful assessment."""

    URL_PATH_ARGS_SCHEMAS = {'attempt_id': {'schema': {'type': 'unicode'}}}
    HANDLER_ARGS_SCHEMAS = {'GET': {}}

    @acl_decorators.open_access
    def get(self, attempt_id: str) -> None:
        """Handles GET requests for the certificate viewer page."""
        attempt = assessment_services.get_assessment_attempt_by_id(
            attempt_id, strict=False
        )
        if not attempt or not attempt.passed:
            raise self.PageNotFoundException(
                'Certificate not found or not earned.'
            )

        offering = (
            certificate_services.get_certificate_assessment_offering_by_id(
                attempt.offering_id, strict=False
            )
        )

        self.values.update(
            {
                'certificate_name': (
                    offering.name if offering else 'Mathematics Mastery'
                ),
                'learner_name': self.username if self.username else 'Learner',
                'date_earned': attempt.end_time.strftime('%B %d, %Y'),
                'score': attempt.score_percentage,
            }
        )

        self.render_template('certificate-viewer-page.mainpage.html')
