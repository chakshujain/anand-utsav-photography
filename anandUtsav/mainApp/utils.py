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


def getInGroups(iter_data, number_of_items_in_group):
    rows = []
    row = []
    for i in range(len(iter_data)):
        row.append(iter_data[i])
        if (i + 1) % number_of_items_in_group == 0:
            rows.append(row)
            row = []
        
    if (len(row)):
        rows.append(row)
    return rows