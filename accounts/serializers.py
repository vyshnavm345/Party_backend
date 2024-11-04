from rest_framework import serializers

from .models import BaseUser, Candidate, Member


class OTPSendSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)


class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp_code = serializers.CharField(max_length=6)


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
            "Nic",
            "phone",
            "gender",
            "district",
            "constituency",
            "image",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = BaseUserSerializer.create(BaseUserSerializer(), validated_data=user_data)
        member = Member.objects.create(user=user, **validated_data)
        return member


class FlatMemberSerializer(serializers.ModelSerializer):
    # Define fields as properties to be fetched from the related user
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    date_of_birth = serializers.DateField(source="user.date_of_birth", read_only=True)
    image = serializers.SerializerMethodField()  # Use a method to get the image URL

    class Meta:
        model = Member
        fields = [
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "position_in_party",
            "Nic",
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


class CandidateSerializer(serializers.ModelSerializer):
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

    # def update(self, instance, validated_data):

    #     # Update candidate fields
    #     instance.constituency = validated_data.get('constituency', instance.constituency)
    #     instance.age = validated_data.get('age', instance.age)
    #     instance.party = validated_data.get('party', instance.party)
    #     instance.district = validated_data.get('district', instance.district)
    #     instance.image = validated_data.get('image', instance.image)
    #     instance.election_status = validated_data.get('election_status', instance.election_status)

    #     instance.save()
    #     return instance


class DistrictSerializer(serializers.Serializer):
    district = serializers.CharField(max_length=100)
