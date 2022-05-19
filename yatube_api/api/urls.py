from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

app_name = 'api'

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('follow', FollowViewSet, basename='followers')
router.register('groups', GroupViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments',
                CommentViewSet, basename='comments')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),

]
