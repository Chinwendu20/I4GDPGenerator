from .models import Post
from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from authentication.models import User


class PostSerializer(serializers.ModelSerializer):
	file_uploaded=serializers.FileField(validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png'])])

	class Meta:
		model=Post
		exclude = ('Banner', 'session')

	def validate_Link(self, value):
		data=self.get_initial()
		post=Post.objects.filter(Link=data.get('Link'))
		if len(post) == 0:
			return value			
		raise serializers.ValidationError("Link already in use")


	def create(self, validated_data):
		validated_data['Banner']=validated_data['file_uploaded']
		del validated_data['file_uploaded']	
		validated_data['session']=request.session	 
		user_data=Post.objects.create(**validated_data)
		return user_data

class Post2Serializer(serializers.ModelSerializer):
	
	class Meta:
		model=Post
		exclude = ('session',)

class PhotoSerializer(serializers.Serializer):
	file_uploaded=serializers.FileField(validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png'])])

class StaxSerializer(serializers.Serializer):
	file_uploaded=serializers.FileField(validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png'])])
	Name=serializers.CharField()
	University=serializers.CharField()


class StaxLinkSerializer(serializers.Serializer):
	file_uploaded=serializers.FileField(validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png'])])
	Name=serializers.CharField()
	Link=serializers.CharField()