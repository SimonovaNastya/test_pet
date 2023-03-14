from api import PetFriends
from settings import valid_email, valid_password


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_peth_with_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_information_new_pet(auth_key, 'Георгий', 'Попугай', '10', 'images/popugay.jpg')
    assert status == 200
    assert result['name'] == 'Георгий'
    assert result['id'] != ''


def test_delete_pet_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    if len(result['pets']) > 0:
        status = pf.delete_pet_from_database(auth_key, result['pets'][0]['id'])
    else:
        _, result = pf.add_information_new_pet(auth_key, 'Георгий', 'Попугай', '10', 'images/popugay.jpg')
        status = pf.delete_pet_from_database(auth_key, result['id'])
    assert status == 200


def test_test_update_info_about_pet_valid():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.add_information_new_pet(auth_key, 'Георгий', 'Попугай', '10', 'images/popugay.jpg')
    status, result = pf.update_information_pet(auth_key, result['id'], 'Кеша', 'Птица', 1)
    assert status == 200


def test_add_new_pet_without_photo_valid():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, 'Пушистик', 'Хомяк', 3)
    assert status == 200
    assert result['name'] == 'Пушистик'


def test_set_pet_photo_valid():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter='my_pets')

    if len(result['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, result['pets'][0]['id'], 'images/krokodil.jpg')
    else:
        _, result = pf.add_information_new_pet(auth_key, 'Гена', 'Крокодил', 7, 'images/popygay.jpg')
        status, result = pf.add_photo_of_pet(auth_key, result['pets'][0]['id'], 'images/krokodil.jpg')
    assert status == 200
    assert result['id']


def test_set_other_pet_photo_invalid():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter='')

    if len(result['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, result['pets'][0]['id'], 'images/krokodil.jpg')
    else:
        _, result = pf.add_information_new_pet(auth_key, 'Гена', 'Крокодил', 7, 'images/popygay.jpg')
        status, result = pf.add_photo_of_pet(auth_key, result['pets'][0]['id'], 'images/krokodil.jpg')
    assert status == 400 or status == 500


def test_set_other_pet_photo_invalid_auth_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter='')
    auth_key['key'] += 'xx'

    if len(result['pets']) > 0:
         status, result = pf.add_photo_of_pet(auth_key, result['pets'][0]['id'], 'images/krokodil.jpg')
    else:
        _, result = pf.add_information_new_pet(auth_key, 'Гена', 'Крокодил', 7, 'images/popygay.jpg')
        status, result = pf.add_photo_of_pet(auth_key, result['pets'][0]['id'], 'images/krokodil.jpg')
    assert status == 403



def test_get_api_key_for_invalid_user():
    status, result = pf.get_api_key('kurs@gmail.com', '1234')
    assert status == 403