from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.views import APIView



from .models import User, UserPayment, UserAddress, PaymentDetails, OrderDetails, Price, Trainer, Training, \
    Subscription, SubscriptionDetail, OrderItem
from .seriralizers import UserSerializer, UserPaymentSerializer, UserAddressSerializer, PaymentDetailsSerializer, \
    OrderDetailsSerializer, PriceSerializer, TrainerSerializer, TrainingSerializer, SubscriptionSerializer, \
    SubscriptionDetailSerializer, OrderItemSerializer


class UserListView(APIView):

    @method_decorator(cache_page(60 * 15))  # Кешувати на 15 хвилин
    def get(self, request, *args, **kwargs):
        users = User.objects.all()

        search_term = request.query_params.get('search_term')

        # Пошук user за прізвищем або ім'ям
        if search_term:
            users = users.filter(Q(first_name__icontains=search_term) |
                                 Q(last_name__icontains=search_term))

        user_id = request.query_params.get("id")
        email = request.query_params.get("email")
        if user_id:
            users = users.filter(id=user_id)
        elif email:
            users = users.filter(email__icontains=email)
        first_name = request.query_params.get("first_name")
        if first_name:
            users = users.filter(first_name__icontains=first_name)
        last_name = request.query_params.get("last_name")
        if last_name:
            users = users.filter(last_name__icontains=last_name)
        password = request.query_params.get("password")
        if password:
            users = users.filter(password=password)
        phone = request.query_params.get("phone")
        if phone:
            users = users.filter(phone=phone)
        gender = request.query_params.get("gender")
        if gender:
            users = users.filter(gender=gender)


        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            user=User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserPaymentListView(APIView):
    @method_decorator(cache_page(60 * 15))  # Кешувати на 15 хвилин
    def get(self, request, *args, **kwargs):

        user_payment = UserPayment.objects.all().select_related('user')

        user_payment_id = request.query_params.get("user_payment_id")
        user = request.query_params.get("user")
        if user_payment_id:
            user_payment = user_payment.filter(user_payment_id=user_payment_id)
        elif user:
            user_payment = user_payment.filter(user=user)
        payment_type = request.query_params.get("payment_type")
        if payment_type:
            user_payment = user_payment.filter(payment_type=payment_type)
        provider = request.query_params.get("provider")
        if provider:
            user_payment = user_payment.filter(provider=provider)



        serializer = UserPaymentSerializer(user_payment, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = UserPaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAddressListView(APIView):

    @method_decorator(cache_page(60 * 15))  # Кешувати на 15 хвилин
    def get(self, request, *args, **kwargs):

        user_address = UserAddress.objects.all().select_related('user')

        user_address_id = request.query_params.get("user_address_id")
        user = request.query_params.get("user")
        if user_address_id:
            user_address = user_address.filter(user_address_id=user_address_id)
        elif user:
            user_address = user_address.filter(user=user)
        city = request.query_params.get("city")
        if city:
            user_address = user_address.filter(city=city)
        address_line_1 = request.query_params.get("address_line_1")
        if address_line_1:
            user_address = user_address.filter(address_line_1=address_line_1)
        address_line_2 = request.query_params.get("address_line_2")
        if address_line_2:
            user_address = user_address.filter(address_line_2=address_line_2)
        postal_code = request.query_params.get("postal_code")
        if postal_code:
            user_address = user_address.filter(postal_code=postal_code)
        mobile = request.query_params.get("mobile")
        if mobile:
            user_address = user_address.filter(mobile=mobile)
        telephone = request.query_params.get("telephone")
        if telephone:
            user_address = user_address.filter(telephone=telephone)


        serializer = UserAddressSerializer(user_address, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = UserAddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk):
        try:
            user_address=UserAddress.objects.get(pk=pk)
        except UserAddress.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserAddressSerializer(user_address, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        try:
            user_address = UserAddress.objects.get(pk=pk)
        except UserAddress.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PaymentDetailsListView(APIView):

    @method_decorator(cache_page(60 * 15))  # Кешувати на 15 хвилин
    def get(self, request, *args, **kwargs):

        payment_details = PaymentDetails.objects.all().select_related('user_payment')

        # Отримання параметрів
        min_amount = request.query_params.get('min_amount')
        max_amount = request.query_params.get('max_amount')

        # Фільтрація за сумою
        if min_amount:
            payment_details = payment_details.filter(amount__gte=min_amount)
        if max_amount:
            payment_details = payment_details.filter(amount__lte=max_amount)

        user_payments_details_id = request.query_params.get("user_payments_details_id")
        user = request.query_params.get("user")
        if user_payments_details_id:
            payment_details = payment_details.filter(user_payments_details_id=user_payments_details_id)
        elif user:
            payment_details = payment_details.filter(user=user)
        order_id = request.query_params.get("order_id")
        if order_id:
            payment_details = payment_details.filter(order_id=order_id)
        amount = request.query_params.get("amount")
        if amount:
            payment_details = payment_details.filter(amount=amount)
        provider = request.query_params.get("provider")
        if provider:
            payment_details = payment_details.filter(provider=provider)
        status = request.query_params.get("status")
        if status:
            payment_details = payment_details.filter(status=status)
        payment_date = request.query_params.get("payment_date")
        if payment_date:
            payment_details = payment_details.filter(payment_date=payment_date)

        serializer = PaymentDetailsSerializer(payment_details, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PaymentDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailsListView(APIView):

    @method_decorator(cache_page(60 * 15))  # Кешувати на 15 хвилин
    def get(self, request, *args, **kwargs):

        order_details = OrderDetails.objects.all().select_related('user', 'payment')

        user_order_details_id = request.query_params.get("user_order_details_id")
        user = request.query_params.get("user")
        if user_order_details_id:
            order_details = order_details.filter(user_order_details_id=user_order_details_id)
        elif user:
            order_details = order_details.filter(user=user)
        order_date = request.query_params.get("order_date")
        if order_date:
            order_details = order_details.filter(order_date=order_date)
        total = request.query_params.get("total")
        if total:
            order_details = order_details.filter(total=total)
        payment = request.query_params.get("payment")
        if payment:
            order_details = order_details.filter(payment=payment)

        serializer = OrderDetailsSerializer(order_details, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = OrderDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PriceListView(APIView):

    @method_decorator(cache_page(60 * 15))  # Кешувати на 15 хвилин
    def get(self, request, *args, **kwargs):

        price = Price.objects.all()

        price_id = request.query_params.get("price_id")
        name = request.query_params.get("name")
        if price_id:
            price = price.filter(price_id=price_id)
        elif name:
            price = price.filter(name=name)
        subscription_type = request.query_params.get("subscription_type")
        if subscription_type:
            price = price.filter(subscription_type=subscription_type)
        discount_percent = request.query_params.get("discount_percent")
        if discount_percent:
            price = price.filter(discount_percent=discount_percent)
        amount = request.query_params.get("amount")
        if amount:
            price = price.filter(amount=amount)


        serializer = PriceSerializer(price, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = PriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk):
        try:
            price=Price.objects.get(pk=pk)
        except Price.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PriceSerializer(price, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        try:
            price = Price.objects.get(pk=pk)
        except Price.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        price.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TrainerListView(APIView):

    @method_decorator(cache_page(60 * 15))  # Кешувати на 15 хвилин
    def get(self, request, *args, **kwargs):

        trainer = Trainer.objects.all()

        trainer_id = request.query_params.get("trainer_id")
        name = request.query_params.get("name")
        if trainer_id:
            trainer = trainer.filter(trainer_id=trainer_id)
        elif name:
            trainer = trainer.filter(name=name)
        phone = request.query_params.get("phone")
        if phone:
            trainer = trainer.filter(phone=phone)


        serializer = TrainerSerializer(trainer, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = TrainerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk):
        try:
            trainer=Trainer.objects.get(pk=pk)
        except Trainer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TrainerSerializer(trainer, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            trainer = Trainer.objects.get(pk=pk)
        except Trainer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        trainer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class TrainingListView(APIView):

    @method_decorator(cache_page(60 * 15))  # Кешувати на 15 хвилин
    def get(self, request, *args, **kwargs):

        training = Training.objects.all().select_related('price')

        training_id = request.query_params.get("training_id")
        name = request.query_params.get("name")
        if training_id:
            training = training.filter(training_id=training_id)
        elif name:
            training = training.filter(name=name)
        price = request.query_params.get("price")
        if price:
            training = training.filter(price=price)
        description = request.query_params.get("description")
        if description:
            training = training.filter(description=description)

        serializer = TrainingSerializer(training, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = TrainingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk):
        try:
            training=Training.objects.get(pk=pk)
        except Training.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TrainingSerializer(training, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        try:
            training = Training.objects.get(pk=pk)
        except Training.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        training.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SubscriptionListView(APIView):


    @method_decorator(cache_page(60 * 15))  # Кешувати на 15 хвилин
    def get(self, request, *args, **kwargs):

        subscription = Subscription.objects.all().select_related('user')

        subscription_id = request.query_params.get("subscription_id")
        user = request.query_params.get("user")
        if subscription_id:
            subscription = subscription.filter(subscription_id=subscription_id)
        elif user:
            subscription = subscription.filter(user=user)
        subscription_type = request.query_params.get("subscription_type")
        if subscription_type:
            subscription = subscription.filter(subscription_type=subscription_type)
        start_date = request.query_params.get("start_date")
        if start_date:
            subscription = subscription.filter(start_date=start_date)
        end_date = request.query_params.get("end_date")
        if end_date:
             subscription = subscription.filter(end_date=end_date)

        serializer = SubscriptionSerializer(subscription, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubscriptionDetailListView(APIView):

    @method_decorator(cache_page(60 * 15))  # Кешувати на 15 хвилин
    def get(self, request, *args, **kwargs):

        subscription_detail = SubscriptionDetail.objects.all().select_related('subscription', 'training')

        subscription_detail_id = request.query_params.get("subscription_detail_id")
        training = request.query_params.get("training")
        if subscription_detail_id:
            subscription_detail = subscription_detail.filter(subscription_detail_id=subscription_detail_id)
        elif training:
            subscription_detail = subscription_detail.filter(training=training)
        subscription = request.query_params.get("subscription")
        if subscription:
            subscription_detail = subscription_detail.filter(subscription=subscription)
        trainer = request.query_params.get("trainer")
        if trainer:
            subscription_detail = subscription_detail.filter(trainer=trainer)

        serializer = SubscriptionDetailSerializer(subscription_detail, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubscriptionDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderItemListView(APIView):

    @method_decorator(cache_page(60 * 15))  # Кешувати на 15 хвилин
    def get(self, request, *args, **kwargs):

        order_item = OrderItem.objects.all().select_related('order','training')

        order_item_id = request.query_params.get("order_item_id")
        order = request.query_params.get("order")
        if order_item_id:
            order_item = order_item.filter(order_item_id=order_item_id)
        elif order:
            order_item = order_item.filter(order=order)
        training = request.query_params.get("training")
        if training:
            order_item = order_item.filter(training=training)
        subscription_type = request.query_params.get("subscription_type")
        if subscription_type:
            order_item = order_item.filter(subscription_type=subscription_type)

        serializer = OrderItemSerializer(order_item, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StatisticsView(APIView):
    def get(self, request):

        total_users = User.objects.count()
        total_payments = UserPayment.objects.count()
        total_addresses = UserAddress.objects.count()
        total_payment_details = PaymentDetails.objects.count()
        total_order_details = OrderDetails.objects.count()
        total_price = Price.objects.count()
        total_trainers = Trainer.objects.count()
        total_trainings = Training.objects.count()
        total_subscriptions = Subscription.objects.count()
        total_subscriptions_details = SubscriptionDetail.objects.count()
        total_order_items = OrderItem.objects.count()
        # Формування структури даних для відповіді
        statistics = {
            'total_users': total_users,
            'total_payments': total_payments,
            'total_addresses': total_addresses,
            'total_payment_details': total_payment_details,
            'total_order_details': total_order_details,
            'total_price': total_price,
            'total_trainers': total_trainers,
            'total_trainings': total_trainings,
            'total_subscriptions': total_subscriptions,
            'total_subscriptions_details': total_subscriptions_details,
            'total_order_items': total_order_items,
        }
        return Response(statistics)

