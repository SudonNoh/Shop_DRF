# authentication > api > renderers.py
import json

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    
    def render(self, data, media_type=None, renderer_context=None):
        # 만약 우리가 'token'을 받게 되면 이 'token'은 byte형태 입니다.
        # Byte는 직렬화하지 못하기 때문에 rendering 전에 decode해야 합니다.
        # 따라서 data 안에 있는 token을 받고,
        token = data.get('token', None)
        
        # token이 byte형태일 경우
        if token is not None and isinstance(token, bytes):
            # 'utf-8'로 decode 해준 후 다시 data의 'token' 부분에 추가합니다.
            data['token'] = token.decode('utf-8')
        
        # 그리고 우린 data를 'user' 안에 담아 json 형태로 render 해줍니다.
        return json.dumps({
            'user': data
        })