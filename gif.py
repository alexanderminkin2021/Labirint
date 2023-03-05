import cv2
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

gif = cv2.VideoCapture('Folder/Left.gif')
ret,frame = gif.read() # ret=True if it finds a frame else False. Since your gif contains only one frame, the next read() will give you ret=False
img = Image.fromarray(frame)
img = img.convert('RGB')
cv2.imshow('new',img)


