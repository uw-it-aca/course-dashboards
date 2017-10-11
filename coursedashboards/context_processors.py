from django.conf import settings


def is_desktop(request):

    desktopapp = not request.is_mobile and not request.is_tablet

    return {
        'is_desktop': desktopapp
    }
