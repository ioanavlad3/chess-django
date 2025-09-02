from django.db import models

# Create your models here.


class UserRegistration(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username
    

class Game(models.Model):
    player_white = models.CharField(max_length=150)
    player_black = models.CharField(max_length=150, blank=True, null=True)
    board_fen = models.TextField(default='startpos')  # initial board state
    turn = models.CharField(max_length=5, default='white')
    is_active = models.BooleanField(default=True)
    room_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    white_rematch = models.BooleanField(default=False)  # if the white player wants a rematch
    black_rematch = models.BooleanField(default=False)
    winner = models.CharField(max_length=10, null=True, blank=True)
    time_per_player = models.IntegerField(default=5)



# class GameRematchStatus(models.Model):
#     room = models.CharField(max_length=100, unique=True)
#     player_white = models.CharField(max_length=100)
#     player_black = models.CharField(max_length=100)
#     white_ready = models.BooleanField(default=False)
#     black_ready = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Rematch status for room {self.room}"