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

from creative import Creative


REQUIRED_INLINE = ['AdSystem', 'AdTitle']
REQUIRED_WRAPPER = ['AdSystem', 'VASTAdTagURI']


def validateSettings(settings, requireds):
    keys = settings.keys()
    for required in requireds:
        if required not in keys:
            raise Exception("Missing required settings: {required}".format(required=required))


def validateInLineSettings(settings):
    validateSettings(settings, REQUIRED_INLINE)


def validateWrapperSettings(settings):
    validateSettings(settings, REQUIRED_WRAPPER)


class Ad(object):
    def __init__(self, settings={}):
        self.errors = []
        self.surveys = []
        self.impressions = []
        self.creatives = []

        if settings["structure"].lower() == 'wrapper':
            validateWrapperSettings(settings)
            self.VASTAdTagURI = settings["VASTAdTagURI"]
        else:
            validateInLineSettings(settings)

        self.id = settings["id"]
        self.sequence = settings.get("sequence", None)
        self.structure = settings["structure"]
        self.AdSystem = settings["AdSystem"]
        self.AdTitle = settings["AdTitle"]

        # optional elements
        self.Error = settings.get("Error", None)
        self.Description = settings.get("Description", None)
        self.Advertiser = settings.get("Advertiser", None)

        self.Pricing = settings.get("Pricing", None)
        self.Extensions = settings.get("Extensions", None)

    def attachSurvey(self, settings):
        survey={"url": settings.url}
        if "type" in settings:
            survey["type"] = settings["type"]
        self.surveys.append(survey)

    def attachImpression(self, settings):
        self.impressions.append(settings)
        return self

    def attachCreative(self, _type, options):
        creative = Creative(_type, options)
        self.creatives.append(creative)
        return creative

