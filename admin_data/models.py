from django.db import models


class SubscriptionPlan(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    price = models.FloatField()
    max_posts = models.IntegerField(null=True, blank=True)
    max_images_per_post = models.IntegerField(null=True, blank=True)
    max_likes = models.IntegerField(null=True, blank=True)
    max_comments = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "subscription_plans"

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    subscription_plan_id = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "users"

    def __str__(self):
        return self.username


class BillingHistory(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    subscription_plan_id = models.IntegerField()
    price = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    transaction_id = models.CharField(max_length=100, unique=True)
    invoice_path = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "billing_history"

    def __str__(self):
        return self.transaction_id
