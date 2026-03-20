// Copyright 2025 The Oppia Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS-IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * @fileoverview Service to start and submit learner assessments.
 */

import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';

export interface AssessmentAttemptBackendDict {
  id: string;
  user_id: string;
  offering_id: string;
  offering_version: number;
  start_time: string;
  end_time: string | null;
  passed: boolean | null;
  score_percentage: number | null;
}

export interface QuestionBackendDict {
  question_dict: Object;
  skill_id: string;
  skill_difficulty: number;
}

export interface AssessmentQuestionResponseBackendDict {
  id: string;
  question_id: string;
  question_version: number;
  skill_id: string;
  skill_version: number;
  learner_answer_html: string;
  is_correct: boolean;
}

interface StartAttemptResponse {
  attempt: AssessmentAttemptBackendDict;
  questions: QuestionBackendDict[];
}

interface SubmitAttemptResponse {
  attempt: AssessmentAttemptBackendDict;
}

interface LearnerCertificatesResponse {
  certificates: AssessmentAttemptBackendDict[];
}

@Injectable({
  providedIn: 'root',
})
export class AssessmentBackendApiService {
  constructor(private http: HttpClient) {}

  async startAssessmentAttemptAsync(
    offeringId: string
  ): Promise<StartAttemptResponse> {
    return this.http
      .post<StartAttemptResponse>('/assessment_attempt_handler', {
        offering_id: offeringId,
      })
      .toPromise()
      .then(response => {
        // This throws "Object is possibly undefined". We need to suppress
        // this error because toPromise() returns T | undefined but the
        // server always returns the expected response type.
        // @ts-ignore
        return response;
      });
  }

  async submitAssessmentAttemptAsync(
    attemptId: string,
    responses: AssessmentQuestionResponseBackendDict[]
  ): Promise<SubmitAttemptResponse> {
    return this.http
      .post<SubmitAttemptResponse>('/assessment_submit_handler', {
        attempt_id: attemptId,
        responses: responses,
      })
      .toPromise()
      .then(response => {
        // This throws "Object is possibly undefined". We need to suppress
        // this error because toPromise() returns T | undefined but the
        // server always returns the expected response type.
        // @ts-ignore
        return response;
      });
  }

  async fetchLearnerCertificatesAsync(): Promise<
    AssessmentAttemptBackendDict[]
  > {
    return this.http
      .get<LearnerCertificatesResponse>('/learner_certificates_handler')
      .toPromise()
      .then(response => {
        // This throws "Object is possibly undefined". We need to suppress
        // this error because toPromise() returns T | undefined but the
        // server always returns the expected response type.
        // @ts-ignore
        return response.certificates;
      });
  }
}
