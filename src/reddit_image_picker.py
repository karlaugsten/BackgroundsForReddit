import praw
import urllib
import os
import uuid
import sys, traceback

from AppKit import NSWorkspace, NSScreen, NSDistributedNotificationCenter, NSWorkspaceDesktopImageAllowClippingKey, NSWorkspaceDesktopImageScalingKey, NSImageScaleProportionallyUpOrDown, NSDictionary
from Foundation import NSURL
from PIL import Image
from flufl.enum import Enum
from secrets import client_id, client_secret

class Ordering(Enum):
    """
        Class to enumerate ordering types
        for reddit listings
    """
    hot = 1
    top = 2
    new = 3

class RedditImage():
    """
        A class to hold properties of the image,
        as well as the file location
    """
    def __init__(self, url):
        self.url = url
        self.saved = False

    def save(self, path=None):
        if self.saved is True: return # do nothing

        self.path = path
        if self.path is None:
            self.path = '/tmp/'+ str(uuid.uuid4()) # only create random file if its not specified

        urllib.urlretrieve(self.url, self.path) # TODO: possible 404 errors, need to handle this
        self.saved = True
        self.image = Image.open(self.path)
        # verify image is correct (i.e. its not an html by mistake or something)
        self.image.verify() # throws an error
        self.width, self.height = self.image.size
        print("Downloaded image: " + self.url + " with size: " + str(self.width) + " " + str(self.height))

class RedditImagePicker():
    """
        A simple class to pick images from a reddit
        subreddit using praw
    """
    def __init__(self, subreddit, ordering, limit):
        self.reddit = praw.Reddit(user_agent='Test script by /u/Karklenator', client_id=client_id, client_secret=client_secret)
        self.subreddit = subreddit
        self.images = []
        self.last_image = None
        self.ordering = Ordering[ordering]
        self.limit = limit

    def setOrdering(self, ordering):
        new_ordering = Ordering[ordering]
        if self.ordering is not new_ordering:
            self.images = [] # reset images to load new ones
            self.last_image = None
        self.ordering = new_ordering

    def setLimit(self, limit):
        if self.limit is not limit:
            self.images = [] # reset images to load new ones
            self.last_image = None
        self.limit = limit

    def nextImage(self):
        while self.images == []: # keep trying to retrieve images from listing
            param = {'after': self.last_image}
            print "Retrieving more images after " + str(self.last_image)
            if self.ordering is Ordering.top:
                param['t'] = self.limit # set the limit only for top
                submissions = self.reddit.subreddit(self.subreddit).top(limit=10, params=param)
            elif self.ordering is Ordering.hot:
                submissions = self.reddit.subreddit(self.subreddit).hot(limit=10, params=param)
            elif self.ordering is Ordering.new:
                submissions = self.reddit.subreddit(self.subreddit).new(limit=10, params=param)

            self.last_image = None
            for submission in submissions:
                self.last_image = submission.fullname
                if ".jpg" in submission.url or ".png" in submission.url:
                    image = RedditImage(submission.url)
                    self.images.append(image)

        return self.images.pop(0)

    def setSubreddit(self, sub):
        self.images = []
        self.subreddit = sub

    def changeBackground(self, sender):
        # Just surround the whole method in a giant try/catch block because why the hell not?
        try:
            next_image = self.nextImage()
            while next_image.saved == False:
                try:
                    if not next_image.saved: next_image.save()
                except Exception as e:
                    print 'Error saving image: ' + str(e)
                    next_image = self.nextImage()

            print("Changing background to image: " + next_image.path)
            # generate a fileURL for the desktop picture
            file_url = NSURL.fileURLWithPath_(next_image.path)

            # set up options for background image
            options = {
                NSWorkspaceDesktopImageAllowClippingKey : False,
                NSWorkspaceDesktopImageScalingKey: NSImageScaleProportionallyUpOrDown
            }

            # get shared workspace
            ws = NSWorkspace.sharedWorkspace()

            # iterate over all screens
            for screen in NSScreen.screens():
                # We have to cast the options dict to a NSDictionary, dont know why??
                nsoptions = NSDictionary.dictionaryWithDictionary_(options)
                # tell the workspace to set the desktop picture
                (result, error) = ws.setDesktopImageURL_forScreen_options_error_(
                file_url, screen, options, None)

            # This currently does nothing?
            # NSDistributedNotificationCenter.defaultCenter().postNotificationName_object_("com.apple.desktop", "BackgroundChanged")
        except Exception as e:
            print str(e) # Actually do this because pyobjc will just throw a cryptic error otherwise that is impossible to debug
            print e.args
            traceback.print_exc(file=sys.stdout)
