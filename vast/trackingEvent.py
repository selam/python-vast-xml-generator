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

VALID_TRACKING_EVENT_TYPES = [
    'creativeView',
    'start',
    'firstQuartile',
    'midpoint',
    'thirdQuartile',
    'complete',
    'mute',
    'unmute',
    'pause',
    'rewind',
    'resume',
    'fullscreen',
    'exitFullscreen',
    'skip',
    'progress',

    'expand',
    'collapse',
    'acceptInvitationLinear',
    'closeLinear'
]


class TrackingEvent(object):
    def __init__(self, event, url, offset=None):
        self.offset = None
        self.event = None
        self.url = None

        if event not in VALID_TRACKING_EVENT_TYPES:
            raise Exception("""The supplied Tracking `event` {event} is not a valid Tracking event.
            Valid tracking events: {events}""".format(
                event=event,
                events=",".join(VALID_TRACKING_EVENT_TYPES)
            ))

        if event == "progress":
            if offset is None:
                raise Exception("Offset must be present for `progress` TrackingEvent.")
            self.offset = offset
        self.event = event
        self.url = url
