# python-vast-xml-generator
if you plan to write an video ad server with vast support you can generate xml response using this lib, 

## Example
#### Create instance
```python
vast = VAST({"version":"3.0", "VASTErrorURI": "optional url if something went wrong in client side"}) # create instance of vast object, version is vast version, 
```


#### Adding Ad
```python
ad = vast.attachAd({ 
    "id": "1", # ad id 
    "structure": 'inline', # or "wrapper", 
    "sequence": "1", # optional, not required
    "Error": 'http://error.err', # error url if something went wrong in client side, optional
    "AdTitle": 'Common name of the ad' # required for inline structure, 
    "AdSystem": { "name": 'name of adserver or company', "version": "1.0"  }, 
    "Description": "optional description of ad",
    "Advertiser": "Optional name of advertiser",
    "Pricing": "Optional price (if you want to RTB on vast)",
    "Extensions": """<xml>xml extension for client side</xml>""",
  })
```


#### Add Impression url 
```python 
# you can add many servers if you need to
ad.attachImpression({
    "id": "servername"
   "url": "impression url"
})
```
#### Add Linear Creative 
```python
# you can give any valid VAST XmlTagName and value for Creative
creative = ad.attachCreative('Linear', {
    "AdParameters" : """<xml></xml>""", #Optional
    "Duration" : '00:00:30' # required for linear type
});
# you can give any valid VAST XmlTagName and value for media file
creative.attachMediaFile('file url', {
   "type": "video/mp4",
   "bitrate": "320",
   "minBitrate": "320",
   "maxBitrate": "320",
   "width": "640",
   "height": "360",
   "scalable": "true",
   "maintainAspectRatio": "true",
   "codec": "",
   "apiFramework": "VPAID",
});

# You can add any valid  tracking events: vast/trackingEvent.py#L18
creative.attachTrackingEvent('creativeView', 'server url');
# many times 
creative.attachTrackingEvent('progress', 'server url', '00:00:01');
#
creative.attachVideoClick('ClickThrough', 'click target url');
creative.attachClickThrough("Url of server")
creative.attachClick("Url") # look at the vast 3.0 documentation 

vast.xml() // returns XMLBuilder object, to print str(vast.xml()) 

```
