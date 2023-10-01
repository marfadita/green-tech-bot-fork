from pymongo import MongoClient

from bson.objectid import ObjectId

import functools
print = functools.partial(print, flush=True)

import datetime

client = MongoClient('mongodb', 27017)
db = client['ecobot']

users = db['users']
subscriptions = db['subscriptions']
locations = db['locations']
fractions = db['fractions']
stations = db['stations']
map_locations = db['map_locations']
map_fractions = db['map_fractions']
map_stations = db['map_stations']

traffic = db['traffic']
journal = db['journal']

print("Connected to DB")


def new_usage(id):
    # TODO can you use datetime.date in mongo?
    today = datetime.datetime.utcnow().date()
    today_datetime = datetime.datetime(today.year, today.month, today.day)

    # actions_count
    if not traffic.find_one({'date': today_datetime}):
        traffic.insert_one({'date': today_datetime, 'actions_count': 0, 'users_count': 0})
    traffic.update_one({'date': today_datetime}, {'$inc': {'actions_count': 1}})  # TODO check thread-safety

    # users_count
    user = users.find_one({'id': id})
    if not user:
        return  # TODO
    if 'last_usage' not in user or user['last_usage'] < today_datetime:
        traffic.update_one({'date': today_datetime}, {'$inc': {'users_count': 1}})

    # user's last_usage
    users.update_one({'id': id}, {'$set': {'last_usage': today_datetime}})


def get_user_by_id(id):
    res = users.find_one({
        'id': id
    })
    if res:
        return {
            'success': True,
            'data': res
        }
    else:
        return {
            'success': False,
            'err': 'no user found'
        }


def user_state(id):
    res = users.find_one({
        'id': id
    })
    if res:
        return {
            'success': True,
            'data': res['state']
        }
    else:
        return {
            'success': False,
            'err': 'no user found'
        }


def change_user_state(id, _state):
    users.find_one_and_update({'id': id}, {'$set': {'state': _state}})


def save_data(id, data_name, data):
    users.find_one_and_update({'id': id}, {'$set': {data_name: data}})


def get_users_subscriptions(id):
    res = subscriptions.find({
        'id': id
    })
    return res


def send_announce(id):
    user_list = users.find({'subscription': True})
    users.update_many({'subscription': True}, {'$inc': {'cnt': 1}})
    data = get_user_by_id(id)
    return {
        'users': [[i['id'], i['cnt']] for i in user_list],
        'msg': data['data']['msg']
    }


def add_subscription(id):
    data = get_user_by_id(id)
    if data['success']:
        data = data['data']
        subscriptions.insert_one({'id': id,
                                  'where': data['where-subscription'],
                                  'what': data['what-subscription']})
    else:
        print("FAIL")


def delete_subscription(id):
    subscriptions.delete_one({'_id': ObjectId(id)})


def get_all_visible_locations():
    locations_list = locations.find({'visible': True})
    return locations_list


def get_stations_by_location_id(id):
    stations_list = stations.find({'location_id': ObjectId(id)})
    return stations_list


def get_fraction_by_station_id(id):
    k = fractions.find_one({'_id': ObjectId(id)})
    return k


def get_station_by_id(id):
    k = map_stations.find_one({'_id': ObjectId(id)})
    return k


def get_map_fractions(core=True):
    fractions_list = map_fractions.find({'core': core})
    return fractions_list


def get_map_stations_for_fration(fraction_name):
    fraction = map_fractions.find_one({'name': fraction_name})
    if '_id' in fraction:
        fractions_list = map_stations.find({'fraction_id': fraction['_id']})
        return fractions_list
    return []


def get_single_stations_for_fration(fraction_name):
    fraction = map_fractions.find_one({'name': fraction_name})
    if '_id' in fraction:
        station = map_stations.find_one({'fraction_id': fraction['_id']})
        return station['_id']
    return []


def get_map_location_name(id):
    k = map_locations.find_one({'_id': ObjectId(id)})
    return k['name']


def get_coords_by_station_id(id):
    station = map_stations.find_one({'_id': ObjectId(id)})
    location = map_locations.find_one(
        {'_id': ObjectId(station['location_id'])})
    return (location['latitude'], location['longitude'])


def insert_new_user(update):
    if not update.message.chat.first_name:
        update.message.chat.first_name = ""
    if not update.message.chat.last_name:
        update.message.chat.last_name = ""
    if not update.message.chat.username:
        update.message.chat.username = ""
    users.insert_one({
        'id': update.message.chat.id,
        'first_name': update.message.chat.first_name,
        'last_name': update.message.chat.last_name,
        'username': update.message.chat.username,
        'state': 'main',
        'subscription': True,
        'cnt': 0,
        'authorized': False
    })
