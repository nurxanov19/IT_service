from django.urls import path
from .views import home, sign_up, create_post, PostUpdate, PostDetail, profile_view, ask_profile

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('sign-up/', sign_up, name='sign_up'),
    path('create-post/', create_post, name='create_post'),
    path('update-post/<int:pk>', PostUpdate.as_view(), name='update-post'),
    path('detail-post/<int:pk>', PostDetail.as_view(), name='detail-post'),
    path('profile/', profile_view, name='profile'),
    path('ask-profile/', ask_profile, name='ask-profile'),

]