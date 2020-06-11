# HMS library to send Android push notifications for Python

hms-python requires Python 3.6 or later.

Basic Usage
-----------

```python
from hms.connection import HmsConnection
from hms.models import AndroidNotification
from hms.exceptions import ApiCallError


async def main():
  app_id = 1234567
  secret = "<APP_SECRET>"
  connection = HmsConnection(app_id, secret)
  await connection.connect()

  notification={
    "title": "Hello world hcm",
    "body": "This is notification body",
    "sound": "default"
  }
  message = AndroidNotification(token=["<TOKEN>"],
                                     collapse_key=-1,
                                     ttl='86400s',
                                     priority=AndroidNotification.PRIORITY_HIGH,
                                     notification=notification
                                     )

  await connection.send_message(message)
  await connection.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
 ```
