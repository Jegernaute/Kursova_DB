from django.db import models, transaction
import uuid

from django.db.models import F


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, choices=(
        ('M', 'Чоловік'),
        ('F', 'Жінка')
    ))

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['first_name', 'last_name'])
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"




class UserPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=255, null=False, blank=False)
    provider = models.CharField(max_length=255, null=False, blank=False)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['user','payment_type','provider'])
        ]

    def __str__(self):
        return f" {self.user} {self.payment_type} {self.provider}"

class UserAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=255, null=False, blank=False )
    address_line_1 = models.CharField(max_length=255, null=False, blank=False)
    address_line_2 = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=10, null=False, blank=False)
    mobile = models.CharField(max_length=20, null=False, blank=False)
    telephone = models.CharField(max_length=20, blank=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['user','city','address_line_1'])
        ]


    def __str__(self):
        return f"{self.user} {self.city} {self.address_line_1}"

    @classmethod
    def get_addresses_with_matching_phone(cls):
        return cls.objects.filter(mobile=F('user__phone'))

class PaymentDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_payment = models.ForeignKey(
        UserPayment, on_delete=models.CASCADE, related_name="payment_details"
    )
    order_id = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    payment_date = models.DateField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f" {self.payment_date}"


class OrderDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.ForeignKey(PaymentDetails, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'order_date', 'total'])
        ]

    def __str__(self):
        return f"{self.user} {self.order_date} {self.total}"

class Price(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    subscription_type = models.CharField(max_length=255, choices=(
        ('30', '30'),
        ('90', '90'),
        ('180', '180'),
        ('365', '365')
    ))
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.amount}"

class Trainer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['name', 'phone'])
        ]

    def __str__(self):
        return f"{self.name} {self.phone}"

class Training(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.ForeignKey('Price', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, choices=(
    ('Хатха-йога', 'Хатха-йога'),
    ('Аштанга-йога', 'Аштанга-йога'),
    ('Інь-йога', 'Інь-йога'),
    ('Тренування в залі (індивідуально)', 'Тренування в залі (індивідуально)'),
    ('Тренування в залі (з тренером)', 'Тренування в залі (з тренером)')
    ))
    description = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['name', 'price'])
        ]

    def __str__(self):
        return f"{self.name} {self.price}"

class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['start_date', 'end_date'])
        ]

    def __str__(self):
        return f"{self.start_date} / {self.end_date}"

class SubscriptionDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['training', 'subscription', 'trainer'])
        ]

    def __str__(self):
        return f"{self.training} {self.subscription} {self.trainer}"

class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey('OrderDetails', on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['order', 'training', 'subscription_type'])
        ]

    def __str__(self):
        return f"{self.order} {self.training} {self.subscription_type}"

