import app.tasks

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        Profile.objects.create(profileUser=instance)


# Profile class extends standard django User model with other functionalities
class Profile(models.Model):
    profileUserName = models.CharField(blank=True, null=True, max_length=50)
    profileUserSurname = models.CharField(blank=True, null=True, max_length=50)
    profileUser = models.OneToOneField(User, on_delete=models.CASCADE)
    profileAvatar = models.ImageField(default='https://res.cloudinary.com/dm2tx6lhe/image/upload/v1608653722/media/images/default_d19dbf', upload_to='images/', blank=True, null=True)
    profileTelephoneNumber = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return "{0} Profile".format(self.profileUser.username)


# class to form custom Integer Field
class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class UserOpinion(models.Model):
    opinionUserAbout = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userAbout')
    opinionUserAuthor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userAuthor')
    opinionDescription = models.TextField(max_length=300, blank=True, null=True)
    opinionStars = IntegerRangeField(min_value=1, max_value=5)
    opinionDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} opinion about {1}({2})".format(self.opinionUserAuthor.username, self.opinionUserAbout.username, self.opinionStars)


class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return '{} category'.format(self.category_name)

class Auction(models.Model):
    auctionUserSeller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctionUserSeller')
    auctionImage = models.ImageField(default='https://res.cloudinary.com/dm2tx6lhe/image/upload/v1608590488/media/images/default_auction_fe1wvk', upload_to='images/', blank=True, null=True)
    auctionCategory = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='auctionCategory', default=4)
    auctionProductName = models.CharField(max_length=50, default='')
    auctionDescription = models.TextField(blank=True, null=True)
    auctionIsNew = models.BooleanField(blank=True, null=True)
    auctionUserHighestBid = models.IntegerField(blank=True, null=True)
    auctionDateStarted = models.DateTimeField()
    auctionDateEnd = models.DateTimeField()
    auctionStartingPrice = models.DecimalField(max_digits=12, decimal_places=2)
    auctionHighestBid = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    auctionMinimalPrice = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    auctionIsShippingAv = models.BooleanField(default=False)
    auctionIsActive = models.BooleanField(default=True)
    auctionShippingCost = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        create_task = False
        if self.pk is None:
            self.auctionHighestBid = self.auctionStartingPrice
            create_task=True
            if self.auctionShippingCost is None and self.auctionIsShippingAv is True:
                self.auctionShippingCost = 20.0

        super(Auction, self).save(*args, **kwargs)
        if create_task:
            app.tasks.set_inactive.apply_async(args=[self.id], eta=self.auctionDateEnd)

    def __str__(self):
        return "{0} - Auction".format(self.auctionProductName)


class Bid(models.Model):
    bidUserBuyer = models.ForeignKey(User, on_delete=models.CASCADE)
    bidAuction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidPrice = models.DecimalField(max_digits=10, decimal_places=2)
    bidDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Bid made by {0} on {1} auction - {2}$".format(self.bidUserBuyer.username, self.bidAuction.auctionProductName,
                                                              self.bidPrice)

class Message(models.Model):
    messageContent = models.TextField()
    messageCreatedAt = models.DateTimeField(auto_now_add=True)
    messageUpdatedAt = models.DateTimeField(auto_now=True)
    messageIsDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.messageContent

class UserMessage(models.Model):
    usermessMessage = models.ForeignKey(Message, on_delete=models.CASCADE)
    usermessFromUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    usermessToUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user_id')
    usermessIsDeleted = models.BooleanField(default=False) ##TODO delete

    def __str__(self):
        return "UserMessage {0}".format(self.usermessMessage)

class AuctionReport(models.Model):
    reportAuction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    reportUser = models.ForeignKey(User, on_delete=models.CASCADE)
    reportContent = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Reportser: {0} by {1}".format(self.reportAuction, self.reportUser)