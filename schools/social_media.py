import requests
import json
from random import randint
#instagram api credentials
toserver2 = True
if toserver2:
    myserver = 'https://www.bilimtap.kz/'
else:
    myserver = 'http://127.0.0.1:8000/'
social_networks_settings_url = myserver + 'schools/social_networks_settings/'
insta_server = myserver + 'schools/instagram_connecting/'
instagram_id = '1402067986632477'
secret_instagram = '5adaeda9020c02ecf00e6114bf2155c3'
#vk.com api credentials
vk_server = myserver + 'schools/vk_connecting/'
vk_id = '7346891'
secret_vk = '6qsFJ2c3GMafUHrf3CK5'

def vk_get_user_access(code, vk):
    url = 'https://oauth.vk.com/access_token'
    data = {
        'client_id':vk_id, 
        'client_secret':secret_vk, 
        'redirect_uri':vk_server, 
        'code':code,
    }
    r = requests.post(url,data=data,allow_redirects=True)
    a = json.loads(r.content)
    user_id = str(a['user_id'])
    access_token = str(a['access_token'])
    vk.user_id = user_id
    vk.access_token = access_token
    vk.save()
    get_groups_url = 'https://api.vk.com/method/groups.get'
    data = {
        'user_id':user_id,
        'extended':1,
        'filter':'admin',
        'access_token':access_token,
        'v':'5.103', 
    }
    r = requests.post(get_groups_url,data=data,allow_redirects=True)
    a = json.loads(r.content)
    group_list = a['response']['items']
    return group_list

def vk_get_group_access(code, vk):
    url = 'https://oauth.vk.com/access_token'
    data = {
        'client_id':vk_id, 
        'client_secret':secret_vk, 
        'redirect_uri':vk_server, 
        'code':code,
    }
    r = requests.post(url,data=data,allow_redirects=True)
    print('vk_get_group_access ffffffffffffff')
    print(r.content)
    print('fffffffffffffff')
    a = json.loads(r.content)
    print(a)
    group_access_token = str(a['access_token_'+vk.groupid])
    return group_access_token

def vk_get_confirmation_code(groupid,group_access_token):
    confirmcode_url = 'https://api.vk.com/method/groups.getCallbackConfirmationCode'
    data = {
        'group_id':groupid,
        'access_token':group_access_token,
        'v':'5.103', 
    }
    r = requests.post(confirmcode_url,data=data,allow_redirects=True)
    a = json.loads(r.content)
    print('confirmation_code00', a)
    confirmation_code = a['response']['code']
    return confirmation_code

def vk_edit_server(groupid, server_id, secretkey, group_access_token):
    edit_url = 'https://api.vk.com/method/groups.editCallbackServer'
    data = {
        'group_id':groupid,
        'server_id':server_id,
        'url':'https://www.bilimtap.kz/schools/api/vk_get_callback/',
        'title':'Bilimtap',
        'secret_key':secretkey,
        'access_token':group_access_token,
        'v':'5.103', 
    }
    r = requests.post(edit_url,data=data,allow_redirects=True)

def vk_add_server(groupid, secretkey, group_access_token):
    url = 'https://api.vk.com/method/groups.addCallbackServer'
    data = {
        'group_id':groupid,
        'url':'https://www.bilimtap.kz/schools/api/vk_get_callback/',
        'title':'Bilimtap',
        'secret_key':secretkey,
        'access_token':group_access_token,
        'v':'5.103', 
    }
    r = requests.post(url,data=data,allow_redirects=True)
    a = json.loads(r.content)
    server_id = a['response']['server_id']
    return server_id

def vk_delete_server(groupid,server, group_access_token):
    delete_url = 'https://api.vk.com/method/groups.deleteCallbackServer'
    data = {
        'group_id':groupid,
        'server_id':server['id'],
        'access_token':group_access_token,
        'v':'5.103', 
    }
    r = requests.post(delete_url,data=data,allow_redirects=True)

def vk_get_servers(groupid, group_access_token):
    check_url = 'https://api.vk.com/method/groups.getCallbackServers'
    data = {
        'group_id':groupid,
        'access_token':group_access_token,
        'v':'5.103', 
    }
    r = requests.post(check_url,data=data,allow_redirects=True)
    a = json.loads(r.content)
    allservers = a['response']['items']
    return allservers

def vk_get_callback_api_version(groupid,server_id,group_access_token):
    url = 'https://api.vk.com/method/groups.getCallbackSettings'
    data = {
        'group_id':groupid,
        'server_id':server_id,
        'access_token':group_access_token,
        'v':'5.103', 
    }
    r = requests.post(url,data=data,allow_redirects=True)
    a = json.loads(r.content)
    print('vk_get_callback_api_version', a)
    api_version = a['response']['api_version']
    return api_version

def vk_set_callback_settings(groupid, server_id, api_version,group_access_token):
    set_callback_url = 'https://api.vk.com/method/groups.setCallbackSettings'
    data = {
        'group_id':groupid,
        'server_id':server_id,
        'api_version':api_version,
        'message_new':1,
        'message_edit':1,
        'wall_reply_new':1,
        'wall_reply_edit':1,
        'wall_reply_delete':1,
        'wall_reply_restore':1,
        'wall_reply_restore':1,
        'board_post_new':1,
        'board_post_edit':1,
        'board_post_restore':1,
        'board_post_delete':1,
        'market_comment_new':1,
        'market_comment_edit':1,
        'market_comment_delete':1,
        'market_comment_restore':1,
        'group_join':1,
        'access_token':group_access_token,
        'v':'5.103', 
    }
    r = requests.post(set_callback_url,data=data,allow_redirects=True)

def vk_get_user(user_id,group_access_token):
    url = 'https://api.vk.com/method/users.get'
    data = {
        'user_ids':user_id,
        'access_token':group_access_token,
        'fields':'photo_50',
        'v':'5.103',
    }
    r = requests.post(url,data=data,allow_redirects=True)
    a = json.loads(r.content)
    print('vk_get_user', a)
    user = a['response'][0]
    name = user['first_name'] + user['last_name']
    photo_link = user['photo_50']
    return name

def vk_send_message(vk, text, user_id):
    url = 'https://api.vk.com/method/messages.send'
    random = randint(100,999)
    data = {
        'message':text,
        'user_id':user_id,
        'random_id':random,
        'access_token':vk.group_access_token,
        'v':'5.103',
    }
    r = requests.post(url,data=data,allow_redirects=True)
    a = json.loads(r.content)
    print(a)