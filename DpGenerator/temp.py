import urllib.request
from PIL import Image,ImageDraw
from Photo.models import Post

urllib.request.urlretrieve(Post.objects.get(id=1).Banner.url, "Banner")
Image.open('Banner')