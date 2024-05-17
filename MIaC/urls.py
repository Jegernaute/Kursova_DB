from django.urls import path
from .views import UserListView, UserPaymentListView, UserAddressListView, PaymentDetailsListView, OrderDetailsListView, \
    PriceListView, TrainerListView, TrainingListView, SubscriptionListView, SubscriptionDetailListView, \
    OrderItemListView, StatisticsView

urlpatterns = [
    path('user/', UserListView.as_view(), name="user_list"),
    path('user/<uuid:pk>/', UserListView.as_view(), name="user_detail"),
    path('user_payment/', UserPaymentListView.as_view(), name="user_payment"),
    path('user_address/', UserAddressListView.as_view(), name="user_address"),
    path('user_address/<uuid:pk>/', UserAddressListView.as_view(), name="user_address"),
    path('payment_details/', PaymentDetailsListView.as_view(), name="payment_details"),
    path('order_details/', OrderDetailsListView.as_view(), name="order_details"),
    path('price/', PriceListView.as_view(), name="price"),
    path('price/<uuid:pk>/', PriceListView.as_view(), name="price"),
    path('trainer/', TrainerListView.as_view(), name="trainer"),
    path('trainer/<uuid:pk>/', TrainerListView.as_view(), name="trainer"),
    path('training/', TrainingListView.as_view(), name="training"),
    path('training/<uuid:pk>/', TrainingListView.as_view(), name="training"),
    path('subscription/', SubscriptionListView.as_view(), name="subscription"),
    path('subscription_detail/', SubscriptionDetailListView.as_view(), name="subscription_detail"),
    path('order_item/', OrderItemListView.as_view(), name="order_item"),
    path('statistic/', StatisticsView.as_view(), name="statistic"),
]