# serializers.py

from rest_framework import serializers

from .models import BaseUser, Member


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


# class CandidateSerializer(serializers.ModelSerializer):
#     member = MemberSerializer(read_only=True)  # Nested member serializer

#     class Meta:
#         model = Candidate
#         fields = ['id', 'member', 'constituency', 'party_affiliation', 'election_status']

#     def create(self, validated_data):
#         member_data = validated_data.pop('member')
#         member = Member.objects.create(**member_data)
#         candidate = Candidate.objects.create(member=member, **validated_data)
#         return candidate
