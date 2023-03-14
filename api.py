import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru'

    def get_api_key(self, email:str, password:str):
        """Метод позволяет получить ключ API, который можно использовать для других методов API """

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'/api/key', headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def get_list_of_pets(self, auth_key, filter):
        """Метод позволяет получить список всех питомцев"""
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url+'/api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def add_information_new_pet(self, auth_key, name, animal_type, age, pet_photo):
        """Метод позволяет добавить информацию о новом питомце"""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url+'/api/pets', data=data, headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def delete_pet_from_database(self, auth_key, pet_id):
        """Метод позволяет удалить питомца из базы"""
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(f'{self.base_url}/api/pets/{pet_id}', headers=headers)
        status = res.status_code

        return status


    def update_information_pet(self, auth_key, pet_id, name, animal_type, age):
        """Метод позволяет обновить информацию о питомце"""
        headers = {'auth_key': auth_key['key']}
        formData = {'name': name, 'animal_type': animal_type, 'age': age}
        res = requests.put(f'{self.base_url}/api/pets/{pet_id}', headers=headers, data=formData)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result



    def add_new_pet_without_photo(self, auth_key, name, animal_type, age):
        """Метод позволяет добавить питомца без фото"""
        headers = {'auth_key': auth_key['key']}
        formData = {'name': name, 'animal_type': animal_type, 'age': age}
        res = requests.post(f'{self.base_url}/api/create_pet_simple', headers=headers, data=formData)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_photo_of_pet(self, auth_key, pet_id, pet_photo):
        """Метод позволяет добавить фотографию питомца"""
        formData = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            }
        )
        headers = {'auth_key': auth_key['key'], 'Content-Type': formData.content_type}
        res = requests.post(f'{self.base_url}/api/pets/set_photo/{pet_id}', headers=headers, data=formData)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


