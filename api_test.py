import requests
import pytest


BASE_URL =  'https://pokeapi.co/api/v2/'

# This function request a respone and returns it if the request has succeded.
def get_response(url_ending):
    response = requests.get(BASE_URL + url_ending)
    assert response.status_code == 200, "Request has failed!"
    return response

# This function checks if the response type is JSON and if so, returns the response's data. 
def get_data(response):
    response_content_type = response.headers.get('content-type').lower()
    assert 'application/json' in response_content_type, "Response type is not JSON!"
    data = response.json()
    assert isinstance(data, dict), "Response type is not JSON!"
    return data

# This function checks that there are exactly 20 different pokemon types. 
def verify_20_types(array):
    assert ['name' in item for item in array], "There is no key 'name' array['result']!"
    assert ['url' in item for item in array], "There is no key 'url' array['result']!"
    unique_names = set(item['name'] for item in array)
    unique_urls = set(item['url'] for item in array)
    if len(unique_names) != 20 or len(unique_urls) != 20:
        return 0
    return 1

# This function return the ID of the Fire type. 
def find_id_fire_type():
    response = get_response('type')
    data = get_data(response)
    assert data.get('results') and ['url' in item for item in data['results']], "There is no key 'url' array['result']!"
    fire_url = [item['url'] for item in data['results'] if item['name'] == 'fire'][0]
    assert '/' in fire_url, "Wrong URL for finding the Fire ID!"
    fire_id = fire_url.rstrip('/').rsplit('/')[-1]
    assert fire_id.isnumeric(), "Wrong URL for finding the Fire ID!"
    return fire_id

# This function return the expected five heaviest pokemons and their weight. 
def get_expected_weights():
    return {
        'charizard-gmax': 10000,
        'cinderace-gmax': 10000,
        'coalossal-gmax': 10000,
        'centiskorch-gmax': 10000,
        'groudon-primal': 9997
    }



def test_section_1():
    response = get_response('type')
    data = get_data(response)
    assert data.get('count') and data['count'] >= 20, "The count of pokemon types is smaller than 20!"
    assert data.get('results') and len(data['results']) >= 20, "The len of pokemon types array is smaller than 20!"
    assert verify_20_types(data['results']), "The number of different pokemon types is not 20!"

def test_section_2():
    fire_id = find_id_fire_type()
    response = get_response('type/' + fire_id)
    data = get_data(response)
    assert data.get('name') and data['name'].lower() == 'fire', "There is no Fire type!"
    fire_pokemons_list = [item['pokemon'].get('name') for item in data['pokemon']]
    assert 'charmander' in fire_pokemons_list, "charmander not found in Fire Pokemon list"
    assert 'bulbasaur' not in fire_pokemons_list, "bulbasaur found in Fire Pokemon list"

def test_section_3():
    expected_weights = get_expected_weights()
    fire_id = find_id_fire_type()
    response = get_response('type/' + fire_id)
    data = get_data(response)
    assert data.get('name') and data['name'].lower() == 'fire', "There is no Fire type!"
    fire_pokemons_list = [item['pokemon'].get('name') for item in data['pokemon']]
    weight_list = []
    for pokemon in fire_pokemons_list:
        response = get_response('pokemon/' + pokemon)
        data = get_data(response)
        assert data.get('weight'), "There is no key 'weight' for {} pokemon!".format(pokemon)
        weight_list.append({ 'weight' : data['weight'], 'name' : pokemon })
    weight_list.sort(key=lambda x: x['weight'], reverse=True)  # sort the weight_list by the object's 'weight' key and reverse the list
    top_5_heaviest_list = weight_list[:5]  # the top 5 heaviest pokemons 
    for pokemon in top_5_heaviest_list:
        assert pokemon['name'] in expected_weights, "{} pokemon is not in the expected weight list".format(pokemon['name'])
        assert expected_weights[pokemon['name']] == pokemon['weight'], "{} pokemon is weights {} and not as expected".format(pokemon['name'], pokemon['weight'])
