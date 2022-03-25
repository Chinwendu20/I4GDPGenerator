from django.shortcuts import render
from rest_framework.views import APIView 
from django.contrib.auth import get_user_model
from .models import User
from .serializers import PostSerializer, Post2Serializer, PhotoSerializer
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import cloudinary.uploader
from PIL import Image,ImageDraw
import urllib.request
from .models import Post
from django.contrib.sessions.models import Session
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
# Create your views here.



class PostView(APIView):
	serializer_class=PostSerializer
	parser_classes = (MultiPartParser,)
	@swagger_auto_schema(request_body=PostSerializer)
	def post(self, request, format=None):
		serializer=self.serializer_class(data=request.data)
		if serializer.is_valid():
			print(request.session)
			print(request.user)
			serializer.validated_data['Banner']=serializer.validated_data['file_uploaded']
			del serializer.validated_data['file_uploaded']
			request.session.create()
			serializer.validated_data['session']=Session.objects.get(pk=request.session.session_key)
			user_data=Post.objects.create(**serializer.validated_data)
			content={'Banner': user_data.Banner.url, 'Link': user_data.Link, 'Height': user_data.Height, 'Width': user_data.Width, 
			'Position_x': user_data.Position_x, 'Position_y': user_data.Position_y, 'Border_radius': user_data.Border_radius, 
			'Name': user_data.Name, 'Description':user_data.Description}
			if request.user != 'AnonymousUser':
				serializer.validated_data['user']=request.user
				content['user']=user_data.user	
			return Response(content, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostUpdateDestroyView(APIView):
	serializer_class=Post2Serializer
	parser_classes = (MultiPartParser,)
	@swagger_auto_schema(request_body=Post2Serializer)
	def put(self, request, id, format=None):
		# print(request.POST)
		# pk=request.POST['id']
		print(request.data)
		print(self.serializer_class(data=request.data))
		key=request.session.session_key
		sess=Session.objects.get(pk=key)
		post = Post.objects.filter(session=sess).filter(id=id)
		serializer = self.serializer_class(post[0], data=request.data)
		if serializer.is_valid():
			user_data=serializer.save()
			content={'Banner': user_data.Banner.url, 'Link': user_data.Link, 'Height': user_data.Height, 'Width': user_data.Width, 
			'Position_x': user_data.Position_x, 'Position_y': user_data.Position_y, 'Border_radius': user_data.Border_radius, 
			'Name': user_data.Name, 'Description':user_data.Description}
			if request.user != 'AnonymousUser':
				serializer.validated_data['user']=request.user
				content['user']=user_data.user	
			return Response(content, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request,id, format=None):
		key=request.session.session_key
		sess=Session.objects.get(pk=key)
		post = Post.objects.filter(session=sess).filter(id=id)
		post[0].delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class PostGetUserView(APIView):
	serializer_class=Post2Serializer
	parser_classes = (MultiPartParser,)
	def get (self, request, slug, format=None):
		try:
			user_data = Post.objects.get(Link=slug)
			serializer = self.serializer_class(user_data)
		except Post.DoesNotExist:
			return Response(status=status.HTTP_204_NO_CONTENT)
		
		content={'Banner': user_data.Banner.url, 'Link': user_data.Link, 'Height': user_data.Height, 'Width': user_data.Width, 
		'Position_x': user_data.Position_x, 'Position_y': user_data.Position_y, 'Border_radius': user_data.Border_radius, 
		'Name': user_data.Name, 'Description':user_data.Description}
		return Response(content, status=status.HTTP_200_OK)

class PostGetCreatorView(APIView):
	serializer_class=Post2Serializer
	parser_classes = (MultiPartParser,)
	def get(self, request, format=None):
		try:
			session=Session.objects.get(pk=request.session.session_key)
			post = Post.objects.filter(session=session)
			serializer = self.serializer_class(post, many=True)
		except Session.DoesNotExist:
			serializer=None
			return Response(serializer, status=status.HTTP_204_NO_CONTENT)

		return Response(serializer.data, status=status.HTTP_200_OK)


class PhotoManipulateView(APIView):
	serializer_class=PhotoSerializer
	parser_classes = (MultiPartParser,)
	@swagger_auto_schema(request_body=PhotoSerializer)
	def post(self, request, slug):
		serializer=self.serializer_class(data=request.data)
		if serializer.is_valid():
			Photo_uploaded=request.FILES['file_uploaded']
			Banner_object=Post.objects.get(Link=slug)
			width=int(Banner_object.Width)
			height=int(Banner_object.Height)
			position_x=int(Banner_object.Position_x)
			position_y=int(Banner_object.Position_y)
			banner=Banner_object.Banner.url
			urllib.request.urlretrieve(banner, "Banner.jpg")
			Banner_Image = Image.open("Banner.jpg")
			Size_of_Uploaded_Photo=(width, height)
			Photo_uploaded_Image = Image.open(Photo_uploaded).resize((Size_of_Uploaded_Photo))
			try:
				border_radius=int(Banner_object.Border_radius)
			except:
				border_radius=""
			if border_radius:
				border_radius=int(Banner_object.Border_radius)
				mask = Image.new("L", black_mask.size, 0)
				draw = ImageDraw.Draw(mask)
				draw.rounded_rectangle([0,0, width, height], radius=border_radius, fill=255)
				Banner_Image.paste(Photo_uploaded, (position_x, position_y), mask)
				upload_data = cloudinary.uploader.upload(Banner_Image)
			else:

				Banner_Image.paste(Photo_uploaded_Image, (position_x, position_y))
				Banner_Image.save('temp.jpg')
				upload_data = cloudinary.uploader.upload('temp.jpg')
			return Response({'Image': upload_data}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class PhotoManipulateCircleView(APIView):
# 	serializer_class=PostSerializer
# 	def post(self, request, slug):
# 		serializer=self.serializer_class(data=request.data)
# 		if serializer.is_valid():
# 			Photo_uploaded=request.FILES['file_uploaded']
# 			Banner=Post.objects.get(Link=slug)
# 			width=Banner_object.width
# 			height=Banner_object.Height
# 			position_x=Banner.Position_x
# 			position_y=Banner.Position_y
# 			Banner=Banner_object.Banner
# 			Banner_Image = Image.open(Banner)
# 			border_radius=Banner.Border_radius
# 			Size_of_Uploaded_Photo=(width, height)
# 			Photo_uploaded_Image = Image.open("ProfilePicture.jpg").resize((Size_of_Uploaded_Photo))
# 			mask = Image.new("L", black_mask.size, 0)
# 			draw = ImageDraw.Draw(mask)
# 			draw.rounded_rectangle([0,0, width, height], radius=border_radius, fill=255)
# 			Banner.paste(Photo_uploaded, (position_x, position_y), mask)
# 			upload_data = cloudinary.uploader.upload(Banner)
#             return Response({'Image': upload_data}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
