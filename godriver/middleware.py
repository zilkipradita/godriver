from django.utils.deprecation import MiddlewareMixin
from datetime import date
from datetime import time
from datetime import datetime
from django.http.response import JsonResponse
from rest_framework import status
import jwt

class CustomMiddleware(MiddlewareMixin):
            
    def process_request(self, request):
        dt = datetime.now() 
        response_data = {}

        if request.path == '/login' or request.path == '/create_user' or request.path == '/doc/' :
            return None
        else :
            try :
                token = request.headers['token']
                decoded_jwt = jwt.decode(token, "5b9799a5860f950804d839736c300d99", algorithms=["HS256"])

                if request.headers['username'] == decoded_jwt['username'] :
                    print("--------------------------------------")
                    print("Successfully validated token")
                    print("username :" + decoded_jwt['username'])
                    print("--------------------------------------")
                    
                    return None    
                else :
                    print("--------------------------------------")
                    print("Failed to validate token")
                    print("This token is not belonged to this user (" + request.headers['username'] + ")")
                    print("Please login using username (" + request.headers['username'] + ") to get the token")
                    print("--------------------------------------")
            
                    response_data['code']    = '412'
                    response_data['message'] = "This token is not belonged to this user (" + request.headers['username'] + "), Please login using username (" + request.headers['username'] + ") to get the token"
                    response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

                    return JsonResponse(response_data, status=status.HTTP_412_PRECONDITION_FAILED, safe=False)
                                    
            except :
                response_data['code']    = '401'
                response_data['message'] = 'Token is expired, Please relogin to get new token'
                response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)
                    
                print("--------------------------------------")
                print("Token is expired, Please relogin to get new token")
                print("--------------------------------------")

                return JsonResponse(response_data, status=status.HTTP_401_UNAUTHORIZED, safe=False)
                
    def process_response(self, request, response):
        
        return response