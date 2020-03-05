from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from . import views
from .quiz import *
from django.urls import path
from slp_admin import views
  
from user_auth import *
from .views import *
from .show_user import *
# from .quiz import *

urlpatterns = [
    path('login/' , login_admin),
    path('logout/' , logout_admin),
    path('dashboard/' , dashboard),
    path('change_password/' , change_password),
    path('list_user/' , list_user),
    path('view_user/<str:id>/' , view_user),
    path('profile/' , user_profile),
    path('forget_password/' , forget_password),
    path('reset_password/<str:id>/' , reset_password),
    path('view_user/block/<str:id>/' , block_user),
    path('purchased_gifts',purchased_gift_page),
    # path('quiz/' , quiz),
    # path('quiz/add_question/' , add_question),
    path('qr-codes/', views.qr_codes, name='qr_codes'),
    path('dispute/requests/', views.dispute_requests, name='qr_codes'),
    path('contractors/',views.contractor_list),
    path('contractor/<int:contraId>/', views.contractor_dtl),
    path('points-request/', views.points_request),

    path('videos/add/', views.add_video, name='add-video'),
    re_path(r'videos/(?P<video_id>\d+)/edit/', views.edit_video, name='edit-video'),
    re_path(r'videos/(?P<video_id>\d+)/delete/', views.delete_video, name='delete-video'),
    path('videos/', views.videos, name='videos'),
    path('category/', views.category, name='category'),
    re_path(r'category/(?P<category_id>\d+)/delete/', views.delete_category, name='delete-category'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('quiz/', quiz, name='quiz'),
    path('quiz/add_question/', add_question),
    path('quiz/<int:quiz_id>/edit/', edit_quiz, name='edit-quiz'),
    path('quiz/<str:quiz_id>/delete/', delete_quiz),
    path('quiz/<str:quiz_id>/view/', view_quiz),

]


if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
