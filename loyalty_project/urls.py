from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('redeem/<int:reward_id>/', views.redeem_reward, name='redeem_reward'),
    path('deposit/', views.deposit, name='deposit'),
    path('history/', views.history, name='history'),
    
   # THÊM 3 DÒNG XỬ LÝ CHAT NÀY:
    path('chat/', views.chat_room, name='chat_room'),
    path('chat/send/', views.send_message, name='send_message'),
    path('chat/get/', views.get_messages, name='get_messages'),

    # THÊM ĐƯỜNG DẪN ĐĂNG KÝ VÀO ĐÂY:
    path('register/', views.register, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)