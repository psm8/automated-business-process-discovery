from processdiscovery.event.base_group import BaseGroup
import zlib


class EventGroup(BaseGroup):
    def __init__(self, events=None):
        super().__init__(events)

    def __hash__(self):
        return zlib.adler32(self.get_event_names_hash())

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.compare(other)

    def get_event_names_hash(self):
        result = b'0'
        for x in self.events:
            if isinstance(x, BaseGroup):
                result += bytes(x.get_event_names_hash())
            else:
                result += x.name.encode('utf-8')

        return result

    def compare(self, other):
        if not isinstance(other, type(self)):
            return False
        if len(self.events) != len(other.events):
            return False
        for i in range(len(self.events)):
            if not self.events[i].compare(other.events[i]):
                return False
        return True
