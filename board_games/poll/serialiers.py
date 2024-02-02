from rest_framework import serializers

from .models import Question, Choice
from user_action.models import Vote
from user_action.serialiers import VoteResponseSerializer


class ChoiceRequestSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField(required=True)

    class Meta:
        model = Choice
        fields = ['question_id', 'choice_text']


class ChoiceResponseSerializer(serializers.ModelSerializer):
    user_votes = serializers.SerializerMethodField('get_user_votes')

    def get_user_votes(self, choice_id):
        match_user_votes = Vote.objects.filter(choice_id=choice_id)
        return VoteResponseSerializer(match_user_votes, many=True).data

    class Meta:
        model = Choice
        fields = ['id', 'question_id', 'choice_text', 'votes', 'user_votes']


class QuestionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_text', 'picture']


class QuestionResponseSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField('get_choices')

    def get_choices(self, question_id):
        match_choices = Choice.objects.filter(question_id=question_id)
        return ChoiceResponseSerializer(match_choices, many=True).data

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'picture', 'choices']
