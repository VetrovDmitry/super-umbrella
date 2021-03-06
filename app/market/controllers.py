from werkzeug.datastructures import FileStorage
from base64 import b64encode
from imagekitio import ImageKit
from os import getenv

from . import models


class HouseController:
    model = models.House

    #  Checks

    def check_house_exists(self, house_id: int) -> dict:
        if self.model.find_by_id(house_id):
            return {'status': True, 'output': 'house: %s exists' % house_id}

        return {'status': False, 'output': 'house: %s does not exist' % house_id}

    def check_house_owner(self, house_id: int, user_id: int) -> dict:
        house = self.model.find_by_id(house_id)
        if user_id == house.user_id:
            return {'status': True, 'output': 'user %s has access to house' % user_id}

        return {'status': False, 'output': 'user %s has no access to house' % user_id}

    @staticmethod
    def check_photo_type(file_type):
        if file_type in models.PhotoTypes.get_values():
            return {'status': True, 'output': f"file_type: {file_type} is valid"}
        return {'status': False, 'output': f"file_type: {file_type} is not valid"}

    #  Creates

    def __new_house(self, city: str, street: str, house_number: str, cost: float, summary: str, user_id: int) -> int:
        new_house = self.model(
            city=city,
            street=street,
            house_number=house_number,
            cost=cost,
            summary=summary,
            user_id=user_id
        )
        new_house.upload()
        return new_house.id

    def create_house(self, house_data: dict) -> dict:
        new_house_id = self.__new_house(
            city=house_data['city'],
            street=house_data['street'],
            house_number=house_data['house_number'],
            cost=house_data['cost'],
            summary=house_data['summary'],
            user_id=house_data['user_id']
        )
        return {'message': f'house: {new_house_id} was created'}

    #  Changes

    def __change_house_fields(self, house_id: int, city: str, street: str, house_number: str, summary: str,
                              cost: float, photo: FileStorage) -> list:
        updated_field = list()
        house = self.model.find_by_id(house_id)
        if city != '':
            house.city = city
            updated_field.append('city')
        if street != '':
            house.street = street
            updated_field.append('street')
        if house_number != '':
            house.house_number = house_number
            updated_field.append('house_number')
        if summary != '':
            house.summary = summary
            updated_field.append('summary')
        if cost:
            house.cost = cost
            updated_field.append('cost')
        if photo:
            PhotoController.add_photo_to_house(house_id, photo)
            updated_field.append('photo')

        house.update()
        return updated_field

    def change_house_details(self, house_id: int, house_details: dict) -> dict:
        updated_fields = self.__change_house_fields(
            house_id=house_id,
            city=house_details['city'],
            street=house_details['street'],
            house_number=house_details['house_number'],
            summary=house_details['summary'],
            cost=house_details['cost'],
            photo=house_details['photo']
        )
        return {'message': f"{updated_fields} of house: {house_id} was updated"}

    #  Deletes

    def delete_house_by_id(self, house_id: int) -> dict:
        house = self.model.find_by_id(house_id)
        house.delete()
        return {'message': f"house: {house_id} was deleted successful"}

    #  Gets

    def get_house_public_info(self, house_id: int) -> dict:
        return self.model.find_by_id(house_id).public_json

    def get_houses_public_info(self) -> dict:
        houses_info = list()
        houses = self.model.find_all()
        for house in houses:
            houses_info.append(house.public_json)
        return {"houses": houses_info}

    #  Searching

    def search_house(self, house_data: dict) -> dict:
        houses = list()
        search_result = self.model.find_by_query(
            city=house_data['city'],
            street=house_data['street'],
            house_number=house_data['house_number'],
            cost=house_data['cost']
        )
        for house in search_result:
            houses.append(house.public_json)

        return {'houses': houses}


class PhotoController:
    model = models.Photo
    allowed_image_type = models.PhotoTypes.get_values()
    remote_folder = 'houses_photo'
    imagekit = ImageKit(
        private_key=getenv('IMAGEKIT_PRIVATE'),
        public_key=getenv('IMAGEKIT_PUBLIC'),
        url_endpoint=getenv('IMAGEKIT_URL')
    )

    @staticmethod
    def extract_file_types(file: FileStorage) -> tuple:
        return str(file.content_type).split('/')

    @classmethod
    def upload_photo(cls, file: FileStorage, filename: str) -> dict:
        return cls.imagekit.upload_file(
            file=b64encode(file.read()),
            file_name=filename,
            options={'folder': cls.remote_folder}
        )['response']

    @classmethod
    def create_photo(cls, house_id: int, filename: str, file_type: enumerate, file_id: str, url: str) -> int:
        new_photo = cls.model(
            house_id=house_id,
            filename=filename,
            file_type=file_type,
            file_id=file_id,
            url=url
        ).upload()
        return new_photo.id

    @classmethod
    def add_photo_to_house(cls, house_id: int, photo: FileStorage) -> dict:
        uploaded_photo = cls.upload_photo(photo, 'house_photo')

        _, file_type = cls.extract_file_types(photo)

        created_photo_id = cls.create_photo(
            house_id=house_id,
            filename=uploaded_photo['name'],
            file_type=file_type,
            file_id=uploaded_photo['fileId'],
            url=uploaded_photo['url']
        )
        return {'message': f"photo: {created_photo_id} was created"}



