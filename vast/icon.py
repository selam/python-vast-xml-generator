#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015 Timu Eren <timu.eren@gmail.com>
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

REQURED_ATTRIBUTES = ["program", "width", "height", "xPosition", "yPosition"]


class Icon(object):
    def __init__(self, settings=dict()):
        keys = settings.keys()
        for required in keys:
            if required not in keys:
                raise Exception("Missing required attribute '{attr}'".format(attr=required))

        self.attributes = {}
        self.attributes.update(settings)
        self.resource = None
        self.clickThrough = None
        self.click = None
        self.view = None

    def setResource(self, _type, uri, creativeType=None):
        if _type not in ('StaticResource', "IFrameResource", "HTMLResource"):
            raise Exception("Invalid resource type")

        resource = {"type": _type, "uri": uri}
        if _type == 'HTMLResource':
            resource["html"] = uri
        if creativeType:
            resource["creativeType"] = creativeType
        self.resource = resource

    def setClickThrough(self, uri):
        self.clickThrough = uri
        return self

    def setClickTracking(self, uri):
        self.click = uri
        return self

    def setViewTracking(self, uri):
        self.view = uri
        return self
