
import pytest
import lib
import socket


# def salary(param1, param2):
# 
#     answer = param1 * param2
#     return answer
# 
# 
# def test_salary():
#     
#     assert salary(2,2) == 5
    

# def test_answer_to_client():
#     assert lib.Server.answer_to_client(1) == '200 - OK'

class TestServer:

    def setup(self):
        pass

    def test_answer_to_client(self):
        
        s = lib.Server
        assert s.answer_to_client(self, 1) == '200 - OK'