import random
import rumps

from reddit_image_picker import RedditImagePicker
from app_preferences import Preferences

from AppKit import NSWorkspace, NSScreen
from Foundation import NSURL


class BackgroundsForRedditApp(rumps.App):
    """
        This is the main class for the application
        this class initalizes the app, and creates
        the buttons and timer functions
    """
    intervals_dict = {
        5: "5 seconds",
        10: "10 seconds",
        30: "30 seconds",
        60: "Minute",
        300: "5 minutes",
        3600: "Hour"
    }
    ordering_dict = {
        "hot" : "Hot",
        "top" : "Top",
        "new" : "New"
    }
    limit_dict = {
        "hour" : "Hour",
        "day" : "Day",
        "week" : "Week",
        "month" : "Month",
        "year" : "Year",
        "all" : "All"
    }
    def __init__(self):
        super(BackgroundsForRedditApp, self).__init__("Backgrounds")
        self.menu = [["Update every", ["5 seconds", "10 seconds", "30 seconds", "Minute", "5 minutes", "Hour", "Other"]], ["Ordering", ["Top", "Hot", "New"]], ["Limit", ["Hour", "Day", "Week", "Month", "Year", "All"]], "Subreddit", "Skip", "Pause"]

        # Store menus for toggling
        self.intervals_menu = self.menu["Update every"]
        self.ordering_menu = self.menu["Ordering"]
        self.limit_menu = self.menu["Limit"]

        # always try to set default preferences
        Preferences.setDefaults()
        # Then load our preferences
        self.preferences = Preferences()

        self.imagePicker = RedditImagePicker(self.preferences.subreddit, self.preferences.ordering, self.preferences.limit)

        self.timer = rumps.Timer(self.imagePicker.changeBackground, self.preferences.update_interval)
        self.timer.start()
        self.limit_menu = self.menu["Limit"]
        self.setOrdering(self.preferences.ordering)
        self.setUpdateInterval(self.preferences.update_interval)
        self.setLimit(self.preferences.limit)

    @rumps.clicked("Ordering", "Hot")
    def hot(self, sender):
        self.setOrdering("hot")

    @rumps.clicked("Ordering", "Top")
    def top(self, sender):
        self.setOrdering("top")

    @rumps.clicked("Ordering", "New")
    def new(self, sender):
        self.setOrdering("new")

    @rumps.clicked("Update every", "5 seconds")
    def prefs(self, sender):
        self.setUpdateInterval(5)

    @rumps.clicked("Update every", "10 seconds")
    def prefs(self, sender):
        self.setUpdateInterval(10)

    @rumps.clicked("Update every", "30 seconds")
    def prefs(self, sender):
        self.setUpdateInterval(30)

    @rumps.clicked("Update every", "Minute")
    def prefs(self, sender):
        self.setUpdateInterval(60)

    @rumps.clicked("Update every", "5 minutes")
    def prefs(self, sender):
        self.setUpdateInterval(300)

    @rumps.clicked("Update every", "Hour")
    def prefs(self, sender):
        self.setUpdateInterval(3600)

    @rumps.clicked("Update every", "Other")
    def prefs(self, sender):
        resp = rumps.Window("Please enter another interval you would to refresh at (in seconds)",
                        "Refresh rate",
                        "5"
                    ).run()
        # TODO: catch exceptions here
        interval = int(resp.text)
        self.setUpdateInterval(interval)

    @rumps.clicked("Limit", "Hour")
    def limit_hour(self, sender):
        self.setLimit("hour")

    @rumps.clicked("Limit", "Day")
    def limit_hour(self, sender):
        self.setLimit("day")

    @rumps.clicked("Limit", "Week")
    def limit_hour(self, sender):
        self.setLimit("week")

    @rumps.clicked("Limit", "Month")
    def limit_hour(self, sender):
        self.setLimit("month")

    @rumps.clicked("Limit", "Year")
    def limit_hour(self, sender):
        self.setLimit("year")

    @rumps.clicked("Limit", "All")
    def limit_hour(self, sender):
        self.setLimit("all")

    @rumps.clicked("Subreddit")
    def subreddit(self, sender):
        resp = rumps.Window("Please enter the subreddit you want to display for background pictures",
                        "Subreddit",
                        self.imagePicker.subreddit
                    ).run()
        self.preferences.setSubreddit(resp.text)
        self.imagePicker.setSubreddit(resp.text) # TODO: verify this is an actual subreddit

    @rumps.clicked("Skip")
    def skip(self, sender):
        self.imagePicker.changeBackground(self)

    @rumps.clicked("Pause")
    def pause(self, sender):
        if sender.title == "Pause":
            sender.title = "Play"
            self.timer.stop()
        else:
            sender.title = "Pause"
            self.timer.start()

    def toggleMenu(self, menus, sender):
        for menu in menus:
            if menus[menu].state:
                menus[menu].state = not menus[menu].state
        sender.state = True

    def setUpdateInterval(self, interval):
        self.preferences.setUpdateInterval(interval)
        if interval != self.timer.interval: # reset or initialize timer
            self.timer.stop()
            self.timer.interval = self.preferences.update_interval
            self.timer.start()
        self.toggleMenu(self.intervals_menu, self.intervals_menu[BackgroundsForRedditApp.intervals_dict.setdefault(interval, "Other")])

    def setOrdering(self, ordering):
        if ordering != "top" and self.menu.has_key("Limit"):
            del self.menu["Limit"]
        elif ordering == "top" and not self.menu.has_key("Limit"):
            self.menu.insert_after("Ordering", self.limit_menu)

        self.preferences.setOrdering(ordering)
        self.imagePicker.setOrdering(ordering)
        self.toggleMenu(self.ordering_menu, self.ordering_menu[BackgroundsForRedditApp.ordering_dict[ordering]])

    def setLimit(self, limit):
        self.preferences.setLimit(limit)
        self.imagePicker.setLimit(limit)
        self.toggleMenu(self.limit_menu, self.limit_menu[BackgroundsForRedditApp.limit_dict[limit]])


if __name__ == "__main__":
    BackgroundsForRedditApp().run()
