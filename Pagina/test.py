import urllib.request as req

imgurl ="https://scontent-iad3-1.cdninstagram.com/v/t51.2885-15/e35/56191689_311853672837178_5702585242739437692_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=110&_nc_ohc=rPOY9ukWKjUAX-ad4L_&oh=429b736008dfb4af6213e6b0a0e39eb6&oe=5EA60F0D"
req.urlretrieve(imgurl, "prof_img/image_name.jpg")