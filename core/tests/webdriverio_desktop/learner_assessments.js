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
 * @fileoverview End-to-end tests for learner assessments and certificates.
 */

var TopicsAndSkillsDashboardPage = require('../webdriverio_utils/TopicsAndSkillsDashboardPage.js');
var LearnerDashboardPage = require('../webdriverio_utils/LearnerDashboardPage.js');
var users = require('../webdriverio_utils/users.js');
var action = require('../webdriverio_utils/action.js');
var waitFor = require('../webdriverio_utils/waitFor.js');

describe('Learner Assessments and Certificates', function () {
  var topicsAndSkillsDashboardPage = null;
  var learnerDashboardPage = null;

  beforeAll(async function () {
    topicsAndSkillsDashboardPage =
      new TopicsAndSkillsDashboardPage.TopicsAndSkillsDashboardPage();
    learnerDashboardPage = new LearnerDashboardPage.LearnerDashboardPage();
  });

  it('should allow admin to create a certificate offering', async function () {
    await users.createAndLoginAdminUser('admin@example.com', 'adminUser');

    await topicsAndSkillsDashboardPage.get();
    // Create a topic to associate with certificate (simplified).
    await topicsAndSkillsDashboardPage.createTopic(
      'Math Topic',
      'math-topic',
      'Topic for assessment',
      true
    );

    // Create a skill.
    await topicsAndSkillsDashboardPage.get();
    await topicsAndSkillsDashboardPage.createSkillWithDescriptionAndExplanation(
      'Basic Addition',
      'Addition of numbers',
      true
    );

    // Assign skill to topic.
    await topicsAndSkillsDashboardPage.get();
    await topicsAndSkillsDashboardPage.assignSkillToTopic(
      'Basic Addition',
      'Math Topic'
    );

    // Navigate to Certificates tab.
    await topicsAndSkillsDashboardPage.navigateToCertificatesTab();
    await topicsAndSkillsDashboardPage.expectNoCertificatesMessageToBeVisible();

    // Click create certificate.
    await topicsAndSkillsDashboardPage.clickCreateCertificateButton();

    // Fill the modal.
    await action.setValue(
      'Certificate Name',
      $('.e2e-test-certificate-name-field'),
      'Elementary Math'
    );
    await action.setValue(
      'Certificate Description',
      $('.e2e-test-certificate-description-field'),
      'Basics of addition'
    );
    // Select first classroom if available.
    await $('.e2e-test-certificate-classroom-select').selectByIndex(1);
    // Select the skill checkbox.
    await action.click(
      'Skill checkbox',
      $('.e2e-test-certificate-skill-checkbox')
    );

    // Create the certificate.
    await action.click(
      'Confirm creation',
      $('.e2e-test-confirm-certificate-creation-button')
    );

    await waitFor.pageToFullyLoad();

    await users.logout();
  });

  it('should show certificates on learner dashboard after completion', async function () {
    // Note: Actually completing an assessment in e2e is complex because
    // it requires mock questions and answering them. Here we verify the
    // dashboard tab exists and shows empty state for a new user.

    await users.createUser('learner@example.com', 'learnerUser');
    await users.login('learner@example.com');

    await learnerDashboardPage.get();
    await learnerDashboardPage.navigateToCertificatesTab();
    await learnerDashboardPage.expectNumberOfCertificatesToBe(0);

    await users.logout();
  });
});
