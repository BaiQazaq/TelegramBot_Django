from django.urls import path
from .views import Tg_dj_View

urlpatterns = [
    path('tg_dj/<str:token>/', Tg_dj_View.as_view(), name='tg_dj'),
]