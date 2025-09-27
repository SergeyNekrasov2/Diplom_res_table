from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated

from reservation.forms import ReservationForm
from reservation.models import Reservation, Restaurant


def home(request):
    """Основной шаблон."""
    return render(request, "home.html")


class Contacts(TemplateView):
    """Cтраница контакты."""

    template_name = "reservation/contacts.html"

    def post(self, request, *args, **kwargs):
        """Обработка POST-запроса ответа на обратную связь."""
        if request.method == "POST":
            name = request.POST.get("name")  # получаем имя
            # message = request.POST.get("message")  # получаем сообщение
            # Отправляем сообщение об успешной отправке
            messages.success(request, f"Спасибо, {name}! Ваше сообщение успешно отправлено.")
            return redirect("reservation:contacts")  # Перенаправляем на ту же страницу
        return render(request, self.template_name)


class Feedback(TemplateView):
    """Cтраница обратной связи."""

    template_name = "reservation/feedback.html"


class MainView(TemplateView):
    """Главная страница."""

    model = Restaurant
    template_name = "reservation/main.html"


class AboutView(TemplateView):
    """Страница о ресторане."""

    model = Restaurant
    template_name = "reservation/about.html"


class ReservationListView(LoginRequiredMixin,ListView):
    """Страница бронирования."""

    model = Reservation
    template_name = "reservation/reservation_list.html"
    context_object_name = "reservation"
    success_url = reverse_lazy("reservation:reservation_list")
    form_class = ReservationForm


    def get_object(self, queryset=None):
        """Получение одного объекта."""
        self.object = super().get_object(queryset)
        self.object.save()
        if self.request.user == self.object.owner:
            self.object.save()
            return self.object
        raise PermissionRequiredMixin

    def get_context_data(self, **kwargs):
        """Добавление данных в контекст шаблона."""
        context = super().get_context_data(**kwargs)
        context["form"] = ReservationForm()
        return context

    def post(self, request, *args, **kwargs):
        """Обработка POST-запроса."""
        form = self.form_class(request.POST)

        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.owner = request.user
            reservation.save()

            # Проверка, находится ли время бронирования в прошлом
            if reservation.reserved_at and reservation.reserved_at < timezone.now():
                messages.error(
                    request,
                    "Дата бронирования не может быть в прошлом. Пожалуйста, выберите другое время.",
                )
                return self.get(request, *args, **kwargs)  # Возврат на ту же страницу

            # Проверка интервала бронирования (60 минут после)
            reserved_at = reservation.reserved_at
            start_time = reserved_at - timedelta(minutes=60)
            end_time = reserved_at


            # Проверка, есть ли уже бронирования в этом интервале
            interval_reservation = Reservation.objects.filter(reserved_at__range=(start_time, end_time)).exclude(
                id=reservation.id
            )  # Исключаем текущее бронирование, если оно уже существует

            if interval_reservation.exists():
                messages.error(
                    request,
                    "К сожалению, на это время уже занято. Выберите другой стол или дату.",
                )
                return self.get(request, *args, **kwargs)  # Возврат на ту же страницу

            # Если все проверки пройдены, сохраняем бронирование
            reservation.save()
            messages.success(request, "Ваше бронирование успешно зарегистрировано!")
            return redirect(self.success_url)  # Перенаправление на страницу с успешным бронированием

        # Если форма не прошла валидацию, отправляем общее сообщение об ошибке
        messages.error(
            request,
            "К сожалению, на это время уже занято. Выберите другой стол или дату",
        )
        return self.get(request, *args, **kwargs)  # Возврат на ту же страницу

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.groups.filter(name='admin').exists():
            return qs
        return qs.filter(owner=self.request.user)

class ReservationCreateView(LoginRequiredMixin, CreateView):
    """Страница создания бронирования."""

    model = Reservation
    form_class = ReservationForm
    template_name = "reservation/reservation_list.html"
    success_url = reverse_lazy("reservation:reservation_list")


    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)



class ReservationUpdateView(UpdateView, ):
    """Страница редактирование бронирования."""

    model = Reservation
    form_class = ReservationForm
    template_name = "reservation/reservation_list.html"
    context_object_name = "reservation"
    success_url = reverse_lazy("reservation:personal_account")


    def get_object(self, queryset=None):
        """Получение одного объекта."""
        reservation = super().get_object(queryset)
        if self.request.user != reservation.owner:
            raise PermissionRequiredMixin("Вы не можете редактировать это бронирование.")
        return reservation

    def get_context_data(self, **kwargs):
        """Добавление данных в контекст шаблона."""
        context = super().get_context_data(**kwargs)
        context["from_personal_account"] = True  # чтобы было доступно только при режиме редактирования
        return context

    def form_valid(self, form):
        """Обработка данных, если форма прошла валидацию."""
        reservation = form.save(commit=False)

        # Проверка, что дата бронирования не в прошлом
        if reservation.reserved_at and reservation.reserved_at < timezone.now():
            messages.error(self.request, "Дата бронирования не может быть в прошлом.")
            return self.form_invalid(form)

        # Проверка интервала бронирования (60 минут после)
        reserved_at = reservation.reserved_at
        start_time = reserved_at
        end_time = start_time + timedelta(minutes=60)

        # Проверка, есть ли уже бронирования в этом интервале
        interval_reservation = Reservation.objects.filter(reserved_at__range=(start_time, end_time)).exclude(
            id=reservation.id
        )  # Исключаем текущее бронирование

        if interval_reservation.exists():
            messages.error(self.request, "К сожалению, на это время уже занято.")
            return self.form_invalid(form)

        # Если все проверки пройдены, сохраняем бронирование
        reservation.save()
        messages.success(self.request, "Бронирование успешно обновлено!")
        return super().form_valid(form)


class ReservationDeleteView(DeleteView):
    """Cтраница удаления бронирования."""

    model = Reservation
    success_url = reverse_lazy("reservation:personal_account")


    def get_object(self, queryset=None):
        """Получение одного объекта."""
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            self.object.save()
            return self.object
        raise PermissionRequiredMixin


class PersonalAccountListView(ListView):
    """Cтраница личного кабинета"""

    model = Reservation
    template_name = "reservation/personal_account.html"

    def get_queryset(self):
        """Набор данных, для отображения в представлении."""

        # Фильтруем по владельцу и сортируем по дате и столику
        queryset = Reservation.objects.filter(owner=self.request.user).order_by("reserved_at", "table")
        return queryset


class Services(TemplateView):
    """Cтраница услуги."""

    template_name = "reservation/services.html"


class Mission(TemplateView):
    """Cтраница миссия и ценности."""

    template_name = "reservation/mission.html"


class Team(TemplateView):
    """Cтраница команда."""

    template_name = "reservation/team.html"


class History(TemplateView):
    """Cтраница истории."""

    template_name = "reservation/history.html"
