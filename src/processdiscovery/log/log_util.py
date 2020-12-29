import csv


def get_event_log_csv(filename) -> dict:
    with open("../datasets/" + filename, newline='') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        events = {}
        for row in data:
            count = row.pop(0)
            events[tuple(row)] = int(count)
    return events


def get_event_log() -> dict:
    return {("a", "b", "c", "d", "e", "f"): 1, ("a", "c", "b", "d", "e", "f"): 1}


def get_log_unique_events(keys):
    unique_events = set()
    [unique_events.add(x) for key in keys for x in key]
    return unique_events


def get_sum_of_processes_length(log: dict) -> int:
    return sum(len(key) * log[key] for key in log.keys())


class LogInfo:

    def __init__(self, filename):
        self.log = get_event_log_csv(filename)
        self.log_unique_events = get_log_unique_events(self.log.keys())
        self.sum_of_processes_length = get_sum_of_processes_length(self.log)
        self.process_average_length = self.sum_of_processes_length / sum([x for x in self.log.values()])
