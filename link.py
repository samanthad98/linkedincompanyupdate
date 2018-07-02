import requests

class token(object):
    def __init__(self, accesstoken, expire):
        self.accesstoken = accesstoken
        self.expire = expire

# Implement a outh2 authorization process
class Linkedinauth(object):
    AUTHORIZE = 'https://www.linkedin.com/oauth/v2/authorization'
    ATOKEN = 'https://www.linkedin.com/oauth/v2/accessToken'

    def __init__(self, clientid, clientsecret, redirect_uri):
        self.key = clientid
        self.secret = clientsecret
        self.redirect = redirect_uri
        self.state = '987654321'
        self.scope = ['rw_company_admin']
        self.authorization_code = None
        self.token = None

    # start the authorization process
    def getauthorizationurl(self):
        param = {'scope':'rw_company_admin',
                 'state':self.state,
                 'redirect_uri':self.redirect,
                 'client_id':self.key,
                 'response_type':'code'
        }
        output = []
        for k, v in param.items():
            output.append('%s=%s' % (k, v))
        url = '%s?%s' % (self.AUTHORIZE, '&'.join(output).strip())
        return url

    def setcode(self, code):
        self.authorization_code = code
        return self.authorization_code

    def getaccesstoken(self):
        param = {'grant_type':'authorization_code',
                 'code':self.authorization_code,
                 'redirect_uri':self.redirect,
                 'client_id' = self.key,
                 'client_secret' = self.secret
                 }
        res = requests.post(self.ATOKEN, data=param,timeout=50)
        self.token = token(res['access_token'],res['expires_in'])
        return self.token

    def makereq(self, method, url, param=None, header=None):
        if param = None:
            param = {}
        if header = None:
            header = {'Host': 'api.linkedin.com',
                      'Connection': 'Keep-Alive',
                      'Authorization': 'Bearer '+self.token.accesstoken,
                      'Content-Type': 'application/json',
                      'x-li-format': 'json'}
        else:
            nheader = {'Host': 'api.linkedin.com',
                      'Connection': 'Keep-Alive',
                      'Authorization': 'Bearer '+self.token.accesstoken,
                      'Content-Type': 'application/json',
                      'x-li-format': 'json'}
            header.update(nheader)
        return requests.request(method.upper(),headers=header,params=param,timeout=50)
