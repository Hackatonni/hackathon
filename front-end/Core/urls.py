from django.urls import path
from . views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('article/<int:article_id>/', article_detail_view, name='article_detail'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    path('upload/', upload_article_view, name='upload_article'),
    # path('onboarding/<str:username>/', onboarding_view, name='onboarding'),
    
    path('onboarding/<str:username>/', onboarding_view, name='onboarding'),
    path('onboarding-response/', onboarding_response_view, name='onboarding_response'),

    
    path('recommended/', recommended_view, name='recommended'),
    path('search/', search_view, name='search'),
    path('api/interaction/', user_interaction_api, name='user_interaction_api'),
]

APPEND_SLASH = False