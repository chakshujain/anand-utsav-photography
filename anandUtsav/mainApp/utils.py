from PIL import Image

RESIZE = 1000

def resizeImage(path):
    im = Image.open(path)
    w, h= im.size
    print("dim ", w, h)
    ratio = w/h
    h = RESIZE
    size = h*ratio, h
    print("new dim ", h*ratio, h)

    im.thumbnail(size, Image.ADAPTIVE)
    print("saving to", path)
    im.save(path, "JPEG")

    return h*ratio, h
