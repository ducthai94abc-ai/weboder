from django.urls import path
from . import views

urlpatterns = [
    # Các path nạp tiền và lịch sử cũ của bạn
    path('deposit/', views.deposit, name='deposit'),
    path('history/', views.history, name='history'),

    # THÊM 3 ĐƯỜNG DẪN CHAT MỚI VÀO ĐÂY:
    path('chat/', views.chat_room, name='chat_room'),
    path('chat/send/', views.send_message, name='send_message'),
    path('chat/get/', views.get_messages, name='get_messages'),

    # THÊM ĐƯỜNG DẪN ĐĂNG KÝ VÀO ĐÂY:
    path('register/', views.register, name='register'),
]