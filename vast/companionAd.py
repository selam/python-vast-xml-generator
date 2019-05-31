#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015 Timu Eren <timu.eren@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use self file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from trackingEvent import TrackingEvent


class CompanionAd(object):
    def __init__(self, resource, settings={}):
        self.resource = resource
        self.type = settings.get("type", None)
        self.url = settings.get("url", None)
        self.AdParameters = settings.get("AdParameters", None)
        self.AltText = settings.get("AltText", None)
        self.CompanionClickThrough = settings.get("CompanionClickThrough", None)
        self.CompanionClickTracking = settings.get("CompanionClickTracking", None)
        self.width = settings.get("width", None)
        self.height = settings.get("height", None)
        self.trackingEvents = []

    def attachTrackingEvent(self, type, url):
        self.trackingEvents.append(TrackingEvent(type, url))
