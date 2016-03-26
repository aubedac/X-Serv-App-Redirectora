#!/usr/bin/python

#
# Proxy class
# Simple web application for proxying to the web
# Accepts "GET /resource", and returns the content of
#   http://resource. For example, if /gsyc.es is used,
#   it returns the content of http://gsyc.es
#
# Copyright Jesus M. Gonzalez-Barahona 2009
# jgb @ gsyc.es
# SARO and SAT subjects (Universidad Rey Juan Carlos)
# March 2015
#

import webapp
import urllib2
import sys

class proxyApp (webapp.webApp):
    """Simple web application for proxying to the web."""

    def parse (self, request):
        """Return the resource name (/ removed)"""
        try:
            resourceName = request.split(' ', 2)[1][1:]
            self.diccClient[self.counterClient] = request
        except IndexError:
            resourceName = ""

        return (resourceName, request)

    def process (self, resource):
        """Process the relevant elements of the request.
        """
        resourceName, request = resource
        try:
            if resourceName == "httpClient":
                requestClient = self.diccClient[self.counterClient]
                httpBody = '<html><body>' + requestClient + '</br></body></html>'
                httpCode = "200 OK"
            elif resourceName == "httpProxy":
                headersProxy = self.diccProxy[self.counterProxy]
                httpBody = '<html><body>' + ' '.join(headersProxy) + '</br></body></html>'
                httpCode = "200 OK"
            elif resourceName == "reload/":
                f = urllib2.urlopen(str(self.url))
                httpBody = f.read()
                httpCode = "302 Found"
            elif resourceName == "":
                httpBody = "Error: could not connect"
                httpCode = "404 Resource Not Available"
            else:
                sourceUrl = "http://" + resourceName
                self.url = sourceUrl
                f = urllib2.urlopen(sourceUrl)
                headers = f.info().headers
                self.diccProxy[self.counterProxy] = headers
                httpBody = f.read()
                index1 = httpBody.find("<body")
                index2 = httpBody.find(">")
                urlOriginal = '<a href=' + sourceUrl + '>' + "Original Webpage" + '</a></br>'
                urlOriginal += '<a href=httpProxy>' + "Server-Side HTTP" + '</a></br>'
                urlOriginal += '<a href=httpClient>' + "Client-Side HTTP" + '</a></br>'
                urlOriginal += '<a href=reload/>' + "Reload" + '</a></br>'
                httpBody = httpBody[:index1] + urlOriginal + httpBody[index2+1:]
                httpCode = "200 OK"
        except IOError:
                httpBody = "Error: could not connect"
                httpCode = "404 Resource Not Available"

        return (httpCode, httpBody)

    def __init__(self, hostname, port):
        self.diccClient = {}
        self.diccProxy = {}
        self.counterClient = 0
        self.counterProxy = 0
        self.url = ""
        try:
            super(proxyApp, self).__init__(hostname, port)
        except KeyboardInterrupt:
            sys.exit()

if __name__ == "__main__":
    testProxyApp = proxyApp ("localhost", 1234)
