from django.contrib import admin

from .models import Reservation, Restaurant, Table


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "table",
        "reserved_at",
        "customer_name",
        "customer_contact",
    )
    list_filter = (
        "table",
        "customer_name",
        "reserved_at",
    )
    search_fields = (
        "table",
        "customer_name",
        "reserved_at",
    )


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "history", "mission")
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("id", "number", "capacity")
    list_filter = ("number",)
    search_fields = ("number",)
