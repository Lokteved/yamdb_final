from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from rest_framework.views import APIView
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from rest_framework.response import Response
from rest_framework import viewsets, filters, mixins
from api_yamdb import settings

from .models import Category, Genre, Title, User, Comments, Review
from .filters import TitleFilter
from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly, IsAdmin
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          TitleViewSerializer,
                          EmailSerializer,
                          UserSerializer,
                          CommentSerializer,
                          ReviewSerializer)


class EmailSendView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(
            email=request.data['email'],
            username=request.data['username'],
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Confirmation email',
            f'Your confirmatin_code: {confirmation_code}',
            settings.SENDER_EMAIL,
            [request.data['email']],
            fail_silently=False,
        )
        return Response(serializer.validated_data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username',]
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    @action(detail=False, 
            methods=['get', 'patch'], 
            permission_classes=[IsAuthenticated])
    def me(self, request):
        username = request.user.username
        instance = get_object_or_404(User, username=username)
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        if request.method == 'PATCH':
            serializer.save()
        return Response(serializer.data)


class LabelViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class CategoryViewSet(LabelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(LabelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (Title.objects.prefetch_related('review')
                .annotate(rating=Avg('review__score')))
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('name',)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleViewSerializer
        return TitleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs['review_id']
        queryset = Comments.objects.filter(review_id=review_id)
        return queryset

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        queryset = Review.objects.filter(title_id=title_id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        context['title'] = title
        context['author'] = self.request.user
        return context

    def perform_create(self, serializer):
        serializer.save(
            author=serializer.context['author'],
            title=serializer.context['title']
        )
