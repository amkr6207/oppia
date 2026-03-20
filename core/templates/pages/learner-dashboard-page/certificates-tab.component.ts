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
 * @fileoverview Component for the certificates tab in the learner dashboard.
 */

import {Component, OnInit} from '@angular/core';
import {
  AssessmentBackendApiService,
  AssessmentAttemptBackendDict,
} from 'domain/assessment/assessment-backend-api.service';
import {UrlInterpolationService} from 'domain/utilities/url-interpolation.service';
import {LoaderService} from 'services/loader.service';

@Component({
  selector: 'oppia-certificates-tab',
  templateUrl: './certificates-tab.component.html',
  styleUrls: ['./certificates-tab.component.css'],
})
export class CertificatesTabComponent implements OnInit {
  certificates: AssessmentAttemptBackendDict[] = [];
  isLoading = true;

  constructor(
    private assessmentBackendApiService: AssessmentBackendApiService,
    private loaderService: LoaderService,
    private urlInterpolationService: UrlInterpolationService
  ) {}

  ngOnInit(): void {
    this.isLoading = true;
    this.assessmentBackendApiService
      .fetchLearnerCertificatesAsync()
      .then(certificates => {
        this.certificates = certificates;
        this.isLoading = false;
      });
  }

  getCertificateImageUrl(): string {
    return this.urlInterpolationService.getStaticImageUrl(
      '/learner_dashboard/certificate_icon.svg'
    );
  }

  formatDate(timestamp: number): string {
    return new Date(timestamp).toLocaleDateString();
  }

  viewCertificate(certificateId: string): void {
    // This opens the certificate preview page in a new tab.
    window.open(`/certificate_viewer/${certificateId}`, '_blank');
  }
}
