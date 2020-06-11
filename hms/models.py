import json
from typing import Dict, Any, List
from hms.utils import Utils


class Notification(object):
    __slots__ = ('title', 'body', 'image')

    def __init__(self, title=None, body=None, image=None):
        self.title = title
        self.body = body
        self.image = image


class AndroidNotification(object):
    __slots__ = ('notification', 'data', 'priority',
                 'token', 'ttl', 'collapse_key')

    PRIORITY_LOW = "LOW"
    PRIORITY_DEFAULT = "NORMAL"
    PRIORITY_HIGH = "HIGH"

    def __init__(self, token: List,
                 collapse_key: int,
                 ttl: str, priority: str,
                 notification: Notification = None, data: Dict[str, Any] = None):

        self.data = data
        self.notification = notification
        self.token = token
        self.priority = priority
        self.collapse_key = collapse_key
        self.ttl = ttl

    def as_dict(self) -> Dict[str, Any]:
        android_payload = {
                'collapse_key': self.collapse_key,
                'urgency': self.priority,
                'ttl': self.ttl,
                'fast_app_target': 2,
                'notification': None,
                'data': json.dumps(self.data) if self.data else None
            }
        return {
            'token': self.token,
            'android': Utils.remove_empty_and_none_values(android_payload)
        }


class HmsCodeStatus:
    CODE_SUCCESS = '80000000'
    CODE_TOKEN_INVALID = '80300007'
    CODE_TOKEN_PARAMETERS_INCORRECT = '80100001'
    CODE_AUTH_ERROR = '80200001'
    CODE_AUTH_EXPIRED = '80200003'
    CODE_BODY_TOO_LONG = '80300008'
    CODE_INCORRECT_MESSAGE_STRUCTURE = '80100003'
    CODE_SYSTEM_ERROR = '81000001'


class SendResponse(object):
    __slots__ = ('_code', '_msg', '_request_id')

    def __init__(self, response=None):
        self._code = response['code'] if 'code' in response else 0
        self._msg = response['msg'] if 'msg' in response else ''
        self._request_id = response['requestId'] if 'requestId' in response else None

    @property
    def code(self):
        return self._code

    @property
    def reason(self):
        return self._msg

    @property
    def request_id(self):
        return self._request_id

    @property
    def is_successful(self):
        return self._code == HmsCodeStatus.CODE_SUCCESS

    @property
    def error(self):
        return """{}: {}""".format(str(self._code), self._msg)

    def __str__(self):
        data = [
            '    {}={} ({})'.format(str(key), str(getattr(self, key)), type(getattr(self, key)))
            for key in self.__slots__
        ]
        data = ',\n'.join(data)
        data = self.__class__.__name__ + ' {\n' + data + '\n}'
        return data
