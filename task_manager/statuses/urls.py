from django.urls import path
from task_manager.statuses.views import StatusListView, \
                                        StatusCreateView


urlpatterns = [
    path('', StatusListView.as_view(), name='status_list'),
    path('create/', StatusCreateView.as_view(), name='status_create'),
]

# GET /statuses/ — страница со списком всех статусов
# GET /statuses/create/ — страница создания статуса
# POST /statuses/create/ — создание нового статуса
# GET /statuses/<int:pk>/update/ — страница редактирования статуса
# POST /statuses/<int:pk>/update/ — обновление статуса
# GET /statuses/<int:pk>/delete/ — страница удаления статуса
# POST /statuses/<int:pk>/delete/ — удаление статуса
