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

        if request.path == '/login' or request.path == '/create_user' :
            return None
        else :
            try :
                token = request.headers['token']
                decoded_jwt = jwt.decode(token, "5b9799a5860f950804d839736c300d99", algorithms=["HS256"])

                print("--------------------------------------")
                print("Successfully validated token")
                print("--------------------------------------")
                
                return None
            except :
                response_data['code']    = '401'
                response_data['message'] = 'Token is expired, Please relogin to get new token'
                response_data['date']    = str(date.today()) + " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)
                    
                print("--------------------------------------")
                print("Token is expired, Please relogin to get new token")
                print("--------------------------------------")

                return JsonResponse(response_data, status=status.HTTP_401_UNAUTHORIZED, safe=False)
                
    def process_response(self, request, response):
        # This method is called after the view
        # You can modify the response here
       
        return response