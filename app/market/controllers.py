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

    def __change_house_fields(self, house_id: int, city: str, street: str,
                              house_number: str, summary: str, cost: float) -> list:
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
