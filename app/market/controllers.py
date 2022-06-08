from . import models


class HouseController:
    model = models.House

    #  Checks

    def check_house_exists(self, house_id: int) -> dict:
        if self.model.find_by_id(house_id):
            return {'status': True, 'output': 'house: %s exists' % house_id}

        return {'status': False, 'output': 'house: %s does not exist' % house_id}

    #  Creates

    def __new_house(self, city: str, street: str, house_number: str, user_id: int) -> int:
        new_house = self.model(
            city=city,
            street=street,
            house_number=house_number,
            user_id=user_id
        )
        new_house.create()
        return new_house.id

    def create_house(self, house_data: dict) -> dict:
        new_house_id = self.__new_house(
            city=house_data['city'],
            street=house_data['street'],
            house_number=house_data['house_number'],
            user_id=house_data['user_id']
        )
        return {'message': f'house: {new_house_id} was created'}

    #  Gets

    def get_house_public_info(self, house_id: int) -> dict:
        return self.model.find_by_id(house_id).public_info
