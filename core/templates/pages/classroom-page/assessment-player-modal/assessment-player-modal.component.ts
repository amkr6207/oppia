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
 * @fileoverview Component for the assessment player modal.
 */

import {Component, Input, OnInit} from '@angular/core';
import {NgbActiveModal} from '@ng-bootstrap/ng-bootstrap';
import {
  AssessmentBackendApiService,
  QuestionBackendDict,
  AssessmentQuestionResponseBackendDict,
  AssessmentAttemptBackendDict,
} from 'domain/assessment/assessment-backend-api.service';
import {AlertsService} from 'services/alerts.service';

@Component({
  selector: 'oppia-assessment-player-modal',
  templateUrl: './assessment-player-modal.component.html',
  styleUrls: ['./assessment-player-modal.component.css'],
})
export class AssessmentPlayerModalComponent implements OnInit {
  @Input() certificateOfferingId!: string;
  @Input() certificateName!: string;

  questions: QuestionBackendDict[] = [];
  attempt!: AssessmentAttemptBackendDict;
  currentQuestionIndex: number = 0;

  // Store simple responses mapped by question ID for now.
  userResponses: {[questionId: string]: AssessmentQuestionResponseBackendDict} =
    {};

  isLoading: boolean = true;
  isSubmitting: boolean = false;

  constructor(
    private activeModal: NgbActiveModal,
    private assessmentBackendApiService: AssessmentBackendApiService,
    private alertsService: AlertsService
  ) {}

  ngOnInit(): void {
    this.assessmentBackendApiService
      .startAssessmentAttemptAsync(this.certificateOfferingId)
      .then(response => {
        this.attempt = response.attempt;
        this.questions = response.questions;
        this.isLoading = false;
      })
      .catch(error => {
        this.alertsService.addWarning('Failed to start assessment: ' + error);
        this.closeModal();
      });
  }

  getCurrentQuestion(): QuestionBackendDict | null {
    if (this.questions.length === 0) {
      return null;
    }
    return this.questions[this.currentQuestionIndex];
  }

  nextQuestion(): void {
    if (this.currentQuestionIndex < this.questions.length - 1) {
      this.currentQuestionIndex++;
    }
  }

  previousQuestion(): void {
    if (this.currentQuestionIndex > 0) {
      this.currentQuestionIndex--;
    }
  }

  submitAssessment(): void {
    this.isSubmitting = true;

    // Construct the list of responses.
    const responses: AssessmentQuestionResponseBackendDict[] = Object.values(
      this.userResponses
    );

    this.assessmentBackendApiService
      .submitAssessmentAttemptAsync(this.attempt.id, responses)
      .then(response => {
        this.isSubmitting = false;
        this.activeModal.close({
          passed: response.attempt.passed,
          scorePercentage: response.attempt.score_percentage,
        });
      })
      .catch(error => {
        this.isSubmitting = false;
        this.alertsService.addWarning('Failed to submit assessment: ' + error);
      });
  }

  closeModal(): void {
    this.activeModal.dismiss();
  }
}
