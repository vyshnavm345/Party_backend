from rest_framework import serializers

from .models import NewsFeed


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsFeed
        fields = "__all__"

    def validate_title(self, value):
        if NewsFeed.objects.filter(title=value).exists():
            raise serializers.ValidationError(
                "A news article with this title already exists."
            )
        return value
