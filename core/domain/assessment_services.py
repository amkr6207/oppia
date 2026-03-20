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

"""Commands that can be used to operate on learner assessment attempts
and responses.
"""

from __future__ import annotations

import datetime
import math
import random

from core.constants import constants
from core.domain import (
    assessment_domain,
    certificate_services,
    question_fetchers,
)
from core.platform import models

# Here we use type Any because the function returns a list of
# dictionaries that contain mixed types of values (question dicts,
# skill IDs, and difficulty floats).
from typing import List, Optional, cast

MYPY = False
if MYPY:  # pragma: no cover
    from mypy_imports import assessment_models, question_models

(assessment_models, question_models) = models.Registry.import_models(
    [models.Names.ASSESSMENT, models.Names.QUESTION]
)

# Hard limit for max questions.
MAX_CERTIFICATE_ASSESSMENT_QUESTIONS = 50

# Ratios mandated by PRD.
EASY_RATIO = 0.3
MODERATE_RATIO = 0.4
HARD_RATIO = 0.3
PASSING_THRESHOLD = 0.8


def _get_assessment_attempt_from_model(
    attempt_model: assessment_models.AssessmentAttemptModel,
) -> assessment_domain.AssessmentAttempt:
    """Returns an AssessmentAttempt domain object from a model."""
    return assessment_domain.AssessmentAttempt(
        attempt_model.id,
        attempt_model.user_id,
        attempt_model.offering_id,
        attempt_model.offering_version,
        attempt_model.start_time,
        attempt_model.end_time,
        attempt_model.passed,
        attempt_model.score_percentage,
    )


def _get_assessment_question_response_from_model(
    response_model: assessment_models.AssessmentQuestionResponseModel,
) -> assessment_domain.AssessmentQuestionResponse:
    """Returns an AssessmentQuestionResponse domain object from a model."""
    return assessment_domain.AssessmentQuestionResponse(
        response_model.id,
        response_model.attempt_id,
        response_model.user_id,
        response_model.question_id,
        response_model.question_version,
        response_model.skill_id,
        response_model.skill_version,
        response_model.learner_answer_html,
        response_model.is_correct,
    )


def get_assessment_attempt_by_id(
    attempt_id: str, strict: bool = True
) -> Optional[assessment_domain.AssessmentAttempt]:
    """Returns a domain object representing an assessment attempt."""
    attempt_model = assessment_models.AssessmentAttemptModel.get(
        attempt_id, strict=strict
    )
    if attempt_model:
        return _get_assessment_attempt_from_model(attempt_model)
    return None


def fetch_questions_for_certificate(
    offering_id: str,
) -> List[assessment_domain.QuestionWithMetadataDict]:
    """Retrieves precisely balanced questions for a given certificate
    offering.

    Args:
        offering_id: str. The offering ID.

    Returns:
        list(dict). A list of question dictionaries with difficulty mapped.

    Raises:
        Exception. Certificate offering not found.
    """
    offering = certificate_services.get_certificate_assessment_offering_by_id(
        offering_id
    )
    if not offering:
        raise Exception('Certificate offering not found.')

    skill_ids = offering.attached_skill_ids
    # Arbitrary limit 50 as per PRD.
    total_questions = min(
        MAX_CERTIFICATE_ASSESSMENT_QUESTIONS, len(skill_ids) * 5
    )

    num_easy = math.ceil(total_questions * EASY_RATIO)
    num_hard = math.ceil(total_questions * HARD_RATIO)
    num_mod = total_questions - num_easy - num_hard

    easy_links = question_models.QuestionSkillLinkModel.get_question_skill_links_based_on_difficulty_equidistributed_by_skill(
        num_easy,
        skill_ids,
        constants.SKILL_DIFFICULTY_LABEL_TO_FLOAT[
            constants.SKILL_DIFFICULTY_EASY
        ],
    )
    mod_links = question_models.QuestionSkillLinkModel.get_question_skill_links_based_on_difficulty_equidistributed_by_skill(
        num_mod,
        skill_ids,
        constants.SKILL_DIFFICULTY_LABEL_TO_FLOAT[
            constants.SKILL_DIFFICULTY_MEDIUM
        ],
    )
    hard_links = question_models.QuestionSkillLinkModel.get_question_skill_links_based_on_difficulty_equidistributed_by_skill(
        num_hard,
        skill_ids,
        constants.SKILL_DIFFICULTY_LABEL_TO_FLOAT[
            constants.SKILL_DIFFICULTY_HARD
        ],
    )

    all_links = easy_links + mod_links + hard_links
    random.shuffle(all_links)

    question_ids = [link.question_id for link in all_links]
    questions = question_fetchers.get_questions_by_ids(question_ids)

    result = []
    for index, q in enumerate(questions):
        if q is not None:
            # Here we use cast because the underlying to_dict() method
            # returns a broad QuestionDict, which we need to treat as
            # QuestionWithMetadataDict for adding metadata fields.
            question_dict = cast(
                assessment_domain.QuestionWithMetadataDict, q.to_dict()
            )
            question_dict['skill_id'] = all_links[index].skill_id
            question_dict['skill_difficulty'] = all_links[
                index
            ].skill_difficulty
            result.append(question_dict)

    return result


def start_assessment_attempt(
    user_id: str, offering_id: str
) -> assessment_domain.AssessmentAttempt:
    """Starts a new assessment attempt."""
    offering = certificate_services.get_certificate_assessment_offering_by_id(
        offering_id
    )
    if not offering:
        raise Exception('Certificate offering not found.')

    attempt_id = assessment_models.AssessmentAttemptModel.get_new_id('')
    model = assessment_models.AssessmentAttemptModel.create(
        attempt_id=attempt_id,
        user_id=user_id,
        offering_id=offering_id,
        offering_version=offering.version,
        start_time=datetime.datetime.utcnow(),
    )
    return _get_assessment_attempt_from_model(model)


def submit_assessment_attempt(
    attempt_id: str,
    responses: List[assessment_domain.AssessmentQuestionResponse],
) -> assessment_domain.AssessmentAttempt:
    """Submits the attempt with responses."""
    attempt = get_assessment_attempt_by_id(attempt_id)
    if not attempt:
        raise Exception('Attempt not found')
    if attempt.end_time is not None:
        raise Exception('Attempt already submitted')

    # Grade it properly.
    num_correct = sum(1 for r in responses if r.is_correct)
    total = len(responses)
    score = (float(num_correct) / total * 100) if total > 0 else 0.0

    attempt_model = assessment_models.AssessmentAttemptModel.get(attempt_id)
    attempt_model.end_time = datetime.datetime.utcnow()
    attempt_model.score_percentage = score
    attempt_model.passed = score >= (PASSING_THRESHOLD * 100)
    attempt_model.update_timestamps()
    attempt_model.put()

    # Save responses.
    for r in responses:
        r.validate()
        assessment_models.AssessmentQuestionResponseModel.create(
            r.id,
            r.attempt_id,
            r.user_id,
            r.question_id,
            r.question_version,
            r.skill_id,
            r.skill_version,
            r.learner_answer_html,
            r.is_correct,
        )

    return _get_assessment_attempt_from_model(attempt_model)


def get_earned_certificates(
    user_id: str,
) -> List[assessment_domain.AssessmentAttempt]:
    """Returns all successful assessment attempts for a user."""
    # Here we use cast because Mypy is unable to infer the correct type
    # for datastore query results.
    attempt_models = cast(
        List[assessment_models.AssessmentAttemptModel],
        assessment_models.AssessmentAttemptModel.query(
            assessment_models.AssessmentAttemptModel.user_id == user_id,
            assessment_models.AssessmentAttemptModel.passed,
        ).fetch(),
    )
    certificates = []
    for model in attempt_models:
        offering = (
            certificate_services.get_certificate_assessment_offering_by_id(
                model.offering_id
            )
        )
        offering_name = offering.name if offering else 'Mathematics Certificate'
        certificates.append(
            assessment_domain.AssessmentAttempt(
                model.id,
                model.user_id,
                model.offering_id,
                model.offering_version,
                model.start_time,
                model.end_time,
                model.passed,
                model.score_percentage,
                offering_name=offering_name,
            )
        )
    return certificates
