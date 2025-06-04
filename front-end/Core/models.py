
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Existing fields (from your form)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    company = models.CharField(max_length=255, blank=True)
    age = models.IntegerField(null=True, blank=True)
    topics = models.JSONField(default=list)      # ["medicine", "biology"]
    subtopics = models.JSONField(default=list)   # ["ai", "genetics"]
    
    # ✅ New field for actions
    user_activity = models.JSONField(default=dict)

    def update_activity(self, article_id, action):
        article_data = self.user_activity.get(article_id, {
            "clicks": [],
            "likes": [],
            "favorites": [],
            "time_spent": [],
            "searches": [],
            "last_active": str(now())
        })

        if action == "click":
            article_data["clicks"].append("1")
        elif action == "like":
            article_data["likes"].append("1")
        elif action == "dislike":
            article_data["likes"].append("0")
        elif action == "favourite":
            article_data["favorites"].append("1")

        article_data["last_active"] = str(now())
        self.user_activity[article_id] = article_data
        self.save()
