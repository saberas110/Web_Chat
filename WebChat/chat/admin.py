from django.contrib import admin
from .models import Conversation, Message, UserProfile,UserProfileImages,Contact



admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(UserProfile)
admin.site.register(UserProfileImages)
admin.site.register(Contact)
