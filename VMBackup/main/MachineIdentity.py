#!/usr/bin/env python
#
# VM Backup extension
#
# Copyright 2014 Microsoft Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import subprocess
import xml
import xml.dom.minidom

class MachineIdentity:
    def __init__(self):
        self.store_identity_file = './machine_identity_FD76C85E-406F-4CFA-8EB0-CF18B123365C'

    def current_identity(self):
        identity = None
        self.file = None
        try:
            if os.path.exists("/var/lib/waagent/HostingEnvironmentConfig.xml"):
                self.file = open("/var/lib/waagent/HostingEnvironmentConfig.xml",'r')
                xmlText = self.file.read()
                dom = xml.dom.minidom.parseString(xmlText)
                deployment = dom.getElementsByTagName("Role")
                identity=deployment[0].getAttribute("guid")
        finally:
            if self.file != None:
                if self.file.closed == False:
                    self.file.close()
        return identity

    def save_identity(self):
        self.file = None
        try:
            self.file = open(self.store_identity_file,'w')
            machine_identity = self.current_identity()
            if( machine_identity != None ):
                self.file.write(machine_identity)
        finally:
            if self.file != None:
                if self.file.closed == False:
                    self.file.close()

    def stored_identity(self):
        identity_stored = None
        self.file = None
        try:
            if(os.path.exists(self.store_identity_file)):
                self.file = open(self.store_identity_file,'r')
                identity_stored = self.file.read()
        finally:
            if self.file != None:
                if self.file.closed == False:
                    self.file.close()
        return identity_stored

