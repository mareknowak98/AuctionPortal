from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.contrib.sessions.models import Session

#default User, fields in use
#login
#mail
#password

#Profile class extends standar django User model with other functionalities
class Profile(models.Model):
    #default id
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # avatar = models.ImageField(default='default.jpg', blank=True)
    bank_account_nr = models.CharField(max_length=30) #TODO set to real max len
    date_created = models.DateField()
    telephone_number = models.CharField(max_length=15)
    number_of_opinions = models.IntegerField(default=0)
    avg_opinion = models.DecimalField(max_digits=4, decimal_places=3, default=0.0)

    def __str__(self):
        return "{0} Profile".format(self.user.username)

    def save(self):
        super().save()

    # def save(self, *args, **kwargs):
    #     super(Profile, self).save(*args, **kwargs)
    #     img = Image.open(self.avatar.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


# #TODO to fix later

# class Address(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address_user')
#     country = models.CharField(max_length=50, null=True, blank=True)
#     city = models.CharField(max_length=50, null=True, blank=True)
#     street = models.CharField(max_length=50, null=True, blank=True)
#     home_number = models.CharField(max_length=20, null=True, blank=True) #charfield to allow adress like 14A, 14/5
#     postal_code = models.CharField(max_length=6, null=True, blank=True)
#
#     def __str__(self):
#         return "{0}, {1}, {2} - {3}".format(self.city, self.street, self.home_number, self.user.username)
#
class Product(models.Model):
    image = models.ImageField(default='default.jpg', blank=True)
    product_name = models.CharField(max_length=50)
    description = models.TextField()
    is_new = models.BooleanField() #False-used, True-new

    def __str__(self):
        return '{0} {1}'.format(self.product_name, self.is_new)
#
class Auction(models.Model):
    user_seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_user')
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='product')
    # user_highest_bid = models.OneToOneField(User, on_delete=models.CASCADE)
    user_highest_bid = models.IntegerField()
    date_started = models.DateTimeField()
    date_end = models.DateTimeField()
    starting_price = models.DecimalField(max_digits=12, decimal_places=2)
    highest_bid = models.DecimalField(max_digits=12, decimal_places=2)
    minimal_price = models.DecimalField(max_digits=12, decimal_places=2)
    is_shipping_av = models.BooleanField()

    def __str__(self):
        return "{0} - Auction".format(self.product)
#
# class Message(models.Model):
#     sender = models.ForeignKey(User, related_name='sender_user')
#     receiver = models.ForeignKey(User, related_name='receiver_user')
#     message = models.TextField(default='')
#     send_at = models.DateTimeField()
#
#     def __str__(self):
#         return "{0} -> {1} message".format(self.sender, self.receiver)
#
# class AuctionsWon(models.Model):
#     user = models.ForeignKey(User, related_name='winner_user')
#     auction = models.ForeignKey(Auction, related_name='auction_won')
#     end_price = models.DecimalField()
#
#     def __str__(self):
#         return "{0} won by {1}".format(self.auction, self.user.username)