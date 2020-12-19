# from __future__ import absolute_import, unicode_literals
from celery import shared_task

# import app.models as mod
from .models import models

#end auction when date_end expire
@shared_task(serializer='json')
def set_inactive(auction_id):
    auction_ob = models.Auction.objects.get(id=auction_id)
    auction_ob.is_active = False
    auction_ob.save()
    return {"status": True}