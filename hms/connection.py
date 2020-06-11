
import json
import time
from typing import Optional
from aiohttp import ClientSession, ClientTimeout
from urllib.parse import urlencode
from hms.models import SendResponse, AndroidNotification
from hms.exceptions import ApiCallError


class HmsConnection(object):
    __slots__ = ('app_id', 'app_secret', 'token_expired_time',
                 'access_token', 'push_open_url', 'token_server', 'push_server_url', 'timeout', 'request_session')

    def __init__(self, app_id: str, app_secret: str, timeout: int = 15,
                 token_server='https://oauth-login.cloud.huawei.com/oauth2/v2/token',
                 push_open_url='https://push-api.cloud.huawei.com'):

        self.app_id = app_id
        self.app_secret = app_secret
        self.timeout = timeout
        self.token_expired_time = 0
        self.access_token = None
        self.token_server = token_server
        self.push_open_url = push_open_url
        self.push_server_url = self.push_open_url + "/v1/{0}/messages:send"
        self.request_session = None  # type: Optional[ClientSession]

    async def connect(self):
        timeout_client = ClientTimeout(total=self.timeout)
        self.request_session = ClientSession(timeout=timeout_client)
        await self._update_token()

    async def close(self):
        if self.request_session:
            await self.request_session.close()

    async def _refresh_token(self):
        headers = dict()
        headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'

        params = dict()
        params['grant_type'] = 'client_credentials'
        params['client_secret'] = self.app_secret
        params['client_id'] = self.app_id

        msg_body = urlencode(params)

        try:
            status, response = await self.post(self.token_server, msg_body, headers)

            if status != 200:
                return False, 'http status code is {0} in get access token'.format(status)

            response_body = json.loads(response)

            self.access_token = response_body.get('access_token')
            self.token_expired_time = int(round(time.time() * 1000)) + \
                                      (int(response_body.get('expires_in')) - 5 * 60) * 1000

            return True, None
        except Exception as e:
            raise ApiCallError(format(repr(e)))

    def _is_token_expired(self):
        if self.access_token is None:
            return True
        return int(round(time.time() * 1000)) >= self.token_expired_time

    async def _update_token(self):
        if self._is_token_expired() is True:
            print('Token expired')
            result, reason = await self._refresh_token()
            if result is False:
                raise ApiCallError(reason)

    def _create_header(self):
        headers = dict()
        headers['Content-Type'] = 'application/json;charset=utf-8'
        headers['Authorization'] = 'Bearer {0}'.format(self.access_token)
        return headers

    async def send(self, message: AndroidNotification, validate_only: bool) -> SendResponse:
        await self._update_token()
        headers = self._create_header()
        url = self.push_server_url.format(self.app_id)
        msg_body_dict = dict()
        msg_body_dict['validate_only'] = validate_only
        msg_body_dict['message'] = message.as_dict()

        print(message.as_dict())

        return await self._send_to_server(headers, msg_body_dict, url)

    async def _send_to_server(self, headers, body, url):
        try:
            msg_body = json.dumps(body)
            status, response = await self.post(url, msg_body, headers)

            if status != 200:
                raise ApiCallError('http status code is {0} in send.'.format(status))

            resp_dict = json.loads(response)
            return SendResponse(resp_dict)
        except Exception as e:
            raise ApiCallError('caught exception when send. {0}'.format(e))

    async def post(self, url, req_body, headers=None):
        try:
            async with self.request_session.post(url, data=req_body, headers=headers, ) as response:
                res_text = await response.text()
                return response.status, res_text
        except Exception as e:
            raise ValueError('caught exception when post {0}. {1}'.format(url, e))
