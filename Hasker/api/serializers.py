""" Serializer module for Hasker.api """

from Hasker.profile.models import HaskerUser
from Hasker.hasker.models import Question, Answer
from rest_framework import serializers


class HaskerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HaskerUser
        fields = ('username', 'email', 'avatar', 'password')
        write_only_fields = ('password', 'email', 'avatar')
        read_only_fields = ('username',)

    def create(self, validated_data):
        super().create(validated_data)
        # call set_password on user object. Without this
        # the password will be stored in plain text.
        user = HaskerUser(**validated_data)
        if user.password:
            user.set_password(user.password)
        return user

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        password = validated_data.pop('password', None)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('header', 'content', 'tags')
        read_only_fields = ('author',)

