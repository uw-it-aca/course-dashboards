from django.conf import settings


def get_coda_admin_group():
    return getattr(settings, "CODA_ADMIN_GROUP",
                   'u_acadev_coda_admins')


def get_coda_override_group():
    return getattr(settings, "CODA_OVERRIDE_GROUP",
                   'u_acadev_coda_admins')
