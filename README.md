pyswitchvoxapi
==============

Python bindings for the switchvox json api.


depends on requests library:
    http://docs.python-requests.org/en/latest/

Method listing:
    http://developers.digium.com/switchvox/wiki/index.php/WebService_methods


Usage example:

    from pyswitchvoxapi import switchvox_api
    from datetime import datetime, timedelta

    switchvox = switchvox_api(
        'servername', 'username', 'password',
        verifycert=False, autoitemspp=200
    )
    calldata = switchvox.call_method(
        "switchvox.callLogs.search",
        start_date=datetime.now() - timedelta(hours=4),
        end_date=datetime.now(),
        autopage=True
    )
