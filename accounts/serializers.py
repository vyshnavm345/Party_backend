from django.db import transaction
from rest_framework import serializers

from .models import BaseUser, Candidate, District, Member


class OTPSendSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)


class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp_code = serializers.CharField(max_length=6)
    device_token = serializers.CharField(max_length=255, required=False, allow_blank=True)
    

class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ["first_name", "last_name", "email", "date_of_birth"]

    def create(self, validated_data):
        user = BaseUser.objects.create(**validated_data)
        return user


class MemberSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = Member
        fields = [
            "user",
            "position_in_party",
            "nic",
            "phone",
            "gender",
            "district",
            "constituency",
            "image",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        try:
            with transaction.atomic():
                user = BaseUser.objects.create(**user_data)
                member = Member.objects.create(user=user, **validated_data)
            return member
        except Exception as e:
            raise serializers.ValidationError(f"Error creating member: {str(e)}")


class FlatMemberSerializer(serializers.ModelSerializer):
    # Define fields as properties to be fetched from the related user
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    date_of_birth = serializers.DateField(source="user.date_of_birth", read_only=True)
    image = serializers.SerializerMethodField()  # Use a method to get the image URL
    district = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = [
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "position_in_party",
            "nic",
            "phone",
            "gender",
            "district",
            "constituency",
            "image",
        ]

    def get_image(self, obj):
        """Return the image URL or None if no image is uploaded."""
        if obj.image:
            return obj.image.url
        return None

    def get_district(self, obj):
        # Return the district's name or 'None' if no district is set
        return obj.district.name if obj.district else "None"


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ["id", "name"]


class CandidateSerializer(serializers.ModelSerializer):
    district = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = [
            "id",
            "first_name",
            "last_name",
            "fathers_name",
            "age",
            "address",
            "party",
            "district",
            "image",
            "state",
            "education",
            "date_of_birth",
            "email",
            "phone",
            "gender",
            "election_status",
            "biography",
        ]

    def create(self, validated_data):
        # Check if the email already exists
        if Candidate.objects.filter(email=validated_data["email"]).exists():
            raise serializers.ValidationError(
                {"email": "This email is already in use."}
            )

        # Check if the phone number already exists
        if Candidate.objects.filter(phone=validated_data["phone"]).exists():
            raise serializers.ValidationError(
                {"phone": "This phone number is already in use."}
            )

        candidate = Candidate.objects.create(**validated_data)
        return candidate

    def get_district(self, obj):
        # Return the district's name or 'None' if no district is set
        return obj.district.name if obj.district else "None"
