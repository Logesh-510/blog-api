from django.contrib import admin

from .models import BillingHistory, SubscriptionPlan, User


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "max_posts",
        "max_images_per_post",
        "max_likes",
        "max_comments",
    )
    list_display_links = ("id", "name")
    search_fields = ("name",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "subscription_plan_id",
    )
    search_fields = ("username", "email")
    list_filter = ("subscription_plan_id",)


@admin.register(BillingHistory)
class BillingHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "subscription_plan_id",
        "price",
        "start_date",
        "end_date",
        "transaction_id",
    )
    search_fields = ("transaction_id",)
    list_filter = ("subscription_plan_id",)
