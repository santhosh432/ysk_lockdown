# coding=utf-8
"""
Custom middleware

@author : YSK

"""

from django.conf import settings
from django.contrib.auth.models import User

from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from lockdown.models import LockDown
from django.db.utils import IntegrityError
from django.shortcuts import redirect
from django.contrib import messages


class UserLockDown(object):
    """ user lock down for after certain wrong attempts """
    def __init__(self, get_response):
        self.get_response = get_response

        # self.exception = exception
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        check_in_user = auth.authenticate(username=username, password=password)

        try:
            check_in_data = User.objects.get(username=username)
            locked_user = LockDown.check_locked_user(user=check_in_data)
            print('locked_user', locked_user)
        except ObjectDoesNotExist:
            locked_user = {}

        if locked_user.get('status', None) and locked_user.get('expiry', None):
            messages.error(request, 'You have used 5 unsuccessful attempts, please try after {0}'.format(
                locked_user['last_attempt']))
            return redirect('/')

        if not check_in_user and username:
            # print('[info] : User - {0} has not logged in successfully'.format(username))
            try:
                check_in_data = User.objects.get(username=username)

                try:
                    luser = LockDown(lock_user=check_in_data)
                    luser.save()
                    print('[saved]: User - {0}'.format(check_in_data))
                except IntegrityError:
                    luser = LockDown.objects.get(lock_user=check_in_data)
                    luser.save()
                messages.info(request, 'Maximum 5 wrong attempts are valid per day for login')
                messages.info(request, 'Already you used wrong attempts: {0}'.format(luser.attempt))
            except ObjectDoesNotExist:
                print('ObjectDoesNotExist- user- {0}'.format(username))

        else:
            print('[Success] : User - {0} has logged in successfully'.format(username))

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response

