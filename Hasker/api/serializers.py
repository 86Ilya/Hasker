from Hasker.profile.models import HaskerUser
from Hasker.hasker.models import Question, Answer, Tag
from rest_framework import serializers


class HaskerUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HaskerUser
        fields = ('username', 'email', 'avatar', 'password')

    def create(self, validated_data):
        super().create(validated_data)
        user = HaskerUser(**validated_data)
        if user.password:
            user.set_password(user.password)
        return user


class HaskerUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HaskerUser
        fields = ('email', 'avatar', 'password')

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'tag_name')


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    tags = TagSerializer(many=True)

    class Meta:
        model = Question
        fields = ('author', 'header', 'content', 'tags')


class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Answer
        fields = ('author', 'content')
