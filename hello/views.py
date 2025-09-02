from django.shortcuts import render, redirect
from .models import UserRegistration, Game

from django.http import HttpResponse

# hello/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# In-memory storage (for simplicity; use a database like Django models in production)
#latest_fen = "rnbqkbnr/pppp1ppp/5n2/5p2/5P2/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1"
#room_fens = {}  # Dictionary to store FEN per room

latest_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"  # Standard starting position
room_fens = {}

rematch_flags = {}

@csrf_exempt
def submit_move(request):
    global latest_fen, room_fens
    if request.method == "POST":
        data = json.loads(request.body)
        fen = data.get('fen')
        room = data.get('room', 'defaultRoom')
        if fen:
            room_fens[room] = fen
            latest_fen = fen  # Update global FEN
            return JsonResponse({'status': 'success', 'fen': fen})
    return JsonResponse({'status': 'error', 'message': 'Invalid move data'}, status=400)

def get_latest_move(request):
    room = request.GET.get('room', 'defaultRoom')
    fen = room_fens.get(room, latest_fen)
    return JsonResponse({'fen': fen})

def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = UserRegistration.objects.get(username=username, password=password)
            # Save username in session
            request.session['username'] = user.username
            return redirect('welcome')
        except UserRegistration.DoesNotExist:
            return render(request, 'hello/loginPage.html', {'error': 'Incorect Username or Password'})
    return render(request, 'hello/loginPage.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # save to db
        UserRegistration.objects.create(username=username, password=password)
        return redirect('home') 
    return render(request, 'hello/registerPage.html')
# Create your views here.

def welcome(request):
    username = request.session.get('username')
    if not username:
        return redirect('home')
    return render(request, 'hello/welcome.html', {'username': username})

import uuid

def generate_unique_room_name():
    while True:
        code = f'room-{uuid.uuid4().hex[:6]}'
        if not Game.objects.filter(room_name=code).exists():
            return code

def create_room(request):
    username = request.session.get('username')
    user = UserRegistration.objects.get(username=username)
    
    if request.method == "POST":
        time_per_player = int(request.POST.get('time_per_player', 5))
        room_code = generate_unique_room_name()
        game = Game.objects.create(
            player_white=username,
            room_name=room_code,
            time_per_player=time_per_player
        )
        return redirect('game', game_id=game.id)

    return redirect('welcome')


def join_room_list(request):
    # Show only games where black player hasn't joined yet
    username = request.session.get('username')
    user = UserRegistration.objects.get(username=username)
    game.player_black = user

    games = Game.objects.filter(player_black__isnull=True)
    return render(request, 'hello/join_room_list.html', {'games': games})

# Join a specific room
def join_room(request, game_id):
    username = request.session.get('username')
    user = UserRegistration.objects.get(username=username)

    game = Game.objects.get(id=game_id)
    if game.player_black is None:
        game.player_black = username
        game.save()
    return redirect('game', game_id=game.id)


def game(request, game_id):
    game = Game.objects.get(id=game_id)
    username = request.session.get('username')
    if not username:
        return redirect('home')
    return render(request, 'hello/game.html', {'game': game,
                                               'username': username,
                                               'room_name': f'game{game_id}',
                                               'time_per_player': game.time_per_player
                                               })

def index(request):
    return render(request, 'hello/welcome.html')

def get_game_state(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
        return JsonResponse({
            'player_white': game.player_white,
            'player_black': game.player_black if game.player_black else 'Waiting for player',
        })
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)
 
@csrf_exempt
def request_rematch(request):
    data = json.loads(request.body)
    room = data.get('room')
    username = data.get('username')

    try:
        game = Game.objects.get(room_name=room)
    except Game.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Game not found'}, status=404)

    # set the rematch request 
    user = UserRegistration.objects.get(username=username)
    if user == game.player_white:
        game.white_rematch = True
    elif user == game.player_black:
        game.black_rematch = True
    else:
        return JsonResponse({'status': 'error', 'message': 'Not a player'}, status=403)

    game.save()

    # see if both players want to rematch
    if game.white_rematch and game.black_rematch:
        # Create a new game
        new_room = f'rematch-{uuid.uuid4().hex[:6]}'
        new_game = Game.objects.create(
            player_white=game.player_white,
            player_black=game.player_black,
            room_name=new_room
        )
        # Reset the rematch request for the current game
        game.white_rematch = False
        game.black_rematch = False
        game.save()
        return JsonResponse({'status': 'ready', 'new_game_id': new_game.id})

    return JsonResponse({'status': 'waiting'})

def user_history(request):
    username = request.session.get('username')
    if not username:
        return redirect('home')

    games = Game.objects.filter(player_white=username) | Game.objects.filter(player_black=username)
    games = games.order_by('-created_at')

    return render(request, 'hello/history.html', {'games': games})


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def save_winner(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        game_id = data.get('game_id')
        winner = data.get('winner')

        try:
            game = Game.objects.get(id=game_id)
            game.winner = winner
            game.save()
            return JsonResponse({'status': 'ok'})
        except Game.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Game not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
