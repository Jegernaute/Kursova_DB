from datetime import datetime

import factory
from django.utils.crypto import get_random_string
from faker import Faker
from .models import User, UserPayment, UserAddress, PaymentDetails, OrderDetails, Price, Trainer, Training, \
    Subscription, SubscriptionDetail, OrderItem

fake = Faker('uk_UA')

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Sequence(lambda n: f"{get_random_string(8)}@example.com")
    password = factory.Faker('password')
    phone = factory.LazyAttribute(lambda _: fake.phone_number())
    gender = factory.Faker('random_element', elements=['M', 'F'])

def format_phone_number(phone_number):
    return f"({phone_number[0:3]}) {phone_number[3:6]}-{phone_number[6:8]}-{phone_number[8:]}"

class UserPaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserPayment

    user = factory.SubFactory(UserFactory)  # Використання існуючого користувача
    payment_type = factory.Faker('word')
    provider = factory.Faker('company')

class UserAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserAddress

    user = factory.SubFactory(UserFactory)  # Використання існуючого користувача
    city = factory.Faker('city')
    address_line_1 = factory.Faker('address')
    postal_code = factory.LazyFunction(lambda: str(fake.random_int(min=100000, max=999999)))
    mobile = factory.LazyAttribute(lambda _: fake.phone_number())


def format_mobile_number(phone_number):
    return f"({phone_number[0:3]}) {phone_number[3:6]}-{phone_number[6:8]}-{phone_number[8:]}"

class PaymentDetailsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentDetails

    user_payment = factory.SubFactory(UserPaymentFactory)
    order_id = factory.Sequence(lambda n: n)
    amount = factory.Faker('random_number', digits=2)
    provider = factory.Faker('company')
    status = factory.Faker('random_element', elements=['оплачено', 'не оплачено'])
    payment_date = factory.Faker('date_this_decade')

class OrderDetailsFactory (factory.django.DjangoModelFactory):
    class Meta:
        model = OrderDetails

    user =  factory.SubFactory(UserFactory)
    order_date = factory.LazyFunction(datetime.now)
    total = factory.Faker('random_number', digits=2)
    payment = factory.SubFactory(PaymentDetailsFactory)

class PriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Price

    name = factory.Faker('company')
    subscription_type = factory.Faker('random_element', elements=['30', '90', '180', '365'])
    discount_percent = factory.Faker('random_number', digits=2, fix_len=True)
    amount = factory.Faker('random_number', digits=5, fix_len=True)

class TrainerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Trainer

    name = factory.Faker('name')
    phone = factory.Faker('phone_number')

class TrainingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Training

    price = factory.SubFactory(PriceFactory)
    name = factory.Faker('random_element', elements=[
        'Хатха-йога',
        'Аштанга-йога',
        'Інь-йога',
        'Тренування в залі (індивідуально)',
        'Тренування в залі (з тренером)'
    ])
    description = factory.Faker('sentence')

class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subscription

    user = factory.SubFactory(UserFactory)
    subscription_type = factory.Faker('word')
    start_date = factory.Faker('date_this_decade')
    end_date = factory.Faker('date_between', start_date='+1y', end_date='+3y')

class SubscriptionDetailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubscriptionDetail

    training = factory.SubFactory(TrainingFactory)
    subscription = factory.SubFactory(SubscriptionFactory)
    trainer = factory.SubFactory(TrainerFactory)

class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderDetailsFactory)
    training = factory.SubFactory(TrainingFactory)
    subscription_type = factory.Faker('word')