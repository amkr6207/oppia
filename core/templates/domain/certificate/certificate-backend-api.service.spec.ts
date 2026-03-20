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
 * @fileoverview Unit tests for CertificateBackendApiService.
 */

import {
  HttpClientTestingModule,
  HttpTestingController,
} from '@angular/common/http/testing';
import {TestBed, fakeAsync, flushMicrotasks} from '@angular/core/testing';

import {CertificateBackendApiService} from './certificate-backend-api.service';

describe('CertificateBackendApiService', () => {
  let certificateBackendApiService: CertificateBackendApiService;
  let httpTestingController: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [CertificateBackendApiService],
    });
    certificateBackendApiService = TestBed.inject(CertificateBackendApiService);
    httpTestingController = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpTestingController.verify();
  });

  it('should fetch an offering', fakeAsync(() => {
    const sampleOffering = {
      id: 'off_1',
      name: 'Name',
      description: 'Desc',
      classroom_id: 'class_1',
      attached_skill_ids: ['s_1'],
      time_limit_in_minutes: 60,
      version: 1,
    };

    certificateBackendApiService
      .fetchCertificateOfferingAsync('off_1')
      .then(response => {
        expect(response).toEqual(sampleOffering);
      });

    const req = httpTestingController.expectOne(
      '/certificate_offering_handler?offering_id=off_1'
    );
    expect(req.request.method).toEqual('GET');
    req.flush({offering: sampleOffering});

    flushMicrotasks();
  }));

  it('should create an offering', fakeAsync(() => {
    const sampleOffering = {
      id: 'off_1',
      name: 'Name',
      description: 'Desc',
      classroom_id: 'class_1',
      attached_skill_ids: ['s_1'],
      time_limit_in_minutes: 60,
      version: 1,
    };

    certificateBackendApiService
      .createCertificateOfferingAsync(
        'off_1',
        'Name',
        'Desc',
        'class_1',
        ['s_1'],
        60
      )
      .then(response => {
        expect(response).toEqual(sampleOffering);
      });

    const req = httpTestingController.expectOne(
      '/certificate_offering_handler'
    );
    expect(req.request.method).toEqual('POST');
    req.flush({offering: sampleOffering});

    flushMicrotasks();
  }));
});
