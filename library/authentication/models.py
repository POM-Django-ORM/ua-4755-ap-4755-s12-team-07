import re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 1)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    """
        This class represents a basic user. \n
        Attributes:
        -----------
        param first_name: Describes first name of the user
        type first_name: str max length=20
        param last_name: Describes last name of the user
        type last_name: str max length=20
        param middle_name: Describes middle name of the user
        type middle_name: str max length=20
        param email: Describes the email of the user
        type email: str, unique, max length=100
        param password: Describes the password of the user
        type password: str
        param created_at: Describes the date when the user was created. Can't be changed.
        type created_at: int (timestamp)
        param updated_at: Describes the date when the user was modified
        type updated_at: int (timestamp)
        param role: user role, default role (0, 'visitor')
        type role: int (choices)
        param is_active: user activation state, default value False
        type is_active: bool
    """
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=20, default=None, null=True, blank=True)
    middle_name = models.CharField(max_length=20, default=None, null=True, blank=True)
    last_name = models.CharField(max_length=20, default=None, null=True, blank=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    role = models.IntegerField(choices=((0, 'visitor'), (1, 'librarian')), default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        """
        Magic method is redefined to show all information about CustomUser.
        :return: user id, user first_name, user middle_name, user last_name,
                 user email, user updated_at, user created_at,
                 user role, user is_active
        """
        created_val = int(self.created_at.timestamp()) if self.created_at else None
        updated_val = int(self.updated_at.timestamp()) if self.updated_at else None
        return (
            f"'id': {self.id}, "
            f"'first_name': '{self.first_name}', "
            f"'middle_name': '{self.middle_name}', "
            f"'last_name': '{self.last_name}', "
            f"'email': '{self.email}', "
            f"'created_at': {created_val}, "
            f"'updated_at': {updated_val}, "
            f"'role': {self.role}, "
            f"'is_active': {self.is_active}"
        )

    def __repr__(self):
        """
        This magic method is redefined to show class and id of CustomUser object.
        :return: class, id
        """
        return f"CustomUser(id={self.id})"

    @staticmethod
    def get_by_id(user_id):
        """
        :param user_id: SERIAL: the id of a user to be found in the DB
        :return: user object or None if a user with such ID does not exist
        """
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def get_by_email(email):
        """
        Returns user by email
        :param email: email by which we need to find the user
        :type email: str
        :return: user object or None if a user with such ID does not exist
        """
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(user_id):
        """
        :param user_id: an id of a user to be deleted
        :type user_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        try:
            user = CustomUser.objects.get(pk=user_id)
            user.delete()
            return True
        except CustomUser.DoesNotExist:
            return False

    @staticmethod
    def create(email, password, first_name=None, middle_name=None, last_name=None):
        """
        :param email: email of a user
        :type email: str
        :param password: password of a user
        :type password: str
        :param first_name: first name of a user
        :type first_name: str
        :param middle_name: middle name of a user
        :type middle_name: str
        :param last_name: last name of a user
        :type last_name: str
        :return: a new user object which is also written into the DB
        """
        try:
            if not email or CustomUser.objects.filter(email=email).exists():
                return None

            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, email):
                return None

            if first_name and len(first_name) > 20:
                return None
            if last_name and len(last_name) > 20:
                return None
            if middle_name and len(middle_name) > 20:
                return None

            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
            )
            return user
        except Exception:
            return None

    def to_dict(self):
        """
        :return: user id, user first_name, user middle_name, user last_name,
                 user email, user updated_at, user created_at, user role, user is_active
        :Example:
        | {
        |   'id': 8,
        |   'first_name': 'fn',
        |   'middle_name': 'mn',
        |   'last_name': 'ln',
        |   'email': 'ln@mail.com',
        |   'created_at': 1509393504,
        |   'updated_at': 1509402866,
        |   'role': 0,
        |   'is_active': True
        | }
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': int(self.created_at.timestamp()) if self.created_at else None,
            'updated_at': int(self.updated_at.timestamp()) if self.updated_at else None,
            'role': self.role,
            'is_active': self.is_active,
        }

    def update(self,
               first_name=None,
               last_name=None,
               middle_name=None,
               password=None,
               role=None,
               is_active=None):
        """
        Updates user profile in the database with the specified parameters.\\n
        :param first_name: first name of a user
        :type first_name: str
        :param last_name: last name of a user
        :type last_name: str
        :param middle_name: middle name of a user
        :type middle_name: str
        :param password: password of a user
        :type password: str
        :param role: role id
        :type role: int
        :param is_active: activation state
        :type is_active: bool
        :return: None
        """
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if middle_name is not None:
            self.middle_name = middle_name
        if role is not None:
            self.role = role
        if is_active is not None:
            self.is_active = is_active
        if password is not None:
            self.set_password(password)
        self.save()

    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all users
        """
        return CustomUser.objects.all()

    def get_role_name(self):
        """
        returns str role name
        """
        if self.role == 1:
            return 'admin'
        return 'visitor'

    def get_full_name(self):
        names = [self.last_name, self.first_name, self.middle_name]
        return " ".join([name for name in names if name])
