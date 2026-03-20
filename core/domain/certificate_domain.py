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

"""Domain models for certificate assessment offerings."""

from __future__ import annotations

import datetime

from core import utils

from typing import List, TypedDict


class UserCertificateDict(TypedDict):
    """Dict representation of a user certificate."""

    id: str
    user_id: str
    offering_id: str
    offering_version: int
    earned_time: float


class CertificateOfferingDict(TypedDict):
    """Dict representation of a certificate offering."""

    id: str
    name: str
    description: str
    classroom_id: str
    attached_skill_ids: List[str]
    time_limit_in_minutes: int
    version: int


class CertificateAssessmentOffering:
    """Domain object for a certificate assessment offering."""

    def __init__(
        self,
        offering_id: str,
        name: str,
        description: str,
        classroom_id: str,
        attached_skill_ids: List[str],
        time_limit_in_minutes: int,
        version: int,
    ) -> None:
        """Initializes a CertificateAssessmentOffering domain object.

        Args:
            offering_id: str. The unique ID of the offering.
            name: str. The name of the offering.
            description: str. The description.
            classroom_id: str. The classroom ID it belongs to.
            attached_skill_ids: list(str). The skills covered.
            time_limit_in_minutes: int. The time limit.
            version: int. The version of the offering.
        """
        self.id = offering_id
        self.name = name
        self.description = description
        self.classroom_id = classroom_id
        self.attached_skill_ids = attached_skill_ids
        self.time_limit_in_minutes = time_limit_in_minutes
        self.version = version

    def validate(self) -> None:
        """Validates the properties of the offering."""
        if not isinstance(self.id, str):
            raise utils.ValidationError('Expected ID to be a string')
        if not isinstance(self.name, str) or not self.name:
            raise utils.ValidationError('Name cannot be empty')
        if not isinstance(self.description, str):
            raise utils.ValidationError('Description must be a string')
        if not isinstance(self.classroom_id, str) or not self.classroom_id:
            raise utils.ValidationError('Classroom ID cannot be empty')
        if not isinstance(self.attached_skill_ids, list):
            raise utils.ValidationError('Attached skill IDs must be a list')
        if len(self.attached_skill_ids) == 0:
            raise utils.ValidationError('Attached skill IDs cannot be empty')
        for skill_id in self.attached_skill_ids:
            if not isinstance(skill_id, str):
                raise utils.ValidationError(
                    'Expected each skill ID to be a string'
                )
        if not isinstance(self.time_limit_in_minutes, int):
            raise utils.ValidationError('Time limit must be an integer')
        if self.time_limit_in_minutes <= 0:
            raise utils.ValidationError('Time limit must be positive')
        if not isinstance(self.version, int):
            raise utils.ValidationError('Version must be an integer')

    def to_dict(self) -> CertificateOfferingDict:
        """Returns a dict representation of the offering."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'classroom_id': self.classroom_id,
            'attached_skill_ids': self.attached_skill_ids,
            'time_limit_in_minutes': self.time_limit_in_minutes,
            'version': self.version,
        }


class UserCertificate:
    """Domain object for a user certificate."""

    def __init__(
        self,
        certificate_id: str,
        user_id: str,
        offering_id: str,
        offering_version: int,
        earned_time: datetime.datetime,
    ) -> None:
        """Initializes a UserCertificate domain object."""
        self.id = certificate_id
        self.user_id = user_id
        self.offering_id = offering_id
        self.offering_version = offering_version
        self.earned_time = earned_time

    def to_dict(self) -> UserCertificateDict:
        """Returns a dict representation of the certificate."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'offering_id': self.offering_id,
            'offering_version': self.offering_version,
            'earned_time': utils.get_time_in_millisecs(self.earned_time),
        }
