from django.conf.urls import url, include
from rest_framework import routers
from . import api
from . import views

router = routers.DefaultRouter()
router.register(r'game', api.GameViewSet)
router.register(r'level', api.LevelViewSet)
router.register(r'character', api.CharacterViewSet)
router.register(r'media', api.MediaViewSet)
router.register(r'mechanic', api.MechanicViewSet)

app_name = 'core'

urlpatterns = (
    # urls for Django Rest Framework API
    url(r'^api/v1/', include(router.urls)),
)
urlpatterns += (
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^game/new$', views.create_game, name='game_new'),
    url(r'^game/edit/(?P<game_pk>\S+)/$', views.game_edit, name='game_edit'),
    url(r'^game/remove/(?P<game_pk>\S+)/$', views.game_remove, name='game_remove'),
    url(r'^game/(?P<game_pk>\S+)/user/add$', views.game_user_add, name='game_user_add'),
    url(r'^game/(?P<game_pk>\S+)/user/remove/(?P<user_pk>\S+)$', views.game_user_remove, name='game_user_remove'),
    url(r'^game/(?P<game_pk>\S+)/$', views.game_detail, name='game_detail'),
    url(r'^game/(?P<game_pk>\S+)/history$', views.game_history, name='game_history'),
    url(r'^game/(?P<game_pk>\S+)/pdf$', views.game_generatePDF, name='game_pdf'),
)

urlpatterns += (
    url(r'^game/(?P<game_pk>\S+)/level/add$', views.game_level_add, name='game_level_add'),
    url(r'^game/(?P<game_pk>\S+)/level/list$', views.game_level_list, name='game_level_list'),
    url(r'^game/(?P<game_pk>\S+)/level/remove/(?P<level_pk>\S+)$', views.game_level_remove, name='game_level_remove'),
    url(r'^game/(?P<game_pk>\S+)/level/edit/(?P<level_pk>\S+)$', views.game_level_edit, name='game_level_edit'),
    url(r'^game/(?P<game_pk>\S+)/level/history/(?P<level_pk>\S+)$', views.game_level_history, name='game_level_history'),
    url(r'^game/(?P<game_pk>\S+)/level/(?P<level_pk>\S+)$', views.game_level_detail, name='game_level_detail'),

)

urlpatterns += (
    url(r'^game/(?P<game_pk>\S+)/character/add$', views.game_character_add, name='game_character_add'),
    url(r'^game/(?P<game_pk>\S+)/character/list$', views.game_character_list, name='game_character_list'),
    url(r'^game/(?P<game_pk>\S+)/character/remove/(?P<character_pk>\S+)$', views.game_character_remove, name='game_character_remove'),
    url(r'^game/(?P<game_pk>\S+)/character/edit/(?P<character_pk>\S+)$', views.game_character_edit, name='game_character_edit'),
    url(r'^game/(?P<game_pk>\S+)/character/history/(?P<character_pk>\S+)$', views.game_character_history, name='game_character_history'),
    url(r'^game/(?P<game_pk>\S+)/character/(?P<character_pk>\S+)$', views.game_character_detail, name='game_character_detail'),
)

urlpatterns += (
    url(r'^game/(?P<game_pk>\S+)/mechanic/add$', views.game_mechanic_add, name='game_mechanic_add'),
    url(r'^game/(?P<game_pk>\S+)/mechanic/list$', views.game_mechanic_list, name='game_mechanic_list'),
    url(r'^game/(?P<game_pk>\S+)/mechanic/remove/(?P<mechanic_pk>\S+)$', views.game_mechanic_remove, name='game_mechanic_remove'),
    url(r'^game/(?P<game_pk>\S+)/mechanic/edit/(?P<mechanic_pk>\S+)$', views.game_mechanic_edit, name='game_mechanic_edit'),
    url(r'^game/(?P<game_pk>\S+)/mechanic/history/(?P<mechanic_pk>\S+)$', views.game_mechanic_history, name='game_mechanic_history'),
    url(r'^game/(?P<game_pk>\S+)/mechanic/(?P<mechanic_pk>\S+)$', views.game_mechanic_detail, name='game_mechanic_detail'),
)

urlpatterns += (
    url(r'^game/(?P<game_pk>\S+)/media/add$', views.game_media_add, name='game_media_add'),
    url(r'^game/(?P<game_pk>\S+)/media/list$', views.game_media_list, name='game_media_list'),
    url(r'^game/(?P<game_pk>\S+)/media/remove/(?P<media_pk>\S+)$', views.game_media_remove, name='game_media_remove'),
    url(r'^game/(?P<game_pk>\S+)/media/edit/(?P<media_pk>\S+)$', views.game_media_edit, name='game_media_edit'),
    url(r'^game/(?P<game_pk>\S+)/media/(?P<media_pk>\S+)$', views.game_media_detail, name='game_media_detail'),
)