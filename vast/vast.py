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

from ad import Ad
from xmlbuilder import XMLBuilder


class VAST(object):
    def __init__(self, settings={}):
        self.ads = []
        self.version = settings.get("version", "3.0")
        self.VASTErrorURI = settings.get("VASTErrorURI", None)

    def attachAd(self, settings):
        ad = Ad(settings)
        self.ads.append(ad)
        return ad

    def cdata(self, param):
        return "<![CDATA[{param}]]>".format(param=param)

    def add_creatives(self, response, ad, track):
        linearCreatives = [c for c in ad.creatives if c.type == "Linear"]
        nonLinearCreatives = [c for c in ad.creatives if c.type == "NonLinear"]
        companionAdCreatives = [c for c in ad.creatives if c.type == "CompanionAd"]
        with response.Creatives:
            for creative in linearCreatives:
                creativeOpts = {}
                with response.Creative:
                    if creative.skipoffset:
                        creativeOpts["skipoffset"] = creative.skipoffset
                    with response.Linear(**creativeOpts):
                        if len(creative.icons) > 0:
                            with response.Icons:
                                for icon in creative.icons:
                                    with response.Icon(**icon.attributes):
                                        attributes = {}
                                        if "creativeType" in icon.resource:
                                            attributes["creativeType"] = icon.resource["creativeType"]
                                        attr = getattr(response, icon.resource["type"])
                                        attr(self.cdata(icon.resource["uri"]), **attributes)
                                        if icon.click or icon.clickThrough:
                                            with response.IconClicks:
                                                if icon.clickThrough:
                                                    response.IconClickThrough(self.cdata(icon.clickThrough))
                                                if icon.click:
                                                    response.IconClickTraking(self.cdata(icon.click))
                                        if icon.view:
                                            response.IconViewTracking(self.cdata(icon.view))
                        response.Duration(creative.duration)
                        with response.TrackingEvents:
                            for event in creative.trackingEvents:
                                if track:
                                    attrs = {"event": event.event}
                                    if event.offset:
                                        attrs["offset"] = event.offset
                                    response.Tracking(self.cdata(event.url), **attrs)
                        if creative.AdParameters:
                            response.AddParameters(creative.AdParameters)
                        with response.VideoClicks:
                            for click in creative.videoClicks:
                                attr = getattr(response, click["type"])
                                attr(self.cdata(click["url"]), **{"id": click.get("id", "")})

                        with response.MediaFiles:
                            for media in creative.mediaFiles:
                                response.MediaFile(self.cdata(media["url"]), **media["attributes"])

            if len(nonLinearCreatives) > 0:
                for creative in nonLinearCreatives:
                    with response.Creative:
                        with response.NonLinearAds:
                            with response.NonLinear(**creative.attributes):
                                for resource in creative.resources:
                                    attrs = {}
                                    if "creativeType" in resource:
                                        attrs["creativeType"] = resource["creativeType"]
                                    element = getattr(response, resource["type"])
                                    element(self.cdata(resource["uri"]), **attrs)

                                for click in creative.clicks:
                                    element = getattr(response, click["type"])
                                    element(self.cdata(click["uri"]))

                                if creative.AdParameters:
                                    response.AdParameters(creative.AdParameters["data"], **{
                                        "xmlEncoded": creative.AdParameters["xmlEncoded"]
                                    })
                                if creative.nonLinearClickThrough:
                                    response.NonLinearClickThrough(self.cdata(creative.nonLinearClickThrough))
                                if creative.nonLinearClickTracking:
                                    response.NonLinearClickTracking(self.cdata(creative.nonLinearClickTracking))

            if len(companionAdCreatives) > 0:
                with response.CompanionAds:
                    for creative in companionAdCreatives:
                        with response.Companion(**creative.attributes):
                            for resource in creative.resources:
                                attrs = {}
                                element = getattr(response, resource["type"])
                                if "creativeType" in resource:
                                    attrs["creativeType"] = resource["creativeType"]
                                element(self.cdata(resource["uri"]), **attrs)
                                if "adParameters" in resource:
                                    response.AdParameters(resource["adParameters"]["data"], **{
                                        "xmlEncoded": resource["adParameters"]["xmlEncoded"]
                                    })
                            with response.TrakingEvents:
                                for event in creative.trackingEvents:
                                    if track:
                                        attrs = {"event": event.event}
                                        if event.offset:
                                            attrs["offset"] = event.offset
                                        response.Tracking(event.url, **attrs)

                            for click in creative.clickThroughs:
                                response.CompanionClickThrough(self.cdata(click))

                            if creative.nonLinearClickTracking:
                                response.NonLinearClickTracking(self.cdata(creative.nonLinearClickTracking))

    def xml(self, options={}):
        track = True if options.get("track", True)  else options.get("track")
        response = XMLBuilder('VAST', version=self.version)
        if len(self.ads) == 0 and self.VASTErrorURI:
            response.Error(self.cdata(self.VASTErrorURI))
            return response
        for ad in self.ads:
            adOptions = {"id": ad.id}
            if ad.sequence:
                adOptions["sequence"] = str(ad.sequence)

            with response.Ad(**adOptions):
                if ad.structure.lower() == 'wrapper':
                    with response.Wrapper:
                        response.AdSystem(ad.AdSystem["name"], **{"version": ad.AdSystem["version"]})
                        response.VASTAdTagURI(self.cdata(ad.VASTAdTagURI))
                        if ad.Error:
                            response.Error(self.cdata(ad.Error))
                        for impression in ad.impressions:
                            if track:
                                response.Impression(self.cdata(impression["url"]))
                        self.add_creatives(response, ad, track)
                else:
                    with response.InLine:
                        response.AdSystem(ad.AdSystem["name"], **{"version": ad.AdSystem["version"]})
                        response.AdTitle(self.cdata(ad.AdTitle))
                        response.Description(self.cdata(ad.Description or ''))

                        with response.Survey:
                            for survey in ad.surveys:
                                attributes = {}
                                if survey.type:
                                    attributes["type"] = survey.type
                                response.Survey(self.cdata(survey.url), **attributes)

                        if ad.Error:
                            response.Error(self.cdata(ad.Error))

                        for impression in ad.impressions:
                            if track:
                                response.Impression(self.cdata(impression["url"]))

                        self.add_creatives(response, ad, track)

                        if ad.Extensions:
                            for extension in ad.Extensions:
                                response.Extension(extension)
        return response
