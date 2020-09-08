from django.contrib import admin
from .models import MyProfile, MyPost, PostLike, PostComment, FollowUser


admin.site.register(MyProfile)
admin.site.register(MyPost)
admin.site.register(PostComment)
admin.site.register(PostLike)
admin.site.register(FollowUser)

# Register your models here.
