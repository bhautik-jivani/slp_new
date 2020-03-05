from django.contrib import admin
from django.urls import path

from contractor import views
from contractor import apis
import user_auth as ua

urlpatterns = [
    # path('slp_admin/', slp_admin.site.urls),
    path('profile/', views.profile),
    # path('profile/updateProfile/',views.updateProfile),
    path('signin/', ua.login),
    path('check-signin/', views.checkLoginVal),
    path('dashboard/', views.dashboard),
    path('users/', views.users),
    path('user/<int:userId>/',apis.userDetails),
    path('products/', views.products),
    path('product/<int:productid>/',apis.productDetails),
    path('jobcategories/', apis.jobcategories),
    path('tasks/', apis.tasks),
    # path('tasks/additionalpoints/', apis.task_additional_points),
    path('tasks/<int:taskid>/delete/', apis.deleteTask),
    path('tasks-due-bills/', apis.taskduebils),
    path('signout/', views.signout),
    path('set_password',views.set_password),
    path('change_password/', views.change_password),
    path('checkemail/', views.reset_pass),
]