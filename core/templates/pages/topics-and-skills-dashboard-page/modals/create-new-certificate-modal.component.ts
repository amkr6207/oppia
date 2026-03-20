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
 * @fileoverview Modal for creating a new certificate offering.
 */

import {Component, OnInit} from '@angular/core';
import {NgbActiveModal} from '@ng-bootstrap/ng-bootstrap';
import {ConfirmOrCancelModal} from 'components/common-layout-directives/common-elements/confirm-or-cancel-modal.component';
import {TopicsAndSkillsDashboardBackendApiService} from 'domain/topics_and_skills_dashboard/topics-and-skills-dashboard-backend-api.service';
import {SkillSummary} from 'domain/skill/skill-summary.model';

@Component({
  selector: 'oppia-create-new-certificate-modal',
  templateUrl: './create-new-certificate-modal.component.html',
})
export class CreateNewCertificateModalComponent
  extends ConfirmOrCancelModal
  implements OnInit
{
  name: string = '';
  description: string = '';
  classrooms: string[] = [];
  selectedClassroomId: string = '';
  allSkills: SkillSummary[] = [];
  selectedSkillIds: string[] = [];
  timeLimit: number = 60;

  constructor(
    private ngbActiveModal: NgbActiveModal,
    private topicsAndSkillsDashboardBackendApiService: TopicsAndSkillsDashboardBackendApiService
  ) {
    super(ngbActiveModal);
  }

  ngOnInit(): void {
    this.topicsAndSkillsDashboardBackendApiService
      .fetchDashboardDataAsync()
      .then(response => {
        this.classrooms = response.allClassroomNames;
        this.allSkills = response.untriagedSkillSummaries;
      });
  }

  save(): void {
    const offeringId =
      'cert_offering_' + Math.random().toString(36).substr(2, 9);
    this.topicsAndSkillsDashboardBackendApiService
      .createCertificateOfferingAsync(
        offeringId,
        this.name,
        this.description,
        this.selectedClassroomId,
        this.selectedSkillIds,
        this.timeLimit
      )
      .then(() => {
        this.ngbActiveModal.close();
      });
  }

  cancel(): void {
    this.ngbActiveModal.dismiss('cancel');
  }

  isValid(): boolean {
    return (
      this.name.length > 0 &&
      this.selectedClassroomId.length > 0 &&
      this.selectedSkillIds.length > 0
    );
  }

  toggleSkill(skillId: string): void {
    const index = this.selectedSkillIds.indexOf(skillId);
    if (index === -1) {
      this.selectedSkillIds.push(skillId);
    } else {
      this.selectedSkillIds.splice(index, 1);
    }
  }
}
