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

"""Jobs that compute stats for certificate assessments."""

from __future__ import annotations

from core.jobs import base_jobs
from core.jobs.io import ndb_io
from core.jobs.transforms import job_result_transforms
from core.jobs.types import job_run_result
from core.platform import models

import apache_beam as beam
from typing import Iterable, Tuple

MYPY = False
if MYPY:  # pragma: no cover
    from mypy_imports import assessment_models

(assessment_models,) = models.Registry.import_models([models.Names.ASSESSMENT])


class ComputeCertificateMasteryStatsJob(base_jobs.JobBase):
    """Job that computes aggregated stats for each certificate offering."""

    def run(self) -> beam.PCollection[job_run_result.JobRunResult]:
        attempts = self.pipeline | 'Get all AssessmentAttemptModels' >> (
            ndb_io.GetModels(assessment_models.AssessmentAttemptModel.get_all())
        )

        stats_models = (
            attempts
            | 'Group by offering ID' >> beam.GroupBy(lambda m: m.offering_id)
            | 'Compute stats' >> beam.ParDo(ComputeStatsDoFn())
        )

        unused_put_stats = (
            stats_models | 'Put stats into datastore' >> ndb_io.PutModels()
        )

        return (
            attempts
            | 'Count attempts'
            >> job_result_transforms.CountObjectsToJobRunResult(
                'ATTEMPTS ANALYZED'
            ),
            stats_models
            | 'Count stats models'
            >> job_result_transforms.CountObjectsToJobRunResult(
                'STATS MODELS UPDATED'
            ),
        ) | 'Flatten results' >> beam.Flatten()


# Here we use MyPy ignore because beam.DoFn is not fully typed
# in the Apache Beam stubs and requires the misc error to be
# suppressed.
class ComputeStatsDoFn(beam.DoFn):  # type: ignore[misc]
    """DoFn to compute stats for a group of attempts."""

    def process(
        self,
        grouping: Tuple[
            str, Iterable[assessment_models.AssessmentAttemptModel]
        ],
    ) -> Iterable[assessment_models.CertificateMasteryStatsModel]:
        offering_id, attempts = grouping
        attempts_list = list(attempts)

        total_attempts = len(attempts_list)
        total_passes = sum(1 for a in attempts_list if a.passed is True)
        scores = [
            a.score_percentage
            for a in attempts_list
            if a.score_percentage is not None
        ]
        average_score = sum(scores) / len(scores) if scores else 0.0

        stats_model = assessment_models.CertificateMasteryStatsModel(
            id=offering_id,
            offering_id=offering_id,
            total_attempts=total_attempts,
            total_passes=total_passes,
            average_score=average_score,
        )
        stats_model.update_timestamps()
        yield stats_model
