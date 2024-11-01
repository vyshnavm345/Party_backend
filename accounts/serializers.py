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
    date_of_birth = serializers.EmailField(source="user.date_of_birth", read_only=True)

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


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            "first_name",
            "last_name",
            "constituency",
            "age",
            "party",
            "district",
            "image",
            "election_status",
        ]

    def create(self, validated_data):
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
