from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
	Confirm_Password = serializers.CharField(max_length=100)

	def validate_password(self,value):
		data=self.get_initial()
		password=value
		if password != data.get('Confirm_Password'):
			raise serializers.ValidationError("Passwords do not match") 
		return value

	def validate_email(self, value):
		data=self.get_initial()
		try:
			user=User.objects.get(email=data.get('email'))
		except User.DoesNotExist:
			return value
			
		if user.is_active:
				raise serializers.ValidationError("Email is already registered")



	class Meta:
		model=User
		fields=['username', 'first_name', 'last_name', 'email', 'password', 'Confirm_Password']


