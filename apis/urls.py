from django.urls import path
from .views import *

urlpatterns = [
    path('getcategory/', GetCategory.as_view()),
    path('getlatestheadlines/', GetLatestHeadlines.as_view()),
    path('getlogo/', GetLogo.as_view()),
    path('getmostreadnews/', GetMostReadNews.as_view()),
    path('gethomepagenews/', GetHomePageNews.as_view()),
    path('getfullnews/', GetFullNews.as_view()),
    # path('increaseviews/', IncreaseViews.as_view()),
    path('submitcomment/', SubmitComment.as_view()),
    path('getcategorynews/', GetCategoryNews.as_view()),
    path('sendmessage/', SendMessage.as_view()),
    path('getpoll/', GetPoll.as_view()),
    path('votepoll/', VotePoll.as_view()),
    path('getads/', GetAds.as_view())
]
