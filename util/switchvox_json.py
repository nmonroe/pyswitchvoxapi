import json
from decimal import Decimal
from datetime import datetime


class switchvox_jsonencoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, datetime):
            sv_dtformat = '%Y-%m-%d %H:%M:%S'
            return obj.strftime(sv_dtformat)
        return json.JSONEncoder.default(self, obj)
