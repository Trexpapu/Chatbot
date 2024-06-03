"""
URL configuration for ChatBot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Chat import views as chat_views  # Importa las vistas de tu aplicación Chat
from Chat.views import AnswerViewSet, QuestionViewSet
from rest_framework.routers import DefaultRouter
# Define el enrutador para los ViewSets
router = DefaultRouter()
router.register(r'answers', AnswerViewSet)
router.register(r'questions', QuestionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chatbot', chat_views.chatbot),  # Ruta para manejar la URL raíz
    path('', include(router.urls)), # Agrega las URLs de los ViewSets
]
