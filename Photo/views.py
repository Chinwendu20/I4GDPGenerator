from django.shortcuts import render
from rest_framework.views import APIView 
from django.contrib.auth import get_user_model
from .models import User
from .serializers import PostSerializer, Post2Serializer 
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import cloudinary.uploader
from PIL import Image,ImageDraw
import urllib.request
from .models import Post
from django.contrib.sessions.models import Session
# Create your views here.



class PostView(APIView):
	serializer_class=PostSerializer
	def post(self, request, format=None):
		serializer=self.serializer_class(data=request.data)
		if serializer.is_valid():
			print(request.session.session_key)
			print(request.user)
			serializer.validated_data['Banner']=serializer.validated_data['file_uploaded']
			del serializer.validated_data['file_uploaded']
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
	serializer_class=PostSerializer
	def put(self, request, format=None):
		pk=request.GET['id']
		Post = self.get_object(pk)
		serializer = self.serializer_class(Post, data=request.data)
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

	def delete(self, request, format=None):
		pk=request.GET['id']
		Post = self.get_object(pk)
		Post.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)






class PostGetUserView(APIView):
	serializer_class=Post2Serializer
	def get (self, request, slug, format=None):
		try:
			post = Post.objects.get(Link=slug)
			serializer = self.serializer_class(post)
		except Post.DoesNotExist:
			return Response(status=status.HTTP_204_NO_CONTENT)

		return Response(serializer.data, status=status.HTTP_200_OK)

class PostGetCreatorView(APIView):
	serializer_class=Post2Serializer

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
	serializer_class=Post2Serializer
	def post(self, request, slug):
		serializer=self.serializer_class(data=request.data)
		if serializer.is_valid():
			Photo_uploaded=request.FILES['file_uploaded']
			Banner_object=Post.objects.get(Link=slug)
			width=Banner_object.width
			height=Banner_object.Height
			position_x=Banner.Position_x
			position_y=Banner.Position_y
			border_radius=Banner.Border_radius
			Banner=Banner_object.Banner.url
			urllib.request.urlretrieve(Banner, "Banner")
			Banner_Image = Image.open(Banner)
			Size_of_Uploaded_Photo=(width, height)
			Photo_uploaded_Image = Image.open("ProfilePicture.jpg").resize((Size_of_Uploaded_Photo))
			if border_radius:
				mask = Image.new("L", black_mask.size, 0)
				draw = ImageDraw.Draw(mask)
				draw.rounded_rectangle([0,0, width, height], radius=border_radius, fill=255)
				Banner.paste(Photo_uploaded, (position_x, position_y), mask)
				upload_data = cloudinary.uploader.upload(Banner)
			else:

				Banner.paste(Photo_uploaded_Image, (position_x, position_y))
				upload_data = cloudinary.uploader.upload(Banner)
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
