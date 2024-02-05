from rest_framework import serializers

from .models import Question, Choice
from user_action.models import Vote
from user_action.serialiers import VoteResponseSerializer


class ChoiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['choice_text']


class ChoiceResponseSerializer(serializers.ModelSerializer):
    user_votes = serializers.SerializerMethodField('get_user_votes')
    amount_per_choice = serializers.SerializerMethodField('get_amount_per_choice')

    def get_user_votes(self, choice_id):
        match_user_votes = Vote.objects.filter(choice_id=choice_id)
        return VoteResponseSerializer(match_user_votes, many=True).data

    def get_amount_per_choice(self, choice_id):
        return len(self.get_user_votes(choice_id=choice_id))

    class Meta:
        model = Choice
        fields = ['id', 'question_id', 'choice_text', 'votes', 'user_votes', 'amount_per_choice']


class QuestionRequestSerializer(serializers.ModelSerializer):
    choices = ChoiceRequestSerializer(many=True)

    class Meta:
        model = Question
        fields = ['question_text', 'picture', 'choices']


class QuestionResponseSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField('get_choices')
    amount_all = serializers.SerializerMethodField('get_amount_all')

    def get_choices(self, question_id):
        match_choices = Choice.objects.filter(question_id=question_id)
        return ChoiceResponseSerializer(match_choices, many=True).data

    def get_amount_all(self, question_id):
        return sum([choice['amount_per_choice'] for choice in self.get_choices(question_id=question_id)])

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'picture', 'choices', 'amount_all']
