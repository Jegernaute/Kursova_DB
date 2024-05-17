from rest_framework import serializers
from .models import User, UserPayment, UserAddress, PaymentDetails, OrderDetails, Price, Trainer, Training, \
    Subscription, OrderItem, SubscriptionDetail


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserPaymentSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()

    class Meta:
        model = UserPayment
        fields = '__all__'

    def get_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

class UserAddressSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()

    class Meta:
        model = UserAddress
        fields = '__all__'

    def get_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

class PaymentDetailsSerializer(serializers.ModelSerializer):

    user_payment = serializers.SerializerMethodField()

    class Meta:
        model = PaymentDetails
        fields = '__all__'

    def get_user_payment(self, obj):
        user_payment = obj.user_payment
        return f" {user_payment.payment_type} {user_payment.provider}"

class OrderDetailsSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()


    class Meta:
        model = OrderDetails
        fields = '__all__'

    def get_payment(self, obj):
        return f"{obj.payment.payment_date}"

    def get_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'

class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = '__all__'

class TrainingSerializer(serializers.ModelSerializer):

    price = serializers.SerializerMethodField()

    class Meta:
        model = Training
        fields = '__all__'

    def get_price(self, obj):
        return f"{obj.price.amount}"

class SubscriptionSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = '__all__'

    def get_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

class SubscriptionDetailSerializer(serializers.ModelSerializer):

    training = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()
    trainer = serializers.SerializerMethodField()


    class Meta:
        model = SubscriptionDetail
        fields = '__all__'


    def get_training(self, obj):
        return f"{obj.training.name} {obj.training.price}"

    def get_subscription(self, obj):
        return f"{obj.subscription.start_date} {obj.subscription.end_date}"

    def get_trainer(self, obj):
        return f"{obj.trainer.name} {obj.trainer.phone}"

class OrderItemSerializer(serializers.ModelSerializer):

    order = serializers.SerializerMethodField()
    training = serializers.SerializerMethodField()



    class Meta:
        model = OrderItem
        fields = '__all__'

    def get_order(self, obj):
        return f"{obj.order.user} {obj.order.order_date} {obj.order.total}  "

    def get_training(self, obj):
        return f"{obj.training.name} {obj.training.price}"
