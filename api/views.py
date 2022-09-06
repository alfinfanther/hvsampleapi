from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from api.serializers import LoginSerializer

# Create your views here.

class LoginView(APIView):
    def post(self, *args, **kwargs):
        try:
            data = JSONParser().parse(self.request)
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                email = 'admin@example.com'
                password = 'paAsswd045'
                if data['email'] == email and data['password'] == password and self.request.headers.get('CLIENT-ID') == 'TEST-USER':
                    
                    return JsonResponse(data = {
                        "message": "Login sucess",
                        "email": data['email']
                    }, status=200)
                
                else:
                    return JsonResponse(data = {
                                "message": "User/Password salah"
                            }, status=400)
            else:
                return JsonResponse(serializer.errors, status=400)
        except Exception as e:
            return JsonResponse(data = {
                            "message": str(e)
                        }, status=400)