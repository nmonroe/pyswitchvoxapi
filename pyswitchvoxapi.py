from copy import copy
import requests
import json

from util.switchvox_json import switchvox_jsonencoder


class switchvox_api(object):

    def __init__(
        self, server, user, password,
        verifycert=False, autoitemspp=200
    ):
        # update self variables with input
        self.__dict__.update(locals())
        self.serverurl = 'https://%s/json' % (server)
        # setup requests session
        self.session = requests.Session()
        self.session.auth = requests.auth.HTTPDigestAuth(user, password)
        self.session.headers.update({'content-type': 'application/json'})

    def _do_request(self, req):
        data = json.dumps(req, cls=switchvox_jsonencoder)
        r = self.session.post(
            self.serverurl,
            verify=self.verifycert,
            data=data
        )
        response = r.json()
        try:
            # see if the request errored out
            response['response']['errors']
        except KeyError:
            return response
        self._raise_exception(response)

    def _raise_exception(self, errors):
        # get errors and raise RuntimeError with detailed message
        base_message = "\nSwitchvox API Error.\n  Method: %s" % \
            (errors['response']['method'])
        message = ""
        actual_errors = errors['response']['errors']['error']
        if type(actual_errors) is dict:
            error = errors['response']['errors']['error']
            message += "\n    Code: %s - Message: %s" % \
                (error['code'], error['message'])
        elif type(actual_errors) is list:
            for error in actual_errors:
                message += "\n    Code: %s - Message: %s" % \
                    (error['code'], error['message'])
        raise RuntimeError(base_message + message)

    def _do_call(self, method, **kwargs):
        req = {"request": {"method": method, "parameters": kwargs}}
        return self._do_request(req)

    def _call_autopaginate(self, method, **kwargs):
        call_args = copy(kwargs)
        call_args['page_number'] = 1
        call_args['items_per_page'] = self.autoitemspp
        data = self._do_call(method, **call_args)
        result = data['response']['result']
        infokey = result.keys()[0]
        total_pages = int(result[infokey]['total_pages'])
        while call_args['page_number'] < total_pages:
            call_args['page_number'] += 1
            nextdata = self._do_call(method, **call_args)
            d = nextdata['response']['result'][infokey]
            for key in d:
                if type(d[key]) is list:
                    for item in d[key]:
                        data['response']['result'][infokey][key].append(item)
        removekeys = ['page_number', 'items_per_page', 'total_pages']
        for k in removekeys:
            result[infokey].pop(k)
        return data

    def call_method(self, method, autopage=False, **kwargs):
        if autopage:
            return self._call_autopaginate(method, **kwargs)
        return self._do_call(method, **kwargs)
