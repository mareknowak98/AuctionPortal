# from celery import Celery
# from celery import task
#
# celery = Celery('tasks', broker='amqp://guest@localhost//') #!
#
# import os
#
# os.environ[ 'DJANGO_SETTINGS_MODULE' ] = "proj.settings"
#
# @app.task
# def set_inactive(auction_object):
#     auction_object.is_active = False
#     auction_object.save()
#

from celery import shared_task
# from rest_framework.response import Response
import app.models as mod
# from .serializers import AuctionSerializer

#end auction when date_end expire
@shared_task(serializer='json')
def set_inactive(auction_id):
    auction_ob = mod.Auction.objects.get(id=auction_id)
    auction_ob.is_active = False
    auction_ob.save()
    return {"status": True}