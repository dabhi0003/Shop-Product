from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.conf import settings
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import GenericAPIView
import random
import string
from django.template.loader import get_template
from django.core.mail import EmailMessage


class UserView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            is_superuser = request.data.get('is_superuser', False)
            if is_superuser and not request.user.is_superuser:
                return Response({"Msg": "Only superuser can create a superuser"},)
            serializer.save(is_superuser=is_superuser)
            return Response({"Msg": "User Created", "Data": serializer.data})
        return Response(serializer.errors)
    
    def get(self,request):
        if request.user.is_superuser:
            user=User.objects.all()
            serilizer=UserSerializer(instance=user,many=True)
            return Response(serilizer.data) 
        else:
            return Response("Only Admin can show the data.")

class CategoryView(APIView):
    def post(self,request):
        if request.user.is_superuser:
            serializer=CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response("Invalid Data")
        else:
            return Response("Only super user can add the category.")
        
    def get(self,request):
        if request.user.is_superuser:
            category=Category.objects.all()
            serilizer=CategorySerializer(instance=category,many=True)
            return Response(serilizer.data) 
        else:
            return Response("Only Admin can show the data.")
        
class ProductView(APIView):
    def post(self,requset):
        if requset.user.is_superuser:
            serializer=ProductSerializer(data=requset.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response("Invalid Data")
        else:
            return Response("Only admin can add the product..")
        
    def get(self,request):
        if request.user.is_superuser:
            product=Product.objects.all()
            serilizer=UserSerializer(instance=product,many=True)
            return Response(serilizer.data) 
        else:
            return Response("Only Admin can show the data.")
        
class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        if request.user.is_superuser == False:
            serializer=UserDetailsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data)
            else:
                return Response("Invalid Data..")
        else:
            return Response("only User can add that details..Admin can't add information ")
    
    def get(self,request):
        user=request.user
        if request.user.is_superuser:
            details=UserProfile.objects.all()
            serilizer=UserDetailsSerializer(instance=details,many=True)
            return Response(serilizer.data) 
        details=UserProfile.objects.filter(user=user)
        serializer=UserDetailsSerializer(instance=details,many=True)
        return Response(serializer.data)
              
class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data
    
class UserProductView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        if request.user.is_superuser == False:
            serializer=UserProductSerializer(data=request.data)
            if serializer.is_valid():
                user_email = request.user.email
                user_product=serializer.save(user=request.user)
                product = user_product.product
                email_subject = 'Product Details'
                email_body = f"Your Product details..\nProduct Name: {product.name}\nPrice: {product.price}\nDescription: {product.discription}"
                email = EmailMessage(email_subject, email_body, from_email=settings.EMAIL_HOST_USER, to=[user_email])
                email.send()
                return Response({"success":serializer.data})
            else:
                return Response({"Erro":"Invalid Data.."})
        else:
            return Response({"Erro":"only comonuser can buy a product.."})

    def get(self,request):
        user=request.user
        if request.user.is_superuser:
            details=UserProduct.objects.all()
            serilizer=UserProductListSerializer(instance=details,many=True)
            return Response(serilizer.data) 
        details=UserProduct.objects.filter(user=user)
        serializer=UserProductListSerializer(instance=details,many=True)
        return Response(serializer.data)

class SendPasswordResetLinkView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        user = User.objects.filter(email=request.data['email'], username = request.data['username']).first()
        print('user: ', user)
        if user:
            N = 7
            tempass = str(''.join(random.choices(string.ascii_letters, k=N)))
            user.set_password(tempass)
            user.save()
            message = get_template("mail.html").render({
                
                "Temprory_password":tempass,
            })
            mail = EmailMessage(
                subject="Temprory Password Information",
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[request.data['email']],
            )
            mail.content_subtype = "html"
            mail.send(fail_silently=False)
            return Response({"Success":f"Mail sending on this mail is: {request.data['email']}"})    
        else:
            return Response({"Error":f"User Not availble"})
        
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'detail': 'Invalid old password'})
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'detail': 'Password successfully changed'})
        return Response(serializer.errors)