# iptree.py
#
# A fast data structure based on BTrees.OIBTree for storing
# large sets of IP addresses and/or subnets, with fast lookup
# capabilities.
#
# (c) 2013 Jasper Spaans <j@jasper.es>

from BTrees.OIBTree import OIBTree

class IPTree(object):
    """Data structure for storing sets of IP addresses"""
    def __init__(self, l=None):
        self._tree = OIBTree()
        self._tree[[-1,255,255,255]] = 0
        self._tree[[256,0,0,1]] = 0

    def add(self, s):
        ip4 = IP4(s)
        t = self._tree
        #print "adding %r" % ip4
        inbetween = list(t.items(min=ip4.begin, max=ip4.end,
                                 excludemin=True,
                                 excludemax=True))

        ma = t.minKey(ip4.end)   # returns smallest key >= ip4.end
        mi = t.maxKey(ip4.begin) # returns largest key <= ip4.begin

        if ma == ip4.end:
            if t[ma] == 1:
                del t[ma]
        else:
            if not ip4.end in self:
                t[ip4.end] = 0

        if mi == ip4.begin:
            if t[mi] == 0:
                del t[mi]
        else:
            if not ip4.begin in self:
                t[ip4.begin] = 1

        for node, val in inbetween:
            del self._tree[node]

    def remove(self, s):
        ip4 = IP4(s)
        t = self._tree
        #print "removing %r" % ip4
        inbetween = list(t.items(min=ip4.begin, max=ip4.end,
                                 excludemin=True,
                                 excludemax=True))

        ma = t.minKey(ip4.end)   # returns smallest key >= ip4.end
        mi = t.maxKey(ip4.begin) # returns largest key <= ip4.begin

        if ma == ip4.end:
            if t[ma] == 0:
                del t[ma]
        else:
            if ip4.end in self:
                t[ip4.end] = 1

        if mi == ip4.begin:
            if t[mi] == 1:
                del t[mi]
        else:
            if ip4.begin in self:
                t[ip4.begin] = 0

        for node, val in inbetween:
            del self._tree[node]

    def as_iter(self):
        i = iter(self._tree)
        i.next() # discard first item
        while True:
            p0 = i.next()
            p1 = i.next()
            yield (p0, p1)

    def __contains__(self, a):
        if isinstance(a, list):
            k = self._tree.maxKey(a)
            return self._tree[k]
        raise RuntimeError("Should not happen!")

    def __repr__(self):
        return repr(list(self.as_iter()))

class IP4(object):
    """Data structure for storing a IP address with a mask"""

    def __init__(self, s):
        addr, _, mask = s.partition("/")
        if not mask:
            mask = 32
        else:
            mask = int(mask)
        assert 0 <= mask <= 32

        octets = addr.split('.')
        assert len(octets) == 4
        octets = map(int, octets)
        assert 0 <= min(octets)
        assert max(octets) < 256

        # check that the last (32 - mask) bits are zero
        o = octets[:]
        for b in range(mask, 32):
            bit = (o[b/8] >> (7 - (b%8))) & 1
            if bit:
                raise RuntimeError("Invalid ip/netmask combination: %s" % s)

        self.mask = mask
        self.octets = octets

    @property
    def begin(self):
        return self.octets[:]

    @property
    def end(self):
        """Returns the IP address one beyond the current netmask;
        infinity is 256.0.0.0
        """
        if self.mask == 32:
            change_octet = 3
            change_by = 1
        else:
            change_octet = self.mask / 8
            change_by = 256 >> (self.mask % 8)
        octets = self.octets[:]
        octets[change_octet] += change_by
        while change_octet and octets[change_octet]==256:
            octets[change_octet] = 0
            change_octet -= 1
            octets[change_octet] += 1
        return octets

    def __repr__(self):
        return "%s/%d" % (".".join(str(o) for o in self.octets), self.mask)

if __name__ == '__main__':
    print "Constructing new tree!"
    t = IPTree()
    print t
    t.add("10.0.0.0/8")
    print t
    t.add("11.0.0.0/8")
    print t
    t.add("11.0.0.4/31")
    print t
    t.add("11.0.0.0/8")
    print t
    t.add("12.0.0.4/31")
    print t
    t.add("12.0.0.0/30")
    print t
    t.remove("11.0.0.4/31")
    print t
    t.remove("11.0.0.0/29")
    print t
    t.remove("11.0.0.0/8")
    print t
    t.remove("0.0.0.0/0")
    print t
    t.remove("0.0.0.0/0")
    print t
    t.add("130.161.191.190")
    print t
    t.add("130.161.191.191")
    print t
    t.add("0.0.0.0/0")
    print t
