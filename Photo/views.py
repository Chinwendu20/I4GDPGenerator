from django.shortcuts import render
from rest_framework.views import APIView 
from django.contrib.auth import get_user_model
from .models import User
from .serializers import PostSerializer, Post2Serializer, PhotoSerializer, StaxSerializer, StaxLinkSerializer
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import cloudinary.uploader
from PIL import Image,ImageDraw,ImageFont
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
			qs=[]
			for user_data in post:
				content={'Banner': user_data.Banner.url, 'Link': user_data.Link, 'Height': user_data.Height, 'Width': user_data.Width, 
				'Position_x': user_data.Position_x, 'Position_y': user_data.Position_y, 'Border_radius': user_data.Border_radius, 
				'Name': user_data.Name, 'Description':user_data.Description} 
				qs.append(content)
			# 	post.Banner=post.Banner.url
			# 	post.save()
			serializer = self.serializer_class(post, many=True)
		except Session.DoesNotExist:
			serializer=None
			return Response(serializer, status=status.HTTP_204_NO_CONTENT)

		return Response(qs, status=status.HTTP_200_OK)

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
			format_=Banner_object.Banner.format
			image_name= "Banner.{}".format(format_)
			urllib.request.urlretrieve(banner, image_name)
			Banner_Image = Image.open(image_name)
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
			else:

				Banner_Image.paste(Photo_uploaded_Image, (position_x, position_y))
				print(Photo_uploaded)
				Banner_Image.save('{}'.format(Photo_uploaded))
				upload_data = cloudinary.uploader.upload('{}'.format(Photo_uploaded))
			return Response({'Image': upload_data}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaxMainView(APIView):
	serializer_class=StaxSerializer
	parser_classes = (MultiPartParser,)
	@swagger_auto_schema(request_body=serializer_class)
	def post(self, request, slug):
		serializer=self.serializer_class(data=request.data)
		if serializer.is_valid():
			Photo_uploaded=request.FILES['file_uploaded']
			Banner_qs=Post.objects.filter(Link='staxcampus')
			Banner_object=Banner_qs[0]
			width=int(Banner_object.Width)
			height=int(Banner_object.Height)
			position_x=int(Banner_object.Position_x)
			position_y=int(Banner_object.Position_y)
			name=serializer.validated_data['Name']
			university=serializer.validated_data['University']
			banner=Banner_object.Banner.url
			format_=Banner_object.Banner.format
			image_name= "Banner.{}".format(format_)
			urllib.request.urlretrieve(banner, image_name)
			Banner_Image = Image.open(image_name).resize((547, 547))
			Size_of_Uploaded_Photo=(width, height)
			Photo_uploaded_Image = Image.open(Photo_uploaded).resize((Size_of_Uploaded_Photo))
			border_radius=int(Banner_object.Border_radius)
			border_radius=int(Banner_object.Border_radius)
			maski = Image.new("L", Photo_uploaded_Image.size, 0)
			draw = ImageDraw.Draw(maski)
			draw.rounded_rectangle([0,0,width,height], radius=border_radius, fill=255)
			Banner_Image.paste(Photo_uploaded_Image,box=(position_x, position_y), mask=maski)
			draw = ImageDraw.Draw(Banner_Image)
			font = ImageFont.truetype("font/Effra Bold.ttf", 25)
			w,h = font.getsize(name)
			font1 = ImageFont.truetype("font/Effra_Std_Rg.ttf", 16)
			w1,h1 = font1.getsize(university)
			img_size=Banner_Image.size
			draw.text(((547-w)/2,407), name, fill =(255,255,255), font=font)
			draw.text(((547-w1)/2,440), university, fill =(255,255,255), font=font1)
			Banner_Image.save('{}.png'.format(Photo_uploaded))
			upload_data = cloudinary.uploader.upload('{}.png'.format(Photo_uploaded))
			return Response({'Image': upload_data}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaxLinkView(APIView):
	serializer_class=StaxLinkSerializer
	parser_classes = (MultiPartParser,)
	@swagger_auto_schema(request_body=serializer_class)
	def post(self, request):
		serializer=self.serializer_class(data=request.data)
		if serializer.is_valid():
			Photo_uploaded=request.FILES['file_uploaded']
			Banner_qs=Post.objects.filter(Link='linkStax')
			Banner_object=Banner_qs[0]
			width=int(Banner_object.Width)
			height=int(Banner_object.Height)
			position_x=int(Banner_object.Position_x)
			position_y=int(Banner_object.Position_y)
			name=serializer.validated_data['Name']
			Link=serializer.validated_data['Link']
			banner=Banner_object.Banner.url
			format_=Banner_object.Banner.format
			image_name= "Banner.{}".format(format_)
			urllib.request.urlretrieve(banner, image_name)
			Banner_Image = Image.open(image_name).resize((547, 547))
			Size_of_Uploaded_Photo=(width, height)
			Photo_uploaded_Image = Image.open(Photo_uploaded).resize((Size_of_Uploaded_Photo))
			border_radius=int(Banner_object.Border_radius)
			border_radius=int(Banner_object.Border_radius)
			maski = Image.new("L", Photo_uploaded_Image.size, 0)
			draw = ImageDraw.Draw(maski)
			draw.rounded_rectangle([0,0,width,height], radius=border_radius, fill=255)
			Banner_Image.paste(Photo_uploaded_Image,box=(position_x, position_y), mask=maski)
			draw = ImageDraw.Draw(Banner_Image)
			font = ImageFont.truetype("font/Effra Bold.ttf", 22)
			w,h = font.getsize(name)
			font1 = ImageFont.truetype("font/Effra Bold.ttf", 10)
			w1,h1 = font1.getsize(Link)
			img_size=Banner_Image.size
			draw.text((209, 72), name, fill =(255,255,255), font=font)
			draw.text(((547-w1)/2,462), Link, fill =(255,255,255), font=font1)
			Banner_Image.save('{}.png'.format(Photo_uploaded))
			upload_data = cloudinary.uploader.upload('{}.png'.format(Photo_uploaded))
			return Response({'Image': upload_data}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)