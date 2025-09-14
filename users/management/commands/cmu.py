from django.core.management import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        moder_group = Group.objects.create(name='moder')
        view_mailing = Permission.objects.get(codename='view_mailing')
        view_messages = Permission.objects.get(codename='view_message')
        view_users = Permission.objects.get(codename='list_user')
        blocking_users = Permission.objects.get(codename='blocking_user')
        blocking_mailing = Permission.objects.get(codename='block_mailing')

        moder_group.permissions.add(view_mailing, view_users, blocking_users, blocking_mailing, view_messages)

        user = User.objects.create(email='moder@test.ru')
        user.set_password('1111')
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.save()

        user.groups.add(moder_group)