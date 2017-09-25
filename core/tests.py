import unittest
from django.core.urlresolvers import reverse
from django.test import Client
from .models import Game, Level, Script, Character, Media, Mechanic
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


def create_django_contrib_auth_models_user(**kwargs):
    defaults = {}
    defaults["username"] = "username"
    defaults["email"] = "username@tempurl.com"
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_django_contrib_auth_models_group(**kwargs):
    defaults = {}
    defaults["name"] = "group"
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_django_contrib_contenttypes_models_contenttype(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_game(**kwargs):
    defaults = {}
    defaults["name"] = "name"
    defaults["description"] = "description"
    defaults.update(**kwargs)
    if "users" not in defaults:
        defaults["users"] = create_django_contrib_auth_models_user()
    return Game.objects.create(**defaults)


def create_level(**kwargs):
    defaults = {}
    defaults["name"] = "name"
    defaults.update(**kwargs)
    if "game" not in defaults:
        defaults["game"] = create_game()
    if "script" not in defaults:
        defaults["script"] = create_script()
    if "characters" not in defaults:
        defaults["characters"] = create_character()
    if "medias" not in defaults:
        defaults["medias"] = create_media()
    if "mechanics" not in defaults:
        defaults["mechanics"] = create_mechanic()
    return Level.objects.create(**defaults)


def create_script(**kwargs):
    defaults = {}
    defaults["name"] = "name"
    defaults["description"] = "description"
    defaults["active"] = "active"
    defaults.update(**kwargs)
    return Script.objects.create(**defaults)


def create_character(**kwargs):
    defaults = {}
    defaults["name"] = "name"
    defaults["description"] = "description"
    defaults["active"] = "active"
    defaults.update(**kwargs)
    if "mechanics" not in defaults:
        defaults["mechanics"] = create_mechanic()
    return Character.objects.create(**defaults)


def create_media(**kwargs):
    defaults = {}
    defaults["name"] = "name"
    defaults["description"] = "description"
    defaults["url"] = "url"
    defaults["file"] = "file"
    defaults["type"] = "type"
    defaults.update(**kwargs)
    if "characters" not in defaults:
        defaults["characters"] = create_character()
    if "mechanics" not in defaults:
        defaults["mechanics"] = create_mechanic()
    return Media.objects.create(**defaults)


def create_mechanic(**kwargs):
    defaults = {}
    defaults["name"] = "name"
    defaults["description"] = "description"
    defaults["active"] = "active"
    defaults.update(**kwargs)
    return Mechanic.objects.create(**defaults)


class GameViewTest(unittest.TestCase):
    '''
    Tests for Game
    '''
    def setUp(self):
        self.client = Client()

    def test_list_game(self):
        url = reverse('core_game_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_game(self):
        url = reverse('core_game_create')
        data = {
            "name": "name",
            "description": "description",
            "users": create_django_contrib_auth_models_user().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_game(self):
        game = create_game()
        url = reverse('core_game_detail', args=[game.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_game(self):
        game = create_game()
        data = {
            "name": "name",
            "description": "description",
            "users": create_django_contrib_auth_models_user().pk,
        }
        url = reverse('core_game_update', args=[game.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class LevelViewTest(unittest.TestCase):
    '''
    Tests for Level
    '''
    def setUp(self):
        self.client = Client()

    def test_list_level(self):
        url = reverse('core_level_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_level(self):
        url = reverse('core_level_create')
        data = {
            "name": "name",
            "game": create_game().pk,
            "script": create_script().pk,
            "characters": create_character().pk,
            "medias": create_media().pk,
            "mechanics": create_mechanic().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_level(self):
        level = create_level()
        url = reverse('core_level_detail', args=[level.slug,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_level(self):
        level = create_level()
        data = {
            "name": "name",
            "game": create_game().pk,
            "script": create_script().pk,
            "characters": create_character().pk,
            "medias": create_media().pk,
            "mechanics": create_mechanic().pk,
        }
        url = reverse('core_level_update', args=[level.slug,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class ScriptViewTest(unittest.TestCase):
    '''
    Tests for Script
    '''
    def setUp(self):
        self.client = Client()

    def test_list_script(self):
        url = reverse('core_script_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_script(self):
        url = reverse('core_script_create')
        data = {
            "name": "name",
            "description": "description",
            "active": "active",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_script(self):
        script = create_script()
        url = reverse('core_script_detail', args=[script.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_script(self):
        script = create_script()
        data = {
            "name": "name",
            "description": "description",
            "active": "active",
        }
        url = reverse('core_script_update', args=[script.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class CharacterViewTest(unittest.TestCase):
    '''
    Tests for Character
    '''
    def setUp(self):
        self.client = Client()

    def test_list_character(self):
        url = reverse('core_character_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_character(self):
        url = reverse('core_character_create')
        data = {
            "name": "name",
            "description": "description",
            "active": "active",
            "mechanics": create_mechanic().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_character(self):
        character = create_character()
        url = reverse('core_character_detail', args=[character.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_character(self):
        character = create_character()
        data = {
            "name": "name",
            "description": "description",
            "active": "active",
            "mechanics": create_mechanic().pk,
        }
        url = reverse('core_character_update', args=[character.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class MediaViewTest(unittest.TestCase):
    '''
    Tests for Media
    '''
    def setUp(self):
        self.client = Client()

    def test_list_media(self):
        url = reverse('core_media_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_media(self):
        url = reverse('core_media_create')
        data = {
            "name": "name",
            "description": "description",
            "url": "url",
            "file": "file",
            "type": "type",
            "characters": create_character().pk,
            "mechanics": create_mechanic().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_media(self):
        media = create_media()
        url = reverse('core_media_detail', args=[media.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_media(self):
        media = create_media()
        data = {
            "name": "name",
            "description": "description",
            "url": "url",
            "file": "file",
            "type": "type",
            "characters": create_character().pk,
            "mechanics": create_mechanic().pk,
        }
        url = reverse('core_media_update', args=[media.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class MechanicViewTest(unittest.TestCase):
    '''
    Tests for Mechanic
    '''
    def setUp(self):
        self.client = Client()

    def test_list_mechanic(self):
        url = reverse('core_mechanic_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_mechanic(self):
        url = reverse('core_mechanic_create')
        data = {
            "name": "name",
            "description": "description",
            "active": "active",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_mechanic(self):
        mechanic = create_mechanic()
        url = reverse('core_mechanic_detail', args=[mechanic.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_mechanic(self):
        mechanic = create_mechanic()
        data = {
            "name": "name",
            "description": "description",
            "active": "active",
        }
        url = reverse('core_mechanic_update', args=[mechanic.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


