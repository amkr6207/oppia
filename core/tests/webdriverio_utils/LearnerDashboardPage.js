// Copyright 2022 The Oppia Authors. All Rights Reserved.
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
 * @fileoverview Page object for the learner dashboard, for use in WebdriverIO
 * tests.
 */

var waitFor = require('./waitFor.js');

var LearnerDashboardPage = function () {
  var LEARNER_DASHBOARD_URL = '/learner-dashboard';
  var subscriptionSection = $('.e2e-test-subscriptions-section');

  var subscriptionNameElement = $('.e2e-test-subscription-name');
  var subscriptionNameSelector = function () {
    return $$('.e2e-test-subscription-name');
  };

  var certificatesTab = $('.e2e-test-certificates-tab');
  var certificateCard = $('.e2e-test-certificate-card');
  var certificateCardsSelector = function () {
    return $$('.e2e-test-certificate-card');
  };
  var noCertificatesMessage = $('.e2e-test-no-certificates-message');

  this.get = async function () {
    await browser.url(LEARNER_DASHBOARD_URL);
    await waitFor.pageToFullyLoad();
  };

  this.navigateToCertificatesTab = async function () {
    await action.click('Certificates tab', certificatesTab);
    await waitFor.pageToFullyLoad();
  };

  this.expectNumberOfCertificatesToBe = async function (count) {
    if (count === 0) {
      await waitFor.visibilityOf(
        noCertificatesMessage,
        'No certificates message taking too long to appear'
      );
      return;
    }
    await waitFor.visibilityOf(
      certificateCard,
      'Certificate cards taking too long to appear'
    );
    var cards = await certificateCardsSelector();
    expect(cards.length).toEqual(count);
  };

  this.expectSubscriptionFirstNameToMatch = async function (name) {
    await waitFor.visibilityOf(
      subscriptionSection,
      'Subscription section takes too long to appear'
    );
    await subscriptionSection.scrollIntoView();
    await waitFor.visibilityOf(
      subscriptionNameElement,
      'Subscription First Name takes too long to appear'
    );
    var subscriptionName = await subscriptionNameSelector();
    expect(await subscriptionName[0].getText()).toMatch(name);
  };

  this.expectSubscriptionLastNameToMatch = async function (name) {
    var subscriptionName = await subscriptionNameSelector();
    var lastElement = subscriptionName.length - 1;
    await waitFor.visibilityOf(
      subscriptionName[lastElement],
      'Subscription Last Name takes too long to appear'
    );
    expect(await subscriptionName[lastElement].getText()).toMatch(name);
  };
};

exports.LearnerDashboardPage = LearnerDashboardPage;
