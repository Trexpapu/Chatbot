from django.shortcuts import render
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Chat import ChatLogic as ch
from Chat.serializers import AnswerSerializer, QuestionSerializer
from Chat.models import Answer, Question
from rest_framework import viewsets



class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

@api_view(['GET', 'POST'])
def chatbot(request):
    if request.method == 'POST':
        # Obtener la cadena de texto de la solicitud
        message = request.data.get('message', '')

        # Lógica del chatbot (aquí puedes integrar tu lógica de procesamiento de texto)
        response = ch.chatbot(message)

        # Devolver la respuesta
        print(response)
        return Response({'response': response})
    
    elif request.method == 'GET':
        # En caso de solicitudes GET, podrías devolver una respuesta predeterminada o renderizar un formulario
        return Response({'response': 'Estas son las preguntas más frecuentes: ¿Como hacer mi servcio social?. ¿Como seguir tramite de titulación?. ¿Cuales son los edificios de la FIE?'})
