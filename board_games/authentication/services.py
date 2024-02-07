# from django.db.models import F
# from django.db.models.signals import pre_save
#
# from .models import CustomUser
#
#
# def my_callback(sender, instance, created, **kwargs):
#     vote = instance
#     choice = vote.choice
#     choice.n_votes = F('n_votes') + 1
#     choice.save(update_fields='n_votes')
#
#
# pre_save.connect(my_callback, sender=CustomUser)