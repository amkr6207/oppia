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
 * @fileoverview Service to send and receive certificate offerings
 * from the backend.
 */

import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';

export interface CertificateOfferingBackendDict {
  id: string;
  name: string;
  description: string;
  classroom_id: string;
  attached_skill_ids: string[];
  time_limit_in_minutes: number;
  version: number;
}

interface FetchOfferingResponse {
  offering: CertificateOfferingBackendDict;
}

interface CreateOfferingResponse {
  offering: CertificateOfferingBackendDict;
}

@Injectable({
  providedIn: 'root',
})
export class CertificateBackendApiService {
  constructor(private http: HttpClient) {}

  async fetchCertificateOfferingAsync(
    offeringId: string
  ): Promise<CertificateOfferingBackendDict> {
    return this.http
      .get<FetchOfferingResponse>('/certificate_offering_handler', {
        params: {offering_id: offeringId},
      })
      .toPromise()
      .then(response => {
        // This throws "Object is possibly undefined". We need to suppress
        // this error because toPromise() returns T | undefined but the
        // server always returns the expected response type.
        // @ts-ignore
        return response.offering;
      });
  }

  async createCertificateOfferingAsync(
    offeringId: string,
    name: string,
    description: string,
    classroomId: string,
    attachedSkillIds: string[],
    timeLimitInMinutes: number
  ): Promise<CertificateOfferingBackendDict> {
    const payload = {
      offering_id: offeringId,
      name: name,
      description: description,
      classroom_id: classroomId,
      attached_skill_ids: attachedSkillIds,
      time_limit_in_minutes: timeLimitInMinutes,
    };
    return this.http
      .post<CreateOfferingResponse>('/certificate_offering_handler', payload)
      .toPromise()
      .then(response => {
        // This throws "Object is possibly undefined". We need to suppress
        // this error because toPromise() returns T | undefined but the
        // server always returns the expected response type.
        // @ts-ignore
        return response.offering;
      });
  }
}
