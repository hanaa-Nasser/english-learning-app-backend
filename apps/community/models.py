from django.db import models

# Create your models here.

class CommunityPost(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='community_posts', null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.name} on {self.created_at}"


class CommunityReply(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='replies',null=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='community_replies',null=True)
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.name} on Post {self.post.id}"
