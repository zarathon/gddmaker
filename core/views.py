from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import user_is_collaborator_in_game
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, render_to_response
from django.urls import reverse
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from . import forms
from . import models
from reversion import revisions
import reversion
from .utils import render_to_pdf


@login_required(login_url='index', )
def dashboard(request):
    games = request.user.game_set.all()
    context = {
        'games': games,
    }
    return render(request, 'core/dashboard.html', context=context)


def index(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is None:
            error = "Usuário ou senha inválidos"
            return render(request, 'core/index.html', {'error': error})
        else:
            login(request, user)
            return HttpResponseRedirect(reverse('core:dashboard'))
    return render(request, 'core/index.html')


def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        login = request.POST['login']
        password = request.POST['password']

        if User.objects.filter(username=login):
            return render(request, 'core/register.html', {'error': 'Login já em uso por outro usuário!'})

        if User.objects.filter(email=email):
            return render(request, 'core/register.html', {'error': 'Já existe um usuário cadastrado com esse email!'})

        user = User.objects.create_user(login, email, password)
        user.first_name = name
        user.save()
        send_mail('Cadastro Realizado!', 'Bem vindo ao GDDMaker. Construa seu GDD agora com muito mais facilidade.',
                  'gddmaker@gddmaker.com', [email], fail_silently=False)

        message = "Cadastro Realizado com sucesso!"

        return render(request, 'core/index.html', {'message': message})

    return render(request, 'core/register.html')


def logout_view(request):
    logout(request)
    return render(request, 'core/index.html')


@login_required(login_url='index', )
def create_game(request):
    if request.method == 'POST':
        with revisions.create_revision():
            game = models.Game()
            form = forms.GameForm(request.POST, instance=game)
            new_game = form.save()
            new_game.users.add(request.user)
            new_game.save()
            revisions.set_user(request.user)
        return HttpResponseRedirect(reverse('core:game_detail', args=[new_game.id]))
    else:
        form = forms.GameForm()
    return render(request, 'core/game_form.html', {'form': form})


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_detail(request, *args, **kwargs):
    game = get_object_or_404(models.Game, pk=kwargs.get('game_pk'))
    context = {
        'game': game
    }
    return render(request, 'core/game_detail.html', context=context)


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_edit(request, *args, **kwargs):
    game = get_object_or_404(models.Game, pk=kwargs.get('game_pk'))
    if request.method == 'POST':
        with revisions.create_revision():
            form = forms.GameForm(request.POST, instance=game)
            if form.is_valid():
                form.save()
                revisions.set_user(request.user)
                return HttpResponseRedirect(reverse('core:game_detail', args=[game.id]))
            else:
                context = {
                    'form': form,
                    'game': game
                }
                return render(request, 'core/game_form_edit.html', context=context)
    else:
        form = forms.GameForm(instance=game)
        context = {
            'form': form,
            'game': game
        }
    return render(request, 'core/game_form_edit.html', context=context)


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_remove(request, *args, **kwargs):
    game = get_object_or_404(models.Game, pk=kwargs.get('game_pk'))
    with revisions.create_revision():
        game.delete()
        revisions.set_user(request.user)
    return HttpResponseRedirect(reverse('core:dashboard'))

@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_history(request, *args, **kwargs):
    game = get_object_or_404(models.Game, pk=kwargs.get('game_pk'))
    versions = reversion.models.Version.objects.get_for_object(game)

    context = {
        'game': game,
        'versions': versions
    }

    return render(request, 'core/game_history.html', context=context)


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_user_add(request, *args, **kwargs):
    game = get_object_or_404(models.Game, pk=kwargs.get('game_pk'))
    user = None
    try:
        user = User.objects.get(username=request.POST['colaborador-input'])
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=request.POST['colaborador-input'])
        except User.DoesNotExist:
            pass
        pass

    if user is None:
        messages.error(request, 'Colaborador não cadastrado.')
    else:
        game.users.add(user)
        game.save()
        send_mail('Você foi adicionado como colaborador!', 'Você foi adicionado como colaborador no jogo '+ game.name +'. Visite agora a ferramenta GDDMaker para colaborar na construção desse incrível jogo.',
                  'gddmaker@gddmaker.com', [user.email], fail_silently=False)
        messages.success(request, 'Colaborador adicionado ao jogo')
    return HttpResponseRedirect(reverse('core:game_detail', args=[game.id]))


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_user_remove(request, *args, **kwargs):
    game = get_object_or_404(models.Game, pk=kwargs.get('game_pk'))
    user = get_object_or_404(User, pk=kwargs.get('user_pk'))
    game.users.remove(user)
    game.save()
    messages.success(request, 'Colaborador removido do jogo')
    return HttpResponseRedirect(reverse('core:game_detail', args=[game.id]))


@login_required(login_url='index', )
def game_generatePDF(request, *args, **kwargs):
    game = get_object_or_404(models.Game, pk=kwargs.get('game_pk'))
    context = {
        'game': game,
        'app_url': request.get_host(),
    }
    pdf = render_to_pdf('gddpdf.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_level_add(request, *args, **kwargs):
    game = get_object_or_404(models.Game, pk=kwargs.get('game_pk'))
    if request.method == 'POST':
        with revisions.create_revision():
            level = models.Level()
            level.game = game
            form = forms.LevelForm(request.POST, instance=level, game=level.game)
            if form.is_valid():
                level = form.save()
                level.save()
                revisions.set_user(request.user)
                return HttpResponseRedirect(reverse('core:game_level_detail', args=[game.id, level.id]))
            else:
                return render(request, 'core/game_level_add.html', {'form': form, 'game': game})
    else:
        form = forms.LevelForm(game=game)
        return render(request, 'core/game_level_add.html', {'form': form, 'game': game})


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_level_detail(request, *args, **kwargs):
    level = get_object_or_404(models.Level, pk=kwargs.get('level_pk'))
    return render(request, 'core/game_level_detail.html', {'level': level, 'game': level.game})


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_level_remove(request, *args, **kwargs):
    game = get_object_or_404(models.Game, pk=kwargs.get('game_pk'))
    level = get_object_or_404(models.Level, pk=kwargs.get('level_pk'))
    with revisions.create_revision():
        level.delete()
        revisions.set_user(request.user)
    return HttpResponseRedirect(reverse('core:game_detail', args=[game.id]))


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_level_edit(request, *args, **kwargs):
    level = get_object_or_404(models.Level, pk=kwargs.get('level_pk'))
    if request.method == 'POST':
        with revisions.create_revision():
            form = forms.LevelForm(request.POST, instance=level, game=level.game)
            if form.is_valid():
                form.save()
                revisions.set_user(request.user)
                messages.success(request, 'Fase alterada com sucesso')
                return HttpResponseRedirect(reverse('core:game_level_detail', args=[level.game.id, level.id]))
            else:
                return render(request, 'core/game_level_edit.html', {'form': form, 'game': level.game})
    else:
        form = forms.LevelForm(instance=level, game=level.game)
        return render(request, 'core/game_level_edit.html', {'form': form, 'game': level.game})


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_level_history(request, *args, **kwargs):
    level = get_object_or_404(models.Level, pk=kwargs.get('level_pk'))
    versions = reversion.models.Version.objects.get_for_object(level)
    context = {
        'game': level.game,
        'level': level,
        'versions': versions
    }
    return render(request, 'core/game_level_history.html', context=context)


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_level_list(request, *args, **kwargs):
    game = get_object_or_404(models.Game, pk=kwargs.get('game_pk'))
    context = {
        'game': game,
    }
    return render(request, 'core/game_level_list.html', context=context)


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_character_add(request, *args, **kwargs):
    game = get_object_or_404(models.Game, pk=kwargs.get('game_pk'))
    if request.method == 'POST':
        with revisions.create_revision():
            character = models.Character()
            character.game = game
            form = forms.CharacterForm(request.POST, instance=character, game=game)
            if form.is_valid():
                character = form.save()
                character.save()
                revisions.set_user(request.user)
                return HttpResponseRedirect(reverse('core:game_character_detail', args=[game.id, character.id]))
            else:
                return render(request, 'core/game_character_add.html', {'form': form, 'game': game})
    else:
        form = forms.CharacterForm(game=game)
        return render(request, 'core/game_character_add.html', {'form': form, 'game': game})


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_character_detail(request, *args, **kwargs):
    character = get_object_or_404(models.Character, pk=kwargs.get('character_pk'))
    return render(request, 'core/game_character_detail.html', {'character': character, 'game': character.game})


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_character_remove(request, *args, **kwargs):
    game = get_object_or_404(models.Game, pk=kwargs.get('game_pk'))
    character = get_object_or_404(models.Character, pk=kwargs.get('character_pk'))
    with revisions.create_revision():
        character.delete()
        revisions.set_user(request.user)
    return HttpResponseRedirect(reverse('core:game_detail', args=[game.id]))


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_character_edit(request, *args, **kwargs):
    character = get_object_or_404(models.Character, pk=kwargs.get('character_pk'))
    if request.method == 'POST':
        with revisions.create_revision():
            form = forms.CharacterForm(request.POST, instance=character, game=character.game)
            if form.is_valid():
                form.save()
                revisions.set_user(request.user)
                messages.success(request, 'Personagem alterado com sucesso')
                return HttpResponseRedirect(reverse('core:game_character_detail', args=[character.game.id, character.id]))
            else:
                return render(request, 'core/game_character_edit.html', {'form': form, 'game': character.game})
    else:
        form = forms.CharacterForm(instance=character, game=character.game)
        return render(request, 'core/game_character_edit.html', {'form': form, 'game': character.game})


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_character_history(request, *args, **kwargs):
    character = get_object_or_404(models.Character, pk=kwargs.get('character_pk'))
    versions = reversion.models.Version.objects.get_for_object(character)
    context = {
        'game': character.game,
        'character': character,
        'versions': versions
    }
    return render(request, 'core/game_character_history.html', context=context)


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_character_list(request, *args, **kwargs):
    game = get_object_or_404(models.Game, pk=kwargs.get('game_pk'))
    context = {
        'game': game,
    }
    return render(request, 'core/game_character_list.html', context=context)


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_mechanic_add(request, *args, **kwargs):
    game = get_object_or_404(models.Game, pk=kwargs.get('game_pk'))
    if request.method == 'POST':
        with revisions.create_revision():
            mechanic = models.Mechanic()
            mechanic.game = game
            form = forms.MechanicForm(request.POST, instance=mechanic, game=game)
            if form.is_valid():
                mechanic = form.save()
                mechanic.save()
                revisions.set_user(request.user)
                return HttpResponseRedirect(reverse('core:game_mechanic_detail', args=[game.id, mechanic.id]))
            else:
                return render(request, 'core/game_mechanic_add.html', {'form': form, 'game': game})
    else:
        form = forms.MechanicForm(game=game)
        return render(request, 'core/game_mechanic_add.html', {'form': form, 'game': game})


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_mechanic_detail(request, *args, **kwargs):
    mechanic = get_object_or_404(models.Mechanic, pk=kwargs.get('mechanic_pk'))
    return render(request, 'core/game_mechanic_detail.html', {'mechanic': mechanic, 'game': mechanic.game})


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_mechanic_remove(request, *args, **kwargs):
    game = get_object_or_404(models.Game, pk=kwargs.get('game_pk'))
    mechanic = get_object_or_404(models.Mechanic, pk=kwargs.get('mechanic_pk'))
    with revisions.create_revision():
        mechanic.delete()
        revisions.set_user(request.user)
    return HttpResponseRedirect(reverse('core:game_detail', args=[game.id]))


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_mechanic_edit(request, *args, **kwargs):
    mechanic = get_object_or_404(models.Mechanic, pk=kwargs.get('mechanic_pk'))
    if request.method == 'POST':
        with revisions.create_revision():
            form = forms.MechanicForm(request.POST, instance=mechanic, game=mechanic.game)
            if form.is_valid():
                form.save()
                revisions.set_user(request.user)
                messages.success(request, 'Mecânica alterada com sucesso')
                return HttpResponseRedirect(reverse('core:game_mechanic_detail', args=[mechanic.game.id, mechanic.id]))
            else:
                return render(request, 'core/game_mechanic_edit.html', {'form': form, 'game': mechanic.game})
    else:
        form = forms.MechanicForm(instance=mechanic, game=mechanic.game)
        return render(request, 'core/game_mechanic_edit.html', {'form': form, 'game': mechanic.game})


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_mechanic_history(request, *args, **kwargs):
    mechanic = get_object_or_404(models.Mechanic, pk=kwargs.get('mechanic_pk'))
    versions = reversion.models.Version.objects.get_for_object(mechanic)
    context = {
        'game': mechanic.game,
        'mechanic': mechanic,
        'versions': versions
    }
    return render(request, 'core/game_mechanic_history.html', context=context)


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_mechanic_list(request, *args, **kwargs):
    game = get_object_or_404(models.Game, pk=kwargs.get('game_pk'))
    context = {
        'game': game,
    }
    return render(request, 'core/game_mechanic_list.html', context=context)


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_media_add(request, *args, **kwargs):
    game = get_object_or_404(models.Game, pk=kwargs.get('game_pk'))
    if request.method == 'POST':
        media = models.Media()
        media.game = game
        form = forms.MediaForm(request.POST, request.FILES, instance=media,)
        if form.is_valid():
            media = form.save()
            media.save()
            return HttpResponseRedirect(reverse('core:game_media_detail', args=[game.id, media.id]))
        else:
            return render(request, 'core/game_media_add.html', {'form': form, 'game': game})
    else:
        form = forms.MediaForm()
        return render(request, 'core/game_media_add.html', {'form': form, 'game': game})


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_media_detail(request, *args, **kwargs):
    media = get_object_or_404(models.Media, pk=kwargs.get('media_pk'))
    return render(request, 'core/game_media_detail.html', {'media': media, 'game': media.game})


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_media_remove(request, *args, **kwargs):
    game = get_object_or_404(models.Game, pk=kwargs.get('game_pk'))
    media = get_object_or_404(models.Media, pk=kwargs.get('media_pk'))
    media.delete()
    return HttpResponseRedirect(reverse('core:game_detail', args=[game.id]))


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_media_edit(request, *args, **kwargs):
    media = get_object_or_404(models.Media, pk=kwargs.get('media_pk'))
    if request.method == 'POST':
        form = forms.MediaForm(request.POST, request.FILES, instance=media)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mídia alterada com sucesso')
            return HttpResponseRedirect(reverse('core:game_media_detail', args=[media.game.id, media.id]))
        else:
            return render(request, 'core/game_media_edit.html', {'form': form, 'game': media.game})
    else:
        form = forms.MediaForm(instance=media)
        return render(request, 'core/game_media_edit.html', {'form': form, 'game': media.game})


@login_required(login_url='index', )
@user_is_collaborator_in_game
def game_media_list(request, *args, **kwargs):
    game = get_object_or_404(models.Game, pk=kwargs.get('game_pk'))
    context = {
        'game': game,
    }
    return render(request, 'core/game_media_list.html', context=context)


# HTTP Error 403
def permission_denied(request):
    response = render_to_response(
        '403.html',
        context={'request': request}
    )
    response.status_code = 403
    return response


# HTTP ERROR 404
def miss_resource(request):
    response = render_to_response(
        '404.html',
        context= {'request', request}
    )
    response.status_code = 404
    return response


# HTTP ERROR 500
def error_backend(request):
    response = render_to_response(
        '500.html',
        context={'request', request}
    )
    response.status_code = 500
    return response
