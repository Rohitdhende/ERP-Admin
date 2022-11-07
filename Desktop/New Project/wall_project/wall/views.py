from django.shortcuts import render

# Create your views here.
def register_render(request):
    """
    this function use to render signup html fileregister/
    """
    return render(request, 'digital_locker_signup.html')


def login_render(request, *args, **kwargs):
    """
    this function use to render singin html file
    """

    return render(request, 'digital_locker_signin.html')


def email_activation_login(request, *args, **kwargs):
    uid = kwargs.get('uidb64')
    print(uid)
    if uid:
        decoded_user_id = urlsafe_base64_decode(uid)
        print(decoded_user_id)
        user = RegisterUser.objects.get(id=decoded_user_id)
        user.active_email = True
        user.save()
        return render(request, 'digital_locker_signin.html')


class RegisterAPIView(APIView):
    model = RegisterUser
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        user_id = data.get('user_id')
        password = data.get('password')
        email = data.get('email')
        display_name = data.get('display_name')
        hash_pass = pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=32)
        qs = RegisterUser.objects.filter(Q(user_id__iexact=user_id) | Q(email__iexact=email))
        if qs.count() == 0:
            new_user = RegisterUser(user_id=user_id, password=hash_pass, email=email, display_name=display_name)
            new_user.save()
            user = User.objects.create_user(username=user_id, password=hash_pass, email=email,
                                            first_name=display_name)
            user.save()
            auth_user = User.objects.get(username=user_id)
            token=default_token_generator.make_token(auth_user)
            token_user = RegisterUser.objects.get(user_id=user_id)
            token_user.token = token
            token_user.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Thank you for Registering with us.You can sign in now'
            }
        else:
            response = {
                'status': 'error',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'this User id  or Email already taken, please choose another one'
            }

        return Response(response)


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        user_id = data.get('user_id')
        password = data.get('password')
        user = RegisterUser.objects.get(user_id=user_id)
        hash_data = user.verify_password(password)
        if hash_data == True:
            request.session['user_id'] = user.id
            token = user.token

            response = {
                'status': 'ok',
                'token': token,
                'user_id':user.user_id,
                'id':user.id,
                'email':user.email,
                'message': 'entered'
            }
        else:
            response = {
                'status': 'error',
                'message': 'please check your user id or password'
            }
        return Response(response)


class MainPageAPIView(APIView):
    permission_classes = [permissions.AllowAny]

	def __init__(self, arg):
		super(MainPage, self).__init__()
		self.arg = arg
		