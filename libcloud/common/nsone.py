# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict, List

from libcloud.common.base import JsonResponse, ConnectionKey

__all__ = ["API_HOST", "NsOneException", "NsOneResponse", "NsOneConnection"]

# Endpoint for nsone api
API_HOST = "api.nsone.net"


class NsOneResponse(JsonResponse):
    errors = []  # type: List[Dict]
    objects = []  # type: List[Dict]

    def __init__(self, response, connection):
        super(NsOneResponse, self).__init__(response=response, connection=connection)
        self.errors, self.objects = self.parse_body_and_errors()
        if not self.success():
            raise NsOneException(code=self.status, message=self.errors.pop()["message"])

    def parse_body_and_errors(self):
        js = super(NsOneResponse, self).parse_body()
        if "message" in js:
            self.errors.append(js)
        else:
            self.objects.append(js)

        return self.errors, self.objects

    def success(self):
        return len(self.errors) == 0


class NsOneConnection(ConnectionKey):
    host = API_HOST
    responseCls = NsOneResponse

    def add_default_headers(self, headers):
        headers["Content-Type"] = "application/json"
        headers["X-NSONE-KEY"] = self.key

        return headers


class NsOneException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        self.args = (code, message)

    def __str__(self):
        return "%s %s" % (self.code, self.message)

    def __repr__(self):
        return "NsOneException %s %s" % (self.code, self.message)
