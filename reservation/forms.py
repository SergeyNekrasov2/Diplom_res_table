from django import forms
from django.forms import ModelForm

from reservation.models import Reservation, Restaurant


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class RestaurantForm(StyleFormMixin, ModelForm):
    """Форма создания нового ресторана."""

    class Meta:
        model = Restaurant
        fields = "__all__"


class ReservationForm(ModelForm):
    """Форма бронирования столика."""

    class Meta:
        """Стилизация формы бронирования столика."""

        model = Reservation
        fields = ["owner", "table", "reserved_at", "customer_name", "customer_contact"]
        widgets = {
            'owner': forms.HiddenInput(),
            "reserved_at": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Выберите дату и время",
                    "type": "datetime-local",  # для выбора даты и времени
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields["table"].widget.attrs.update({"class": "form-control"})
        self.fields["customer_name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Уточните имя на кого бронируете столик",
            }
        )
        self.fields["customer_contact"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Укажите контактный номер телефона для связи",
            }
        )
        self.fields["owner"].widget.attrs.update({"class": "form-control"})

    # Настройки для формы, если использовать форму отдельно
    # def clean(self):
    #     """Валидация формы, на проверку отсутствия брони выбранного столика."""
    #     cleaned_data = super().clean()
    #     table = cleaned_data.get("table")
    #     reserved_at = cleaned_data.get("reserved_at")
    #
    #     if reserved_at and reserved_at < timezone.now():
    #         raise ValidationError("Выбранное время и дата не могут быть в прошлом.")
    #
    #     if table and reserved_at:
    #         # Определяем начальное и конечное время бронирования
    #         start_time = reserved_at
    #         end_time = reserved_at + timedelta(minutes=60)
    #
    #         # Проверяем, есть ли текущее бронирование на этот столик
    #         if Reservation.objects.filter(
    #                 Q(table=table) &
    #                 Q(reserved_at__lt=end_time) &
    #                 Q(reserved_at__gte=start_time)
    #         ).exists() or Reservation.objects.filter(
    #             Q(table=table) &
    #             Q(reserved_at__gte=start_time) &
    #             Q(reserved_at__lt=end_time)
    #         ).exists():
    #             raise ValidationError(f"Выбранный стол №{table.number} уже забронирован на это время, пожалуйста выберите другое время.")
    #
    #     return cleaned_data
    #
    # def save(self, commit=True):
    #     """Сохранение успешного бронирования."""
    #     reservation = super().save(commit=False)
    #
    #     if commit:
    #         reservation.save()  # Сохраняем в БД
    #     return reservation
