class Collector(dict):
    """Acts like a dict with one key difference:  Duplicate keys are appended together into a list.  First time a key is added, it is stored as usual.  When that key is stored again, the existing valu ei sconverted to a listt and the new value is appended.
    """
    def __setitem__(self, k, v):
        _getitem = super(Collector, self).__getitem__
        _setitem = super(Collector, self).__setitem__

        if k in self:
            i = _getitem(k)
            if type(i) == list:
                i.append(v)
            else:
                _setitem(k, [i, v])
        else:
            _setitem(k, v)


    def replace(k, v):
        """Replaces key with value
        This is a wrapper around the original dict __setitem__ behavior.
        """
        super(Collector, self).__setitem__(k, v)


