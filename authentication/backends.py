# authentication > backends.py

import jwt

from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User

class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        """
            'authenticate' method는 endpoint에 인증이 필요한지 여부와 상관없이 
            모든 요청(request)에서 호출됩니다.
            
            'authenticate'는 두 종류의 value값을 반환합니다.
            
            1) 'None' - 어떤 요청의 header에 'token'을 포함하지 않는 경우 'None'값을
                        반환합니다. 보통 우리는 이런 경우를 인증에 실패한 경우라고 생각하면 됩니다. 
            2) '(user, token)' - 인증이 성공적으로 이루어졌을 때는 user/token 조합을 반환합니다.
            
            만약 두 경우 외에 다른 경우가 생긴다면 그것은 어떤 error가 발생했음을 의미합니다.
            error가 발생한 경우 어떤 것도 반환하지 않습니다. 단지 'AuthenticationFailed' 
            error를 보내고, 나머지는 DRF가 처리하도록 합니다.
        """

        # 'auth_header'는 두 가지 요소(element)를 배열로 갖고 있어야 합니다.
        # 1) authentication header의 이름(여기에서는 'Token')
        # 2) 인증해야 하는 JWT
        # 여기서 우리가 POSTMAN에서 토큰값 앞에 'token'을 붙인 이유가 나옵니다.
        # 'token'이 없는 경우에는 제대로 동작하지 않습니다.
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        # 위에서 언급한 바와 같이 auth_header는 두가지 값을 배열로 갖고 있어야 합니다.
        # 한 개의 값만 받아왔을 경우 None값을 반환합니다.
        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None

        elif len(auth_header) > 2:
            return None

        # prefix.lower()는 우리가 바깥에서 받아온 'token' 값 입니다. postman에서 토큰값
        # 앞에 붙이 그 'token'입니다. 만약 받아온 'token'값이 저희가 앞서 설정한
        # auth_header_prefix의 값과 다르면 None을 반환합니다.
        
        # 여기서 auth_header_prefix는 class가 시작되는 초기에 설정한 authentication_header_prefix를
        # 소문자로 바꾼 값입니다.
        
        # 한편 앞서 lower() 메소드를 이용해 전부 소문자로 바꾸었기 때문에 'Token'값이
        # 'token'값이 돼서 오류없이 통과합니다.
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """
            위의 과정을 통과한 user에게 접근을 허용하도록 합니다. 만약 인증이 성공적이라면
            user와 token을 반환해주고, 그렇지 않은 경우에는 error를 반환합니다.
            
            아래 과정은 추가적인 인증 과정입니다.
            그대로 사용해도 되고 이 부분에서 custom해서 사용해도 됩니다. 아래 return 값으로
            user와 token 값만 제대로 반환하면 됩니다.
        """
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)