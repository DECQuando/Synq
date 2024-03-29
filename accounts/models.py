from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Create and save user with email
    """
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Django標準のUserをベースにカスタマイズしたUserクラス
    """

    class Meta(object):
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    username_validator = UnicodeUsernameValidator()
    # python3で半角英数のみ許容する場合はASCIIUsernameValidatorを用いる
    # username_validator = ASCIIUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=50,
        help_text=_('全角文字、半角英数字、@/./+/-/_ で50文字以下にしてください。'),
        validators=[username_validator],
    )
    email = models.EmailField(
        _('email address'),
        max_length=255,
        unique=True,
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("ユーザーがこの管理サイトにログインできるかどうかを指定します。"),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "このユーザーをアクティブとして扱うかどうかを指定します。"
            "アカウントを削除する代わりに、これを選択解除してください。"
        ),
    )
    date_joined = models.DateTimeField(
        _("date joined"),
        default=timezone.now,
        help_text=_(
            "ユーザーが登録した日付"
        ),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    # def has_perm(self, perm, obj=None):  # Trueを返して、権限があることを知らせる
    #     return True
    #
    # def has_module_perms(self, app_label):  # Trueを返して、アプリ（App）のモデル（Model）へ接続できるようにする
    #     return True
