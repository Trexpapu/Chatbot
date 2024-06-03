from rest_framework import serializers
from .models import Answer, Question

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    answerID = serializers.PrimaryKeyRelatedField(queryset=Answer.objects.all())
    answer_info = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['questionID', 'question', 'answerID', 'answer_info']
    
    def get_answer_info(self, obj):
        answer = obj.answerID
        return {
            'answer': answer.answer
        }