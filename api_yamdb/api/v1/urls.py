from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
)
from .views import (
    AdminViewSet,
    GetTokenClass,
    RegistrationClass,
)

router = DefaultRouter()
router_v1 = DefaultRouter()

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment',
)
router_v1.register(r'users', AdminViewSet)
router.register('categories', CategoryViewSet, basename='categoties')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
urlpatterns = [
    path('', include(router.urls)),
    path('', include(router_v1.urls)),
    path(r'auth/signup/', RegistrationClass.as_view()),
    path(r'auth/token/', GetTokenClass.as_view()),
]
