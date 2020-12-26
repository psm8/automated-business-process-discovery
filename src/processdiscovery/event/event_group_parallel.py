from processdiscovery.event.base_group import BaseGroup
import zlib


class EventGroupParallel(BaseGroup):

    def __init__(self, events=None):
        super().__init__(events)

    def __hash__(self):
        return zlib.adler32(self.get_event_names_hash())

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.compare(other)

    def get_event_names_hash(self):
        result = b'1'
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
        if isinstance(self, EventGroupParallel):
            for x in self.events:
                if not any([x.compare(y) for y in other.events]):
                    return False
        return True
