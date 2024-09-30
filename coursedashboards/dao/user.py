# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import uw_pws
from coursedashboards.models.user import User
from coursedashboards.dao.pws import get_person_of_current_user, \
    get_person_by_netid
from coursedashboards.dao.exceptions import MalformedOrInconsistentUser
import logging


logger = logging.getLogger(__name__)


def user_from_person(person):
    if type(person) is not uw_pws.models.Person:
        person = get_person_by_netid(person.uwnetid)

    save = False

    try:
        user = User.objects.get(uwnetid=person.uwnetid)
    except User.DoesNotExist:
        user = None
        if len(person.prior_uwnetids):
            # update model on netid change
            prior = User.objects.filter(uwnetid__in=person.prior_uwnetids)
            n_prior = len(prior)
            if n_prior == 1:
                user = prior[0]
                user.uwnetid = person.uwnetid
                save = True
            elif n_prior > 1:
                raise Exception(
                    f"Need to sort out netid {person.uwnetid} User models")

        if not user:
            return _user_from_person(person)

    if user.uwregid != person.uwregid:
        if user.uwregid in person.prior_uwregids:
            # update model for new regid and clean up any earlier changes
            try:
                regid_user = User.objects.get(uwregid=person.uwregid)
                if user.id == regid_user.id:
                    user.uwregid = person.uwregid
                    save = True
                else:
                    # netid change on top of previous regid change
                    regid_user.uwregid = user.uwregid
                    user.uwregid = 'regid_placeholder'
                    user.save()
                    regid_user.save()
                    user.uwregid = person.uwregid
                    save = True
            except User.DoesNotExist:
                user.uwregid = person.uwregid
                save = True
        else:
            logger.error(
                f"previous regid for {user.uwnetid} ({user.uwregid}) "
                f"not found in person service {person.uwregid}")
            raise MalformedOrInconsistentUser()

    if user.email != _person_email(person):
        user.email = _person_email(person)
        save = True
    if user.preferred_first_name != person.preferred_first_name:
        user.preferred_first_name = person.preferred_first_name
        save = True
    if user.preferred_middle_name != person.preferred_middle_name:
        user.preferred_middle_name = person.preferred_middle_name
        save = True
    if user.preferred_surname != person.preferred_surname:
        user.preferred_surname = person.preferred_surname
        save = True
    if user.is_student != person.is_student:
        user.is_student = person.is_student
        save = True
    if user.is_staff != person.is_staff:
        user.is_staff = person.is_staff
        save = True
    if user.is_employee != person.is_employee:
        user.is_employee = person.is_employee
        save = True
    if user.is_alum != person.is_alum:
        user.is_alum = person.is_alum
        save = True
    if user.is_faculty != person.is_faculty:
        user.is_faculty = person.is_faculty
        save = True

    if save:
        user.save()

    return user


def _user_from_person(person):
    return User.objects.create(
        uwnetid=person.uwnetid, uwregid=person.uwregid,
        display_name=person.display_name,
        preferred_first_name=person.preferred_first_name,
        preferred_middle_name=person.preferred_middle_name,
        preferred_surname=person.preferred_surname,
        email=_person_email(person),
        is_student=False if person.is_student else person.is_student,
        is_staff=False if person.is_staff else person.is_staff,
        is_employee=False if person.is_employee else person.is_employee,
        is_alum=False if person.is_alum is None else person.is_alum,
        is_faculty=False if person.is_faculty else person.is_faculty)


def _person_email(person):
    try:
        return person.email_addresses[0]
    except IndexError:
        return f"{person.uwnetid}@uw.edu"


def get_current_user():
    return user_from_person(get_person_of_current_user())
