from django.contrib.auth.forms import (PasswordResetForm, SetPasswordForm,
                                       UserChangeForm, UserCreationForm)
from django.forms import ModelForm
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from reservation.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма регистрации пользователя."""

    class Meta:
        model = User
        fields = ("email", "first_name", "phone_number", "password1", "password2")

        # Изменяем поля на русский язык
        labels = {
            "password1": "Пароль",
            "password2": "Подтверждение пароля",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # mark_safe позволяет Django интерпретировать HTML-теги
        # <br> чтобы каждая строка переносилась на новую строку в HTML.
        self.fields["password1"].help_text = mark_safe(
            "* Ваш пароль должен содержать как минимум 8 символов.<br>"
            "* Ваш пароль не может быть слишком похож на другую вашу личную информацию.<br>"
            "* Ваш пароль не может быть часто используемым паролем.<br>"
            "* Ваш пароль не может состоять только из цифр."
        )
        self.fields["password2"].help_text = _(
            "Для подтверждения введите, пожалуйста, пароль ещё раз."
        )

        self.fields["password1"].error_messages = {
            "password_too_short": _(
                "Ваш пароль должен содержать как минимум 8 символов."
            ),
            "password_too_similar": _(
                "Ваш пароль не может быть слишком похож на другую вашу личную информацию."
            ),
            "password_too_common": _(
                "Ваш пароль не может быть часто используемым паролем."
            ),
            "password_entirely_numeric": _(
                "Ваш пароль не может состоять только из цифр."
            ),
        }

        # Используем переопределенные поля на русский язык
        for k, v in self.Meta.labels.items():
            self[k].label = v


class UserForm(StyleFormMixin, UserChangeForm):
    """Форма данных пользователя."""

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "phone_number",
            "avatar",
        )


class UserUpdateForm(StyleFormMixin, ModelForm):
    """Форма обновления данных пользователя."""

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "phone_number",
            "avatar",
        )
        success_url = reverse_lazy("users:user_list")


class UserForgotPasswordForm(PasswordResetForm):
    """Форма запроса на восстановление пароля."""

    class Meta:
        labels = {
            "email": "Электронная почта",
        }

    def __init__(self, *args, **kwargs):
        """Обновление стилей формы"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "form-control", "autocomplete": "off"}
            )

        # Используем переопределенные поля на русский язык
        for k, v in self.Meta.labels.items():
            self[k].label = v


class UserSetNewPasswordForm(SetPasswordForm):
    """Форма изменения пароля пользователя после подтверждения."""

    class Meta:
        labels = {
            "new_password1": "Новый пароль",
            "new_password2": "Подтверждение пароля",
        }

    def __init__(self, *args, **kwargs):
        """Обновление стилей формы"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "form-control", "autocomplete": "off"}
            )

            # mark_safe позволяет Django интерпретировать HTML-теги
            # <br> чтобы каждая строка переносилась на новую строку в HTML.
            self.fields["new_password1"].help_text = mark_safe(
                "* Ваш пароль должен содержать как минимум 8 символов.<br>"
                "* Ваш пароль не может быть слишком похож на другую вашу личную информацию.<br>"
                "* Ваш пароль не может быть часто используемым паролем.<br>"
                "* Ваш пароль не может состоять только из цифр."
            )
            self.fields["new_password2"].help_text = _(
                "Для подтверждения введите, пожалуйста, пароль ещё раз."
            )

            self.fields["new_password1"].error_messages = {
                "password_too_short": _(
                    "Ваш пароль должен содержать как минимум 8 символов."
                ),
                "password_too_similar": _(
                    "Ваш пароль не может быть слишком похож на другую вашу личную информацию."
                ),
                "password_too_common": _(
                    "Ваш пароль не может быть часто используемым паролем."
                ),
                "password_entirely_numeric": _(
                    "Ваш пароль не может состоять только из цифр."
                ),
            }

        # Используем переопределенные поля на русский язык
        for k, v in self.Meta.labels.items():
            self[k].label = v