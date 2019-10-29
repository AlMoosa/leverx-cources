# from allauth.account.adapter import DefaultAccountAdapter


# class CustomAccountAdapter(DefaultAccountAdapter):

#     def save_user(self, request, user, form, commit=False):
#         user = super().save_user(request, user, form, commit)
#         data = form.cleaned_data
#         user.is_student = data.get('is_student')
#         user.is_teacher = data.get('is_teacher')
#         user.save()
#         return user
