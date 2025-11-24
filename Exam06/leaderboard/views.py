from rest_framework.decorators import api_view
from rest_framework.response import Response
from scores.models import Score
from players.models import Player

@api_view(['GET'])
def game_leaderboard(request):
    game_id = request.query_params.get('game_id')
    if not game_id:
        return Response({'error': 'game_id is required'}, status=400)
    scores = Score.objects.filter(game_id=game_id)
    players = {}
    for s in scores:
        if s.player.id not in players:
            players[s.player.id] = {'player': s.player.nickname, 'country': s.player.country, 'points': 0, 'wins':0, 'draws':0,'losses':0, 'player_id': s.player.id}
        players[s.player.id]['points'] += s.points
        if s.result == 'win':
            players[s.player.id]['wins'] += 1
        elif s.result == 'draw':
            players[s.player.id]['draws'] += 1
        else:
            players[s.player.id]['losses'] += 1
    leaderboard = sorted(players.values(), key=lambda x: x['points'], reverse=True)
    for i, p in enumerate(leaderboard):
        p['rank'] = i+1
        p['rating'] = Player.objects.get(id=p['player_id']).rating
        p['rating_change'] = p['points']
    return Response(leaderboard)

@api_view(['GET'])
def top_players_leaderboard(request):
    game_id = request.query_params.get('game_id')
    limit = int(request.query_params.get('limit', 10))
    scores = Score.objects.filter(game_id=game_id)
    players = {}
    for s in scores:
        if s.player.id not in players:
            players[s.player.id] = {'player': s.player.nickname, 'country': s.player.country, 'points': 0, 'player_id': s.player.id}
        players[s.player.id]['points'] += s.points
    leaderboard = sorted(players.values(), key=lambda x: x['points'], reverse=True)[:limit]
    for i, p in enumerate(leaderboard):
        p['rank'] = i+1
        p['rating'] = Player.objects.get(id=p['player_id']).rating
    return Response({
        'game_id': game_id,
        'limit': limit,
        'total_players': len(players),
        'leaderboard': leaderboard
    })

@api_view(['GET'])
def global_leaderboard(request):
    country = request.query_params.get('country')
    limit = int(request.query_params.get('limit', 100))
    qs = Player.objects.all()
    if country:
        qs = qs.filter(country__iexact=country)
    leaderboard = qs.order_by('-rating')[:limit]
    data = []
    for i, p in enumerate(leaderboard):
        data.append({'rank': i+1, 'player': p.nickname, 'rating': p.rating, 'total_games': p.score_set.count()})
    return Response({
        'total_players': qs.count(),
        'country': country,
        'leaderboard': data
    })
