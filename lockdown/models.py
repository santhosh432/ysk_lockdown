from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.


class LockDown(models.Model):
    """ Lock user after 3 unsuccessful failure  attempts """
    lock_user = models.OneToOneField(User, help_text='Locked user', related_name='lockdownuser')
    attempt = models.PositiveSmallIntegerField(default=0)
    status = models.BooleanField(default=False)
    last_attempt = models.DateTimeField(auto_now=True)  # creates new date after every modification

    def __str__(self):
        return self.lock_user.username

    def is_locked(self):
        """ Check weather locked user or not
            Locked user: True,
            Not Locked user: False
        """
        if self.status:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        if self.attempt == 5:
            self.status = True
        else:
            self.attempt += 1
        return super(LockDown, self).save(*args, **kwargs)

    @classmethod
    def check_locked_user(cls, user):
        """ Check for locked user or not
        input: user orm object
        output: {'status':False, 'expiry':None, 'last_attempt':None}
        status: is_locked or not
        expiry: expiry date
        last_attempt: last attempted date
        """
        try:
            u = cls.objects.get(lock_user=user, status=True)
            last_attempt = timezone.localtime(u.last_attempt + timezone.timedelta(days=1))
            print('Now:', timezone.localtime(timezone.now()), 'Last Attempt',timezone.localtime(u.last_attempt))

            now = timezone.localtime(timezone.now())
            one_day = last_attempt
            expiry = one_day > now
            print('expiry', expiry)
            if not expiry:
                u.attempt = 0
                u.status = False
                u.save()
            return {'status':u.status, 'expiry': expiry, 'last_attempt':last_attempt.strftime("%Y-%m-%d %H:%M:%S")}
        except ObjectDoesNotExist:
            return {'status':False, 'expiry':None, 'last_attempt':None}
