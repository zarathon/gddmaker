from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from . import models


def user_is_collaborator_in_game(function):
    def wrap(request, *args, **kwargs):
        game = get_object_or_404(models.Game, pk=kwargs.get('game_pk'))
        if game.users.filter(id=request.user.id).count() == 1:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap