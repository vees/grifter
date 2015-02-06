class ImportRecursiveCount:
    def __init__(self, success, ignored, failure):
        print "Created IRC"
        self._import_success = success
        self._import_ignored = ignored
        self._import_failure = failure
        pass

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return "Stats: %s %s %s" % (
            self._import_success, self._import_ignored, self._import_failure)

    def add(self, count_to_add):
        if isinstance(count_to_add, ImportRecursiveCount):
            self._import_success += count_to_add._import_success
            self._import_ignored += count_to_add._import_ignored
            self._import_failure += count_to_add._import_failure
        else:
            print "Failed to add object"
            pass

    def add_success(self):
        self._import_success += 1

    def add_ignored(self):
        self._import_ignored += 1
        #print self.__str__()

    def add_failure(self):
        self._import_failure += 1
