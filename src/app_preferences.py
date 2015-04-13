from AppKit import NSWorkspace, NSDictionary, NSUserDefaults


class Preferences():
    """
        A class to handle changes in
        application preferences, save, edit
        and retrieve them..
    """
    ordering_key = "ordering"
    ordering_default = "top"
    update_interval_key = "update_interval"
    update_interval_default = 30
    subreddit_key = "subreddit"
    subreddit_default = "EarthPorn"
    limit_key = "limit"
    limit_default = "all"

    def __init__(self):
        # load the application preferences
        user_defaults = NSUserDefaults.standardUserDefaults()

        self.subreddit = user_defaults.stringForKey_(Preferences.subreddit_key)
        self.ordering = user_defaults.stringForKey_(Preferences.ordering_key)
        self.update_interval = user_defaults.integerForKey_(Preferences.update_interval_key)
        self.limit = user_defaults.stringForKey_(Preferences.limit_key)

    def setSubreddit(self, subreddit):
        user_defaults = NSUserDefaults.standardUserDefaults()
        user_defaults.setObject_forKey_(subreddit, Preferences.subreddit_key)
        self.subreddit = subreddit

    def setOrdering(self, ordering):
        user_defaults = NSUserDefaults.standardUserDefaults()
        user_defaults.setObject_forKey_(ordering, Preferences.ordering_key)
        self.ordering = ordering

    def setUpdateInterval(self, update_interval):
        user_defaults = NSUserDefaults.standardUserDefaults()
        user_defaults.setInteger_forKey_(update_interval, Preferences.update_interval_key)
        self.update_interval = update_interval

    def setLimit(self, limit):
        user_defaults = NSUserDefaults.standardUserDefaults()
        user_defaults.setObject_forKey_(limit, Preferences.limit_key)
        self.limit = limit

    @staticmethod
    def setDefaults():
        """
            Sets the default preferences for this application
        """
        user_defaults = NSUserDefaults.standardUserDefaults()
        pref_dict = {
            Preferences.ordering_key: Preferences.ordering_default,
            Preferences.update_interval_key: Preferences.update_interval_default,
            Preferences.subreddit_key: Preferences.subreddit_default,
            Preferences.limit_key: Preferences.limit_default

        }
        nspref_dict = NSDictionary.dictionaryWithDictionary_(pref_dict)
        user_defaults.registerDefaults_(nspref_dict)
