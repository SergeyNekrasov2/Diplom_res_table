from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Restaurant(models.Model):
    """Модель ресторана."""

    name = models.CharField(
        max_length=20, verbose_name="Название", help_text="Введите название"
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание"
    )
    history = models.TextField(
        verbose_name="История ресторана",
        help_text="Введите описание истории",
        **NULLABLE,
    )
    mission = models.TextField(
        verbose_name="Миссия и ценности",
        help_text="Введите описание миссии и ценностей",
        **NULLABLE,
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        help_text="Укажите владельца",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ресторан"
        verbose_name_plural = "Рестораны"
        ordering = [
            "name",
        ]


class Table(models.Model):
    """Модель стола."""

    number = models.IntegerField(unique=True, verbose_name="Номер стола")
    capacity = models.IntegerField(verbose_name="Вместимость столика")
    is_available = models.BooleanField(default=True, verbose_name="Доступность столика")
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        help_text="Укажите владельца",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f"№ {self.number} (Вместимость: {self.capacity})"


class Reservation(models.Model):
    """Модель бронирования."""

    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, verbose_name="Номер столика")
    reserved_at = models.DateTimeField(verbose_name="Дата бронирования")
    customer_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    customer_contact = models.CharField(max_length=100, verbose_name="Контактная информация")
    owner = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f"Зарезервировано для {self.customer_name} в {self.reserved_at} столик {self.table}"

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = [
            "reserved_at",
        ]