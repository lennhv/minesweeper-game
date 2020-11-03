import uuid
import random
from unittest import mock
from requests.auth import HTTPBasicAuth
# from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


# Create your tests here.
from games.models import MinesweeperGame
from users.models import User


class MinesweeeperApiForbidenTest(APITestCase):
    """ Test API for no user provided """

    def test_list_games(self):
        response = self.client.get(reverse('games:api-minesweeper'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_games(self):
        response = self.client.post(reverse(
            'games:api-minesweeper'), {'rows': 10, 'columns': 10, 'mines': 5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_game_detail(self):
        url = reverse('games:api-minesweeper-detail', args=(uuid.uuid4(),))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_game(self):
        url = reverse('games:api-minesweeper-detail', args=(uuid.uuid4(),))
        response = self.client.post(
            url, {'rows': 10, 'columns': 10, 'mines': 5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_flag_game(self):
        url = reverse('games:api-minesweeper-flag', args=(uuid.uuid4(),))
        response = self.client.post(
            url, {'square': [0, 0]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MinesweeeperApiInvalidUserTest(APITestCase):

    def setup(self):
        self.client.auth = HTTPBasicAuth('user', 'pass')

    def test_list_games(self):
        response = self.client.get(reverse('games:api-minesweeper'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_games(self):
        response = self.client.post(reverse(
            'games:api-minesweeper'), {'rows': 10, 'columns': 10, 'mines': 5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_game_detail(self):
        url = reverse('games:api-minesweeper-detail', args=(uuid.uuid4(),))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_game(self):
        url = reverse('games:api-minesweeper-detail', args=(uuid.uuid4(),))
        response = self.client.post(
            url, {'rows': 10, 'columns': 10, 'mines': 5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_flag_game(self):
        url = reverse('games:api-minesweeper-flag', args=(uuid.uuid4(),))
        response = self.client.post(
            url, {'square': [0, 0]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MinesweeeperListRetreiveApiInvalidUserTest(APITestCase):

    def get_game_kwargs(self, user):
        return {
            'user': user,
            'rows': random.randint(9, 50),
            'columns': random.randint(9, 50),
            'mines': random.randint(9, 26),
        }

    def setUp(self):
        username = 'testlist'
        password = 'test1234*'
        user = User.objects.create_user('testlist', password=password)
        self.client.login(username=username, password=password)
        self.games = [MinesweeperGame.objects.create_game(
            **self.get_game_kwargs(user)) for i in range(5)]

    def test_list_games(self):
        response = self.client.get(reverse('games:api-minesweeper'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_game_detail(self):
        game = self.games[2]
        url = reverse('games:api-minesweeper-detail', args=(game.id,))
        response = self.client.get(url)
        print(response)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        self.client.logout()
