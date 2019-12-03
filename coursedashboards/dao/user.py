import uw_pws
from coursedashboards.models.user import User
from coursedashboards.dao.pws import get_person_of_current_user, \
    get_person_by_netid


def user_from_person(person):
    if type(person) is not uw_pws.models.Person:
        person = get_person_by_netid(person.uwnetid)

    try:
        user = User.objects.get(uwnetid=person.uwnetid)
    except User.DoesNotExist:
        try:
            user = User.objects.get(uwregid=person.uwregid)
        except User.DoesNotExist:
            return _user_from_person(person)

    save = False
    if user.uwnetid != person.uwnetid:
        user.uwnetid = person.uwnetid
        save = True
    if user.uwregid != person.uwregid:
        user.uwregid = person.uwregid
        save = True
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
        return '{}@uw.edu'.format(person.uwnetid)


def get_current_user():
    return user_from_person(get_person_of_current_user())
