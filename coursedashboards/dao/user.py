from coursedashboards.models.user import User
from coursedashboards.models.term import Term
from coursedashboards.dao.pws import get_person_of_current_user


def user_from_person(person):
    try:
        user = User.objects.get(uwnetid=person.uwnetid)
        if user.uwregid != person.uwregid:
            user.uwregid = person.uwregid

        user.save()
    except User.DoesNotExist:
        try:
            user = User.objects.get(uwregid=person.uwregid)
            if user.uwnetid != person.uwnetid:
                user.uwnetid = person.uwnetid
                user.email = person.email
                user.save()
        except User.DoesNotExist:
            user = User.objects.create(
                uwnetid=person.uwnetid, uwregid=person.uwregid,
                display_name=person.display_name, email=person.email1)

    return user


def get_current_user():
    return user_from_person(get_person_of_current_user())
