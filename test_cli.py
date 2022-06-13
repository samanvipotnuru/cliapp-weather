import unittest
from unittest import mock
from myapp import cli
from getpass import getpass
import click

class TestCLIApp(unittest.TestCase):

    def setUp(self) -> None:
        cli.before()
        return super().setUp()

    def test_logIn(self):
        def inpt(s):
            return 'sams'
        def passw(s):
            return 'new'
        cli.input = inpt
        cli.getpass = passw
        user = cli.logIn()
        isinstance(user, cli.appUser)
        cli.logOut()
    
    def test_register(self):
        inputList = ['Trial','trial','y']
        passwList = ['some','some']
        def inpt(s):
            return inputList.pop(0)
        def passw(s):
            return passwList.pop(0)
        
        cli.input = inpt
        cli.getpass = passw
        cli.register()
        cli.delUser(cli.userList['trial'])
        cli.after()

    @mock.patch('myapp.cli.input',create=True)
    def test_makeAPIcall(self,mocked_input):
        inputList = ['1','london','3','4','']
        mocked_input.side_effect = ['1','london','3','4','']
        cli.makeAPIcall()
        mocked_input.side_effect = ['3']
        cli.makeAPIcall()
        mocked_input.side_effect = ['1','33.33','99.99','3','4','']
        cli.makeAPIcall()
        mocked_input.side_effect = ['some','1','london','3','4','']
        cli.makeAPIcall()
    

    @mock.patch('myapp.cli.input',create=True)
    def test_updateInfo(self,mocked_input):
        mocked_input.side_effect = ['1','sams','']
        user = cli.appUser('Sam','sams','9717eab6a57ca64171aafc6e17b03367',b'\xab\xe9\xd1\xb1\x92"K\x19R\xd7\x15\xd3;\xab\xf5\xd0')
        cli.updateInfo(user)
    
    @mock.patch('myapp.cli.input',create=True)
    def test_printAll(self,mocked_input):
        mocked_input.side_effect = ['']
        cli.printAllUsers()