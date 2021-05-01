from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.core.mail import send_mail

# Create your views here.
class GetCategory(APIView):
    def get_datas(self):

        try:
            datas = Category.objects.values('category_name')
        except:
            datas = None

        return datas

    def post(self, request):
        datas = self.get_datas()

        if datas is None:
            return Response({'error': True})
        else:
            return Response({'error': False, 'data': datas})

class GetLatestHeadlines(APIView):
    def get_datas(self):

        try:
            datas = News.objects.all().values('id', 'headline').order_by('-id')[:3]
        except:
            datas = None

        return datas

    def post(self, request):
        datas = self.get_datas()

        if datas is None:
            return Response({'error': True})
        else:
            return Response({'error': False, 'data': datas})


class GetLogo(APIView):
    def get_datas(self):
        
        try:
            datas = Logo.objects.filter(status=True).values('logo').order_by('-id')[:1]
        except:
            datas = None

        return datas

    def post(self, request):
        datas = self.get_datas()

        if datas is None:
            return Response({'error': True})
        else:
            return Response({'error': False, 'data': datas})


class GetMostReadNews(APIView):
    def get_datas(self):

        try:
            datas = News.objects.all().values('id', 'headline', 'views', 'author__username', 'image',
                                              'posted_date').order_by('-views')[:5]
        except:
            datas = None

        return datas

    def post(self, request):
        datas = self.get_datas()

        if datas is None:
            return Response({'error': True})
        else:
            return Response({'error': False, 'data': datas})


class GetHomePageNews(APIView):
    def get_datas(self, category):

        try:
            datas = []
            for item in category:
                a = {}
                data = News.objects.filter(category__category_name=item).values('id', 'headline', 'image', 'posted_date',
                                                                                 'author__username', 'views').order_by('-id')[:5]
                a = {'category': item, 'news': data}
                datas.append(a)
        except:
            datas = None

        return datas

    def post(self, request):
        category = ['News', 'Sports', 'Entertainment', 'Politics', 'Technology', 'Finance']
        datas = self.get_datas(category)

        if datas is None:
            return Response({'error': True})
        else:
            return Response({'error': False, 'data': datas})


class GetPoll(APIView):
    def get_datas(self):
        try:
            latest_poll = VotingPoll.objects.all().values('id', 'question', 'total_votes').latest('id')
            # print(latest_poll.id)
            poll_options = PollOptions.objects.filter(voting_poll__id=latest_poll['id']).values('id', 'option', 'num_of_votes')
            # print(poll_options)
            datas = {'poll':latest_poll, 'options':poll_options}
        
        except:
            datas = None
        
        return datas

    def post(self, request):
        datas = self.get_datas()
        if datas is None:
            return Response({'error': True})
        else:
            return Response({'error': False, 'data': datas})

class VotePoll(APIView):
    def post(self, request):
        poll_option_voted_id = None
        poll_id = None

        if 'poll_id' in request.data:
            poll_id = request.data['poll_id']
        if 'poll_option_voted_id' in request.data:
            poll_option_voted_id = request.data['poll_option_voted_id']

        try:
            poll = VotingPoll.objects.get(id=poll_id)
            poll.total_votes += 1
            poll.save()

            poll_option_voted = PollOptions.objects.get(id=poll_option_voted_id)
            poll_option_voted.num_of_votes += 1
            poll_option_voted.save()

            return Response({'error': False})

        except:
            return Response(({'error': True})) 


class GetFullNews(APIView):
    def increase_views(self, news_id):
        try:
            news = News.objects.get(id=news_id)
            news.views += 1
            news.save()
        except:
            pass

    def get_datas(self, news_id):
        try:
            news = News.objects.filter(id=news_id).values('id', 'headline', 'image', 'author__username', 'views', 'description',
                                                            'credit', 'posted_date', 'category__category_name')
            comments = Comments.objects.filter(news_id__id=news_id).values('name', 'mail_address', 'comment', 'posted_date')
            hashtags = Hashtags.objects.all().values('tags')
            categories = Category.objects.values('category_name')
            datas = {'news':news, 'comments':comments, 'hashtags':hashtags, 'categories':categories }        
        except:
            datas = None

        return datas

    def post(self, request):
        news_id = None

        if 'id' in request.data:
            news_id = request.data['id']

        self.increase_views(news_id)

        datas = self.get_datas(news_id)

        if datas is None:
            return Response({'error': True})
        else:
            return Response({'error': False, 'data': datas})

# class IncreaseViews(APIView):
#     def post(self, request):
#         news_id = None

#         if 'id' in request.data:
#             news_id = request.data['id']

#             news = News.objects.get(id=news_id)
#             news.views+=1
#             news.save()

#             return Response({'error': False})
        
#         else:
#             return Response({'error': True})

class SubmitComment(APIView):
    def get_datas(self, news_id):
        try:
            datas = Comments.objects.filter(news_id=news_id).values('name', 'mail_address', 'comment', 'posted_date').order_by('-id')
        except:
            datas = None

        return datas

    def post(self, request):
        name = None
        comment = None
        mail_address = None
        news_id = None
        
        if 'name' in request.data:
            name = request.data['name']
        if 'comment' in request.data:
            comment = request.data['comment']
        if 'mail_address' in request.data:
            mail_address = request.data['mail_address']
        if 'news_id' in request.data:
            news_id = request.data['news_id']

        news = News.objects.get(id=news_id)

        comment_to_post = Comments(name=name, comment=comment, mail_address=mail_address, news_id=news)

        try:
            comment_to_post.save()
            error = False
        except:
            error = True

        datas = self.get_datas(news_id)

        if datas is None:
            return Response({'error': error})
        else:
            return Response({'error': error, 'data': datas})


class GetCategoryNews(APIView):
    def get_datas(self, category):
        try:
            latest_category_news = News.objects.filter(category__category_name=category).values('id', 'headline', 'image', 
                                    'posted_date', 'author__username', 'views').order_by('-id')

            most_viewed_category_news = News.objects.filter(category__category_name=category).values('id', 'headline', 'image', 
                                'posted_date', 'author__username', 'views').order_by('-views')

            datas = {'latest_category_news':latest_category_news, 'most_viewed_category_news':most_viewed_category_news}

        except:
            datas = None
        
        return datas

    def post(self, request):
        category = None

        if 'category' in request.data:
            category = request.data['category']

        datas = self.get_datas(category)

        if datas is None:
            return Response({'error': True})
        else:
            return Response({'error': False, 'data': datas})


class SendMessage(APIView):
    def post(self, request):
        name = None
        mail = None
        message = None

        if 'name' in request.data:
            name = request.data['name']
        if 'mail' in request.data:
            mail = request.data['mail']
        if 'message' in request.data:
            message = request.data['message']

        message_to_send = Message(name=name, mail=mail, message=message)

        try:
            message_to_send.save()
            send_mail(
                'Message Received Successfully',
                'We have received your message. We will contact you soon.',
                'anykhabar78@gmail.com',
                [mail],
                fail_silently=False,
            ),
            send_mail(
                'Mail Received from ' + name,
                message,
                'anykhabar78@gmail.com',
                ['anykhabar78@gmail.com'],
                fail_silently=False,
            )
            return Response({'error': False})
        except:
            return Response({'error': True})

class GetAds(APIView):
    def get_datas(self):
        try:
            datas = Ads.objects.filter(status=True).values('page', 'location', 'image', 'url_link')

        except:
            datas = None

        return datas

    def post(self, request):
        datas = self.get_datas()

        if datas is None:
            return Response({'error': True})
        else:
            return Response({'error': False, 'data': datas})





