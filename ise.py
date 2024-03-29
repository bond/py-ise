import json
import requests

class ISEError(Exception):
  """Base class for ISE related Exceptions"""
  pass

class ISEAuthError(ISEError):
  """Exception raised for authentication errors

  Attributes:
    message -- explaination of the error
  """
  def __init__(self, message):
    self.message = message

class ISENotFoundError(ISEError):
  """Exception raised for authentication errors

  Attributes:
    message -- explaination of the error
  """
  def __init__(self, message):
    self.message = message

class API:

  API_MAX_SIZE = 100

  def __init__(self, hostname=None, user=None, password=None, debug=False, port=9060, cabundle='/etc/pki/tls/certs/ca-bundle.crt'):

    if not hostname: raise ValueError('hostname must be provided as argument')
    if not user: raise ValueError('user must be provided as argument')
    if not password: raise ValueError('password must be providided as argument')

    self.hostname = hostname
    self.user = user
    self.password = password
    self.port = port
    self.debug = debug
    self.cabundle = cabundle

  def uri_for_path(self, path=None, page=None, size=None):
    query=[]
    if page != None: query.append('page={}'.format(page))
    if size != None: query.append('size={}'.format(size))

    uri = "https://{0}:{1}/ers{2}".format(
      self.hostname,
      self.port,
      path,
      size,
      page)

    if query: uri = uri + "?" + "&".join(query)
    return uri

  def get(self, uri):
    if self.debug: print("Getting api-data from: " + uri)
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    resp = requests.get(uri, headers=headers, auth=requests.auth.HTTPBasicAuth(self.user, self.password), verify=self.cabundle)
    if resp.status_code == 200:
      return resp
    elif resp.status_code == 401:
      raise ISEAuthError("Authentication failed for user '{}'".format(self.user))
    elif resp.status_code == 404:
      raise ISENotFoundError("ISE returned 404 for resource: {}".format(uri))
    else:
      raise ISEError("Ise returned {0} for resource: {1}".format(resp.status_code, uri))

  def get_resource(self, uri):
    return json.loads(self.get(uri).content)

  def get_all_resources(self, uri, filter=None):

    # store results in array
    resources = []

    resp = self.get(uri)
    data = json.loads(resp.content)
    if self.debug: print("Got {} resouces".format(len(data["SearchResult"]["resources"])))

    # for each resources, get full data from API with new request
    for idx, resource in enumerate(data["SearchResult"]["resources"]):
      resources.append(self.get_resource(resource["link"]["href"]))

    # get all pages recursively
    if 'nextPage' in data["SearchResult"] and data["SearchResult"]["nextPage"]["href"] != "":
      next_page_resources = self.get_all_resources(data["SearchResult"]["nextPage"]["href"])
      resources.append(next_page_resources)

    # return all the resources
    return resources

  def networkdevice(self, uuid):
    return self.get_resource(self.uri_for_path('/config/networkdevice/{}'.format(uuid)))

  def networkdevicegroups(self, filter=None):
    return self.get_all_resources(self.uri_for_path('/config/networkdevicegroup', size=self.API_MAX_SIZE))

  def networkdevices(self, filter=None):
    return self.get_all_resources(self.uri_for_path('/config/networkdevice', size=self.API_MAX_SIZE))
    
