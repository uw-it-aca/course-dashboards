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
    if save:
        user.save()

    return user


def _user_from_person(person):
    return User.objects.create(
        uwnetid=person.uwnetid, uwregid=person.uwregid,
        display_name=person.display_name,
        email=_person_email(person),
        is_alum=False if person.is_alum is None else person.is_alum)


def _person_email(person):
    try:
        return person.email_addresses[0]
    except IndexError:
        return '%s@uw.edu' % person.uwnetid


def get_current_user():
    return user_from_person(get_person_of_current_user())
