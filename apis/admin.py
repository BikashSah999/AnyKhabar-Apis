from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(News)
admin.site.register(Category)
admin.site.register(Logo)
admin.site.register(Comments)
admin.site.register(Hashtags)
admin.site.register(Message)
admin.site.register(PollOptions)
admin.site.register(VotingPoll)
admin.site.register(Ads)