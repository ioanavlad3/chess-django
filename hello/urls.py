from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('welcome/', views.welcome, name='welcome'),
    path('create_room/', views.create_room, name='create_room'),
    path('join_room_list/', views.join_room_list, name='join_room_list'),
    path('join_room/<int:game_id>/', views.join_room, name='join_room'),
    path('game/<int:game_id>/', views.game, name='game'),
    path('', views.index, name='index'),
    path('game/<str:room_name>/', views.game, name='game'),
    path('submit-move/', views.submit_move, name='submit_move'),
    path('get-latest-move/', views.get_latest_move, name='get_latest_move'),
    path('get-game-state/<int:game_id>/', views.get_game_state, name='get_game_state'),
 #   path('request-rematch/', views.request_rematch, name='request_rematch'),
    path('history/', views.user_history, name='history'),
    path('save-winner/', views.save_winner, name='save_winner'),

]
