from rest_framework import serializers

from .models import Event, NewsFeed


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


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "heading", "description", "image", "date"]

    def create(self, validated_data):
        return Event.objects.create(**validated_data)


# class EventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = ['id', 'heading', 'description', 'image', 'date']

#     def create(self, validated_data):
#         # Generate or set defaults for required Page fields
#         validated_data['title'] = validated_data.get('heading', 'Default Title')
#         validated_data['slug'] = slugify(validated_data.get('heading', 'default-title'))
#         validated_data['path'] = "some/default/path"  # Adjust as needed for the Wagtail structure
#         validated_data['depth'] = 1  # Adjust based on your site's page hierarchy

#         # Create the Event instance with the updated validated_data
#         return super().create(validated_data)
