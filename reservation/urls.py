from django.urls import path

from reservation.apps import ReservationConfig
from reservation.views import (
    AboutView,
    Contacts,
    Feedback,
    MainView,
    Mission,
    PersonalAccountListView,
    ReservationCreateView,
    ReservationDeleteView,
    ReservationListView,
    ReservationUpdateView,
    Services,
    Team,
    History,
)

app_name = ReservationConfig.name

urlpatterns = [
    # path('', home, name='home'),
    path("", MainView.as_view(), name="main"),
    path("contacts/", Contacts.as_view(), name="contacts"),
    path("feedback/", Feedback.as_view(), name="feedback"),
    path("about/", AboutView.as_view(), name="about"),
    path("services/", Services.as_view(), name="services"),
    path("mission/", Mission.as_view(), name="mission"),
    path("history/", History.as_view(), name="history"),
    path("team/", Team.as_view(), name="team"),
    path("reservation/", ReservationListView.as_view(), name="reservation_list"),
    path(
        "reservation/create/",
        ReservationCreateView.as_view(),
        name="reservation_create",
    ),
    path(
        "reservation/<int:pk>/update/",
        ReservationUpdateView.as_view(),
        name="reservation_update",
    ),
    path(
        "reservation/<int:pk>/delete/",
        ReservationDeleteView.as_view(),
        name="reservation_delete",
    ),
    path("personal_account/", PersonalAccountListView.as_view(), name="personal_account"),
]
