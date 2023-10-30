from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.index, name='index'),
   
    path('login/',views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name="register"),
    path('upload/', views.image_upload, name = 'upload'),
    path('face_reg/', views.face_reg, name="face_reg"),
    path('recognize/', views.recognize_face, name='recognize'),
    path('course/', views.course, name='course'),
    path('edit/<str:id>', views.edit, name='edit')
 
]

urlpatterns = urlpatterns+static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)