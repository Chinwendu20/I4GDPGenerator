from django.shortcuts import render
from rest_framework.views import APIView 
from django.contrib.auth import get_user_model
from .models import User
from .serializers import UserSerializer
import binascii
import os
from .models import SignupCode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# Create your views here.



class SignUpView(APIView):
	permission_classes = (AllowAny,)
	serializer_class=UserSerializer
	def post(self, request, format=None):
		serializer=self.serializer_class(data=request.data)
		if serializer.is_valid():
			email=serializer.validated_data['email']
			try:
				user_=User.objects.get(email=email)
				try:
					signup_code=SignupCode.objects.get(user=user_)
					signup_code.delete()

				except SignupCode.DoesNotExist:
					pass
			except User.DoesNotExist:
				del serializer.validated_data['Confirm_Password']
				serializer.validated_data['is_active']=False
				user_=User.objects.create_user(**serializer.validated_data)
				# user_.is_active=False				
			code=binascii.hexlify(os.urandom(20)).decode('utf-8')
			signup=SignupCode.objects.create(user=user_, code=code)
			subject= render_to_string('Email_files/verify_subject.txt')
			body=render_to_string('Email_files/verification_email.txt', {'code':signup.code})
			user_.email_user(subject, body)
			content={'message': 'User created, check mail for verification'}
			return Response(content, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignUpVerify(APIView):
	permission_classes = (AllowAny,)
	def get (self, request, format=None):
		code=request.GET['code']
		try:
			signupcode=SignupCode.objects.get(code=code)
			user=signupcode.user
			user.is_active=True
			user.save()
			content={'message': 'User verified'}
			return Response(content, status=status.HTTP_201_CREATED)
		except SignupCode.DoesNotExist:
			content={'message': 'Unable to verify user'}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)





