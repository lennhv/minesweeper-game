import uuid
import random
import json
from unittest import mock
from requests.auth import HTTPBasicAuth
# from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


# Create your tests here.
from games.minesweeper_board import Minesweeper
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


class MinesweeeperCreateApiTest(APITestCase):
    """ create game test """

    def get_game_kwargs(self):
        return {
            'rows': random.randint(9, 50),
            'columns': random.randint(9, 50),
            'mines': random.randint(9, 26),
        }

    def setUp(self):
        username = 'testcreate'
        password = 'test1234*'
        user = User.objects.create_user('testcreate', password=password)
        self.client.login(username=username, password=password)

    def test_create_games(self):
        """ create game
        """
        request = self.get_game_kwargs()
        response = self.client.post(
            reverse('games:api-minesweeper'), request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["rows"], request["rows"])
        self.assertEqual(response.data["columns"], request["columns"])
        self.assertEqual(response.data["mines"], request["mines"])

    def tearDown(self):
        self.client.logout()


class MinesweeeperListRetreiveApiTest(APITestCase):
    """ List and retreive games """

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
        """ list all games
        """
        response = self.client.get(reverse('games:api-minesweeper'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.games))

    def test_get_game_detail(self):
        """ get especific game
        """
        game = self.games[random.randint(0, len(self.games)-1)]
        url = reverse('games:api-minesweeper-detail', args=(game.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["board"], json.loads(game.board))

    def tearDown(self):
        self.client.logout()


class MinesweeeperUpdateGameTest(APITestCase):
    """ update game """

    def setup_board(self, board):
        _board = []
        for row in board:
            cols = []
            for c in row:
                cols.append(Minesweeper.convert_to_cell(c))
            _board.append(cols)
        _game = MinesweeperGame.objects.create_game(**{
            'user': self.user,
            'rows': 9,
            'columns': 9,
            'mines': 4,
        })
        _game.board = json.dumps(_board)
        _game.save()
        return _game

    def setUp(self):
        username = 'testupdate'
        password = 'test1234*'
        self.user = User.objects.create_user('testupdate', password=password)
        self.client.login(username=username, password=password)

    def test_open_one_square(self):
        """ open one square
        """
        mines = ((1, 1), (2, 2), (2, 3), (5, 5))
        # board
        _b = [[1, 1, 1, 0, 0, 0, 0, 0, 0],
              [1, "M", 2, 1, 0, 0, 0, 0, 0],
              [1, 3, "M", 2, 0, 0, 0, 0, 0],
              [0, 2, "M", 2, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 1, "M", 1, 0, 0],
              [0, 0, 0, 0, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]
              ]

        _game = self.setup_board(_b)
        # _board = []
        # for row in _b:
        #     cols = []
        #     for c in row:
        #         cols.append(Minesweeper.convert_to_cell(c))
        #     _board.append(cols)
        # _game = MinesweeperGame.objects.create_game(**{
        #     'user': self.user,
        #     'rows': 9,
        #     'columns': 9,
        #     'mines': 4,
        # })
        # _game.board = json.dumps(_board)
        # _game.save()
        opens = [[4, 4]]
        url = reverse('games:api-minesweeper-detail', args=(_game.id,))
        request = {
            "opens": opens
        }
        response = self.client.put(url, request, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,)
        _picked = Minesweeper.property_to_numbers(
            response.data["board"][4][4])
        self.assertEqual(_picked[1], 1)

    def test_open_many_squares(self):
        """ open many squares, continue game
        """
        mines = ((1, 1), (2, 2), (2, 3), (5, 5))
        # board
        _b = [[1, 1, 1, 0, 0, 0, 0, 0, 0],
              [1, "M", 2, 1, 0, 0, 0, 0, 0],
              [1, 3, "M", 2, 0, 0, 0, 0, 0],
              [0, 2, "M", 2, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 1, "M", 1, 0, 0],
              [0, 0, 0, 0, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]
              ]
        _game = self.setup_board(_b)
        opens = [[3, 5], [0, 5], [1, 5], [2, 5],
                 [0, 6], [1, 6], [2, 6], [3, 6]]
        url = reverse('games:api-minesweeper-detail', args=(_game.id,))
        request = {
            "opens": opens
        }
        response = self.client.put(url, request, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        _open = Minesweeper.property_to_numbers(
            response.data["board"][5][3])
        self.assertEqual(_open[1], 1)
        _open = Minesweeper.property_to_numbers(
            response.data["board"][6][1])
        self.assertEqual(_open[1], 1)
        _open = Minesweeper.property_to_numbers(
            response.data["board"][5][2])
        self.assertEqual(_open[1], 1)

    def test_open_mine_square(self):
        """ open mine, the game is finished
        """
        mines = ((1, 1), (2, 2), (2, 3), (5, 5))
        # board
        _b = [[1, 1, 1, 0, 0, 0, 0, 0, 0],
              [1, "M", 2, 1, 0, 0, 0, 0, 0],
              [1, 3, "M", 2, 0, 0, 0, 0, 0],
              [0, 2, "M", 2, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 1, "M", 1, 0, 0],
              [0, 0, 0, 0, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]
              ]
        _game = self.setup_board(_b)
        opens = [[5, 5]]
        url = reverse('games:api-minesweeper-detail', args=(_game.id,))
        request = {
            "opens": opens
        }
        response = self.client.put(url, request, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        _open = Minesweeper.property_to_numbers(
            response.data["board"][5][5])
        self.assertEqual(_open[1], 1)
        game = MinesweeperGame.objects.get(pk=_game.id)
        self.assertEqual(game.status, game.FINISHED)
        self.assertEqual(game.result, game.LOST)

    def test_win_game(self):
        """ Open square and win game
        """
        mines = ((1, 1), (2, 2), (2, 3), (5, 5))
        to_open = [6, 3]
        # board
        _b = [[1, 1, 1, 0, 0, 0, 0, 0, 0],
              [1, "M", 2, 1, 0, 0, 0, 0, 0],
              [1, 3, "M", 2, 0, 0, 0, 0, 0],
              [0, 2, "M", 2, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 1, "M", 1, 0, 0],
              [0, 0, 0, 0, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]
              ]
        _game = self.setup_board(_b)
        _open = []
        for i, b in enumerate(_b):
            row = []
            for j, cell in enumerate(b):
                _cell = Minesweeper.convert_to_cell(cell)
                if cell != 'M':
                    _cell = Minesweeper.property_to_numbers(_cell)
                    if [j, i] != to_open:
                        _cell[1] = 1
                    _cell = Minesweeper.numbers_to_property(_cell)
                row.append(_cell)
            _open.append(row)
        _game.board = json.dumps(_open)
        _game.save()
        # Minesweeper.display_board(_open)
        opens = [to_open]
        url = reverse('games:api-minesweeper-detail', args=(_game.id,))
        request = {
            "opens": opens
        }
        response = self.client.put(url, request, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Minesweeper.display_board(response.data["board"])
        _open = Minesweeper.property_to_numbers(
            response.data["board"][3][6])
        self.assertEqual(_open[1], 1)
        game = MinesweeperGame.objects.get(pk=_game.id)
        self.assertEqual(game.status, game.FINISHED)
        self.assertEqual(game.result, game.WIN)

    def tearDown(self):
        self.client.logout()


class MinesweeeperFlagGameTest(APITestCase):
    """ update game """

    def setup_board(self, board):
        _board = []
        for row in board:
            cols = []
            for c in row:
                cols.append(Minesweeper.convert_to_cell(c))
            _board.append(cols)
        _game = MinesweeperGame.objects.create_game(**{
            'user': self.user,
            'rows': 9,
            'columns': 9,
            'mines': 4,
        })
        _game.board = json.dumps(_board)
        _game.save()
        return _game

    def setUp(self):
        username = 'testupdate'
        password = 'test1234*'
        self.user = User.objects.create_user('testupdate', password=password)
        self.client.login(username=username, password=password)

    def test_flag_square(self):
        """ flag mine square
        """
        mines = ((1, 1), (2, 2), (2, 3), (5, 5))
        # board
        _b = [[1, 1, 1, 0, 0, 0, 0, 0, 0],
              [1, "M", 2, 1, 0, 0, 0, 0, 0],
              [1, 3, "M", 2, 0, 0, 0, 0, 0],
              [0, 2, "M", 2, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 1, "M", 1, 0, 0],
              [0, 0, 0, 0, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]
              ]
        _game = self.setup_board(_b)
        square = [6, 2]
        url = reverse('games:api-minesweeper-flag', args=(_game.id,))
        request = {
            "square": square
        }
        response = self.client.put(url, request, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        _flagged = Minesweeper.property_to_numbers(
            response.data["board"][2][6])
        self.assertEqual(_flagged[0], 1)

    def test_flag_mine_square(self):
        """ flag mine square
        """
        mines = ((1, 1), (2, 2), (2, 3), (5, 5))
        # board
        _b = [[1, 1, 1, 0, 0, 0, 0, 0, 0],
              [1, "M", 2, 1, 0, 0, 0, 0, 0],
              [1, 3, "M", 2, 0, 0, 0, 0, 0],
              [0, 2, "M", 2, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 1, "M", 1, 0, 0],
              [0, 0, 0, 0, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]
              ]
        _game = self.setup_board(_b)
        square = [5, 5]
        url = reverse('games:api-minesweeper-flag', args=(_game.id,))
        request = {
            "square": square
        }
        response = self.client.put(url, request, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        _flagged = Minesweeper.property_to_numbers(
            response.data["board"][5][5])
        self.assertEqual(_flagged[0], 1)
        game = MinesweeperGame.objects.get(pk=_game.id)
        self.assertEqual(game.status, game.STARTED)
        self.assertEqual(game.result, None)

    def tearDown(self):
        self.client.logout()
