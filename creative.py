#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015 Timu Eren <timu.eren@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
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


from companionAd import CompanionAd
from icon import Icon
from trackingEvent import TrackingEvent

VALID_VIDEO_CLICKS = ['ClickThrough', 'ClickTracking', 'CustomClick']


class Creative(object):
    def __init__(self, _type, settings=None):
        settings = {} if settings is None else settings
        self.type = _type
        self.mediaFiles = []
        self.trackingEvents = []
        self.videoClicks = []
        self.clickThroughs = []
        self.clicks = []
        self.resources = []
        self.icons = []
        self.AdParameters = settings.get("AdParameters", None)
        self._adParameters = None
        self.attributes = {}
        self.duration = settings.get("Duration", None)
        self.skipoffset = settings.get("skipoffset", None)
        self.nonLinearClickEvent = None

        if _type == "Linear" and self.duration is None:
            raise Exception('A Duration is required for all creatives. Consider defaulting to "00:00:00"')

        if "id" in settings:
            self.attributes["id"] = settings["id"]

        if "width" in settings:
            self.attributes["width"] = settings["width"]
        if "height" in settings:
            self.attributes["height"] = settings["height"]
        if "expandedWidth" in settings:
            self.attributes["expandedWidth"] = settings["expandedWidth"]
        if "expandedHeight" in settings:
            self.attributes["expandedHeight"] = settings["expandedHeight"]
        if "scalable" in settings:
            self.attributes["scalable"] = settings["scalable"]
        if "maintainAspectRatio" in settings:
            self.attributes["maintainAspectRatio"] = settings["maintainAspectRatio"]
        if "minSuggestedDuration" in settings:
            self.attributes["minSuggestedDuration"] = settings["minSuggestedDuration"]
        if "apiFramework" in settings:
            self.attributes["apiFramework"] = settings["apiFramework"]

    def attachMediaFile(self, url, settings={}):
        media_file = {"attributes": {}}
        media_file["url"] = url
        media_file["attributes"]["type"] = settings.get("type", 'video/mp4')
        media_file["attributes"]["width"] = settings.get("width",'640')
        media_file["attributes"]["height"] = settings.get("height", '360')
        media_file["attributes"]["delivery"]= settings.get("delivery",  'progressive')
        if "id" not in settings:
            raise Exception('an `id` is required for all media files')

        media_file["attributes"]["id"] = settings["id"]
        if "bitrate" in settings:
            media_file["attributes"]["bitrate"] = settings["bitrate"]
        if "minBitrate" in settings:
            media_file["attributes"]["minBitrate"] = settings["minBitrate"]
        if "maxBitrate" in settings:
            media_file["attributes"]["maxBitrate"] = settings["maxBitrate"]
        if "scalable" in settings:
            media_file["attributes"]["scalable"] = settings["scalable"]
        if "codec" in settings:
            media_file["attributes"]["codec"] = settings["codec"]
        if "apiFramework" in settings:
            media_file["attributes"]["apiFramework"] = settings["apiFramework"]
        if "maintainAspectRatio" in settings:
            media_file["attributes"]["maintainAspectRatio"] = settings["maintainAspectRatio"]

        self.mediaFiles.append(media_file)
        return self

    def attachTrackingEvent(self, _type, url, offset=None):
        self.trackingEvents.append(TrackingEvent(_type, url, offset))
        return self

    def attachVideoClick(self, _type, url, _id=''):
        if _type not in VALID_VIDEO_CLICKS:
            raise Exception('The supplied VideoClick `type` is not a valid VAST VideoClick type.')
        self.videoClicks.append({"type": _type, "url": url, "id": _id})
        return self

    def attachClickThrough(self, url):
        self.clickThroughs.append(url)
        return self

    def attachClick(self, uri, _type=None):
        if isinstance(uri, basestring):
            _type = 'NonLinearClickThrough'
        self.clicks = [{"type": _type, "uri": uri}]
        return self

    def attachResource(self, _type, uri, creative_type=None):
        resource = {"type": _type, "uri": uri}
        if _type == 'HTMLResource':
            resource["html"] = uri
        if creative_type is not None:
            resource["creativeType"] = creative_type
        self.resources.append(resource)
        return self

    def attachIcon(self, settings):
        icon = Icon(settings)
        self.icons.append(icon)
        return icon

    def adParameters(self, data, xml_encoded):
        self._adParameters = {"data": data, "xmlEncoded": xml_encoded}
        return self

    def attachNonLinearClickTracking(self, url):
        self.nonLinearClickEvent = url