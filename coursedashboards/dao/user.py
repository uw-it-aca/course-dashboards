from coursedashboards.models.user import User
from coursedashboards.models.term import Term
from coursedashboards.dao.pws import get_person_of_current_user


def user_from_person(person):
    try:
        user = User.objects.get(uwnetid=person.uwnetid)
    except User.DoesNotExist:
        try:
            user = User.objects.get(uwregid=person.uwregid)
        except User.DoesNotExist:
            return User.objects.create(
                uwnetid=person.uwnetid, uwregid=person.uwregid,
                display_name=person.display_name,
                email=_person_email(person))

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


def _person_email(person):
    try:                        # PWS person
        email = person.email1
    except AttributeError:
        email = person.email    # SWS person

    return email if email else '%s@uw.edu' % person.uwnetid


def get_current_user():
    return user_from_person(get_person_of_current_user())
