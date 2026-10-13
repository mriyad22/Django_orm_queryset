from django.urls import path
from .views import *


urlpatterns = [
    path('', dashboard, name='dashboard'),

    #-----> User create
    path('register/', user_register, name='register_page'),
    path('login/', user_login, name="login_page"),
    path('logout/', user_logout, name='logout'),

    #------> profiel url
    path('profile/', profile_view, name='profile'),
    path('profile-update/', update_profile, name='profile_update'),

    #------> job url
    path('jobs/', job_display, name='jobs'),
    path('create-job/', create_job, name='create_job'),
    path('apply/<int:a_id>/', job_application, name='apply'),

    #-----> application url
    path('candidate/<str:c_id>/', candidate_view, name="candidate")
]
