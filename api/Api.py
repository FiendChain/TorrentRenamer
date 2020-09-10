import requests 
import json
from .errors import *

BASE_URL = "https://api.thetvdb.com/"

class Api:
    def __init__(self, apikey=None, userkey=None, username=None, token=None):
        self.headers = {}
        self.credentials = {
            "apikey": apikey,
            "userkey": userkey,
            "username": username,
        }
        if not token:
            self.token = self.login(apikey, userkey, username)
        else:
            self.token = self.refresh_token(token)

    @staticmethod
    def load_api(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            token = data.get('token', None)
            credentials = data.get('credentials', {})
        if not token:
            api = Api(**credentials)
        else:
            try:
                api = Api(**credentials, token=token)
            except AuthorizationError: 
                api = Api(**credentials)
        
        data['token'] = api.token
        with open(filename, 'w') as file:
            json.dump(data, file)
        
        return api
    
    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self._token = token
        self.headers.setdefault('Authorization', 'Bearer {}'.format(token))

    def login(self, apikey, userkey, username):
        response = requests.post(BASE_URL+"login", json={
            "apikey": apikey,
            "userkey": userkey,
            "username": username,
        })
        if response.status_code != 200:
            raise LoginException(apikey, userkey, username)
        return json.loads(response.text).get('token', None)

    def refresh_token(self, token=None):
        if not token:
            token = self.token
        response = requests.get(BASE_URL+"refresh_token", headers={
            'Authorization': 'Bearer {}'.format(token),
        })
        if response.status_code == 401:
            raise AuthorizationError(
                message="Invalid token: {}".format(token), 
                route=BASE_URL+"refresh_token")
        if response.status_code != 200:
            raise UnknownResponseException(response)
        return json.loads(response.text).get('token') 

    def search_series(self, name):
        response = requests.get(BASE_URL+"search/series", headers=self.headers, params={
            "name": name
        })
        if response.status_code == 401:
            raise AuthorizationError(BASE_URL+"search/series")
        if response.status_code == 404: # no match
            return None
        if response.status_code != 200:
            raise UnknownResponseException(response)
        return json.loads(response.text).get('data', [])
    
    def get_series_by_id(self, series_id):
        url = BASE_URL+"series/{}".format(series_id)
        response = requests.get(url, headers=self.headers)
        if response.status_code == 401:
            raise AuthorizationError(url)
        if response.status_code == 404:
            return None
        if response.status_code != 200:
            raise UnknownResponseException(response)
        return json.loads(response.text).get('data', None)

    def get_series_episodes(self, series_id):
        url = BASE_URL+"series/{}/episodes".format(series_id)
        def get_page(page=1):
            response = requests.get(url, headers=self.headers, params={
                'page': page,
            })
            if response.status_code == 401:
                raise AuthorizationError(url)
            if response.status_code == 404:
                return None
            if response.status_code != 200:
                raise UnknownResponseException(response)
            return json.loads(response.text)
        pages = []
        response = get_page()
        page_info = response.get('links')
        pages.extend(response.get('data'))
        # get all pages
        next_page = page_info.get('next', None)
        last_page = page_info.get('last', None)
        if not next_page or not last_page:
            return pages
        for pageNumber in range(int(next_page), int(last_page)+1):
            response = get_page(pageNumber)
            page = response.get('data', None)
            if page:
                pages.extend(page)
        return pages