from django.contrib import admin
from .models import Auction, Category, Bid, Profile, Message, UserMessage, UserOpinion
# Register your models here.

# admin.site.register(Product)
admin.site.register(Auction)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(UserMessage)
admin.site.register(UserOpinion)

