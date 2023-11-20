from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import User, Video
from .forms import VideoForm
import cv2
import os
import numpy as np

# admin:admin123

def index(request):
    if request.POST:
        # try:
        e = request.POST['email']
        u = get_object_or_404(User, email = e)
        print(u.password) 
        # except (KeyError, User.DoesNotExist) :
        #     return render(request, "login.html", {
        #         'error_message': "Invalid username !!!"
        #         }
        #     ) 
        return render(request, "index.html", {})
    else:
        return render(request, "index.html", {})

def login(request):
    if request.POST:
        print(request.POST)
        a = User(username = request.POST['username'], email = request.POST['email'], firstname = request.POST['firstname'], lastname = request.POST['lastname'], password = request.POST['password'], plan = request.POST['plan'])
        a.save()
    return render(request, "login.html", {})

def signup(request):
    return render(request, "sign-up.html", {})

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        tit = request.POST['title']

        vid = request.FILES.get('video_file')
        file_path = default_storage.save(f"encoded/{tit}.mp4", ContentFile(vid.read()))
        print(file_path)
        encoded_image = encode(image_name="black.png", secret_data="{ip: '106.15.25.43', email:'aaa@gmail.com'}", video = vid, path = file_path)
        # print(encoded_image)
        # cv2.imwrite("encoded_image.png", encoded_image)
        # encoded_video = embed(output_image, video)
        # form.Meta.model = embed(output_image, vid)
        # print(form.Meta.model)
        if form.is_valid():
            Video.objects.create(url = file_path, video_file=vid, title=tit)
            # form.save()
            # return render(request, 'index.html', {})
            return redirect('../admin')  # Redirect to a page showing all uploaded videos
    else:
        form = VideoForm()
        return render(request, 'upload_video.html', {'form': form})

# ================================================================================================================================
def encode(image_name, secret_data, video, path):
    width, height = findVideoDim(path)
    # read the image
    image = cropImage(image_name, width, height)
    # maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    # convert data to binary
    binary_secret_data = to_bin(secret_data)
    # size of data to hide
    data_len = len(binary_secret_data)
    print("[*] Maximum number of bits we can encode:", n_bytes*8)
    print("[*] Number of bits to encode:", data_len)
    if len(secret_data) > n_bytes:  
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
    print("[+] Encoding data...")
    # add stopping criteria
    secret_data += "====="
    data_index = 0
    for row in image:
        for pixel in row:
            # convert RGB values to binary format
            r, g, b = to_bin(pixel)
            # modify the least significant bit only if there is still data to store
            if data_index < data_len:
                # least significant red pixel bit
                pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant green pixel bit
                pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant blue pixel bit
                pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            # if data is encoded, just break out of the loop
            if data_index >= data_len:
                break
    return image

def findVideoDim(video): # To find dimension of the video
    vcap = cv2.VideoCapture(video)
    if vcap.isOpened():
        width  = round(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))   # float `width`
        height = round(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
        print(f"[*] Dimension of the given video: {width}p x {height}p")
        return (width, height)
    else:
        print("[!] Error opening video ! Exiting ...")
        exit()

def cropImage(img, width, height): # To crop the image into video dimension
    image = cv2.imread(img)
    y=0
    x=0
    crop = image[y:y+height, x:x+width].copy()
    return crop

def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes):
        return ''.join([ format(i, "08b") for i in data ])
    elif isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")
