from django.contrib import admin
from .models import User, UserPayment, UserAddress, PaymentDetails, OrderDetails, Price, Trainer, Training, \
    Subscription, SubscriptionDetail, OrderItem

admin.site.register(User)
admin.site.register(UserPayment)
admin.site.register(UserAddress)
admin.site.register(PaymentDetails)
admin.site.register(OrderDetails)
admin.site.register(Price)
admin.site.register(Trainer)
admin.site.register(Training)
admin.site.register(Subscription)
admin.site.register(SubscriptionDetail)
admin.site.register(OrderItem)