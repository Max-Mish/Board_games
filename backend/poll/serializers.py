from rest_framework import serializers

from user_action.models import Vote
from user_action.serializers import VoteResponseSerializer
from .models import Question, Choice


class ChoiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['choice_text']


class ChoiceResponseSerializer(serializers.ModelSerializer):
    user_votes = serializers.SerializerMethodField('get_user_votes')

    def get_user_votes(self, choice_id):
        match_user_votes = Vote.objects.filter(choice_id=choice_id)
        return VoteResponseSerializer(match_user_votes, many=True).data

    class Meta:
        model = Choice
        fields = '__all__'


class QuestionRequestSerializer(serializers.ModelSerializer):
    choices = ChoiceRequestSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'


class QuestionResponseSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField('get_choices')

    def get_choices(self, question_id):
        match_choices = Choice.objects.filter(question_id=question_id)
        return ChoiceResponseSerializer(match_choices, many=True).data

    class Meta:
        model = Question
        fields = '__all__'
