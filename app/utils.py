import os


STANDART_IMAGES = {
    'house': 'images/standart_photo.png',
    'profile': 'images/profile_photo.png'
}


def get_image(path, mode='house'):
    if path is None or path == '':
        return STANDART_IMAGES.get(mode)

    image = os.path.join('app/static/uploads', path)
    if os.path.isfile(image):
        return 'uploads/' + path