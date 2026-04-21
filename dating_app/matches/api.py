from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Case, When, Value, IntegerField,Count,F
from accounts.models import User
from matches.models import Match
from accounts.serializers import UserSerializer

class FeedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        user_pref = user.interested_in

        queryset = User.objects.select_related('city').exclude(id=user.id)
        swiped_users = Match.objects.filter(user_from=user).values('user_to')
        queryset = queryset.exclude(id__in=swiped_users)

        queryset = queryset.annotate(
            priority=Case(
                When(city=user.city, then=Value(1)),
                default=Value(2),
                output_field=IntegerField()
            )
        )

        if user_pref != "A":
            queryset = queryset.filter(gender=user_pref)

        users_to_show = queryset.order_by('priority', '-last_seen')[:15]

        serializer = UserSerializer(users_to_show,many = True)

        return Response(serializer.data)


class StatisticsAPIView(APIView):
    # Разрешаем смотреть общую статистику всем, даже неавторизованным
    permission_classes = []

    def get(self, request):

        raw_cities = User.objects.exclude(city__isnull=True) \
            .values('city__name') \
            .annotate(total_users=Count('id')) \
            .order_by('-total_users')

        users_by_city = [
            {"city_name": item['city__name'], "total_users": item['total_users']}
            for item in raw_cities
        ]

        raw_genders = User.objects.exclude(gender__isnull=True) \
            .values('gender') \
            .annotate(total=Count('id'))

        gender_stats = []
        for item in raw_genders:
            gender_name = "Мужчины" if item['gender'] == 'M' else "Женщины"
            gender_stats.append({"gender": gender_name, "total": item['total']})

        my_stats = None
        if request.user.is_authenticated:
            my_likes_sent = Match.objects.filter(user_from=request.user, status=Match.Status.LIKE).count()
            my_likes_received = Match.objects.filter(user_to=request.user, status=Match.Status.LIKE).count()

            mutual_matches = User.objects.filter(
                swipes_received__user_from=request.user, swipes_received__status=Match.Status.LIKE,
                swipes_sent__user_to=request.user, swipes_sent__status=Match.Status.LIKE
            ).count()

            my_stats = {
                "likes_sent": my_likes_sent,
                "secret_admirers": my_likes_received,
                "mutual_matches": mutual_matches
            }

        # Отдаем собранные данные
        return Response({
            "app_global_stats": {
                "total_registered": User.objects.count(),
                "users_by_city": users_by_city,  # Теперь здесь безопасный Python-список
                "users_by_gender": gender_stats,
            },
            "my_personal_stats": my_stats
        })
