from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CategoryViewSet,
                    GenreViewSet,
                    TitleViewSet,
                    CommentViewSet,
                    ReviewViewSet,
                    EmailSendView,
                    UserViewSet)

from api.token import YamdbTokenObtainPairView

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='Review',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='Comments',
)


urlpatterns = [
    path('auth/email/', EmailSendView.as_view()),
    path(
        'auth/token/',
        YamdbTokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    path('', include(router.urls)),
]
