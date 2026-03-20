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

"""Tests for certificate_mastery_jobs.py"""

from __future__ import annotations

from core.jobs import job_test_utils
from core.jobs.batch_jobs import certificate_mastery_jobs
from core.jobs.types import job_run_result
from core.platform import models

from typing import Type

(assessment_models,) = models.Registry.import_models([models.Names.ASSESSMENT])


class ComputeCertificateMasteryStatsJobTest(job_test_utils.JobTestBase):
    """Tests for ComputeCertificateMasteryStatsJob."""

    JOB_CLASS: Type[
        certificate_mastery_jobs.ComputeCertificateMasteryStatsJob
    ] = certificate_mastery_jobs.ComputeCertificateMasteryStatsJob

    def test_empty_storage(self) -> None:
        """Tests that the job runs successfully on an empty datastore."""
        self.assert_job_output_is_empty()

    def test_compute_stats_for_attempts(self) -> None:
        """Tests that the job computes stats correctly."""
        attempt_1 = self.create_model(
            assessment_models.AssessmentAttemptModel,
            id='attempt_1',
            user_id='user_1',
            offering_id='offering_1',
            offering_version=1,
            score_percentage=100.0,
            passed=True,
        )
        attempt_2 = self.create_model(
            assessment_models.AssessmentAttemptModel,
            id='attempt_2',
            user_id='user_2',
            offering_id='offering_1',
            offering_version=1,
            score_percentage=50.0,
            passed=False,
        )
        self.put_multi([attempt_1, attempt_2])

        self.assert_job_output_is(
            [
                job_run_result.JobRunResult.as_stdout('ATTEMPTS ANALYZED: 2'),
                job_run_result.JobRunResult.as_stdout(
                    'STATS MODELS UPDATED: 1'
                ),
            ]
        )

        stats_model = assessment_models.CertificateMasteryStatsModel.get_by_id(
            'offering_1'
        )
        self.assertIsNotNone(stats_model)
        self.assertEqual(stats_model.total_attempts, 2)
        self.assertEqual(stats_model.total_passes, 1)
        self.assertEqual(stats_model.average_score, 75.0)
