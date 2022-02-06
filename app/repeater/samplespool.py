try: from repeater import take, unique_pattern_counter, extract_labels, pick_by_prob, find_activities_length, \
    strip_sample_and_idx_from_key, randomize_reading_len
except: pass
from collections import OrderedDict, Counter
import csv
from indexed import IndexedOrderedDict
import random

class SamplesPool(object):
    def __init__(self, datasets, variable_activities=False):
        self.samples = IndexedOrderedDict()
        self.samples_file_descriptors = []
        self.variable_activities = variable_activities
        for i, dataset in enumerate(datasets, start=1):
            self.samples_file_descriptors.append(open(dataset, 'r'))
            d = csv.reader(self.samples_file_descriptors[i - 1])
            self.header = next(d)
            self.samples['sample' + str(i)] = d

        self.extract_all_labels()
        self.reset_file_descriptors()
        self.attach_readings_to_labels()

    def attach_readings_to_labels(self):
        self.readings = dict()
        for i, label in enumerate(self.labels):
            reader = csv.reader(self.samples_file_descriptors[i])
            next(reader)
            # stripped_dataset = strip_labels_column(reader)
            for l in self.labels[label]:
                self.readings[ label + '_' + l ] = take(self.labels[label][l], reader)

    def reset_file_descriptors(self):
        for f in self.samples_file_descriptors:
            f.seek(0)

    def extract_all_labels(self):
        self.labels = OrderedDict()
        for sample in self.samples:
            self.labels[sample] = unique_pattern_counter(extract_labels(self.samples[sample]))

    def pick_labels_at(self, time_step, length):
        li = []
        for label in self.labels:
            if len(self.labels[label]) == length:
                try:
                    pick = self.labels[label].items()[time_step -1]
                    li.append(label + '_' + pick[0])
                except IndexError:
                    pass

        return pick_by_prob(Counter(li))

    def generate_sample(self, header=True):
        lens = find_activities_length(self.labels)

        new_dataset = []
        if header:
            new_dataset.append(self.header)

        picked_labels = []

        length = random.choice(lens)
        for i, time_step in enumerate(range(1, length + 1)):
            if time_step > 1:
                pick = self.pick_labels_at(time_step, length)

                # If we have duplicate picks, pick again
                tries = 0
                while((strip_sample_and_idx_from_key(pick) == strip_sample_and_idx_from_key(picked_labels[i -1])) and (tries <= 50)):
                    pick = self.pick_labels_at(time_step, length)
                    tries += 1
                picked_labels.append(pick)
            else:
                picked_labels.append(self.pick_labels_at(time_step, length))


        # Check if we have duplicate last activity
        if strip_sample_and_idx_from_key(picked_labels[-1]) == strip_sample_and_idx_from_key(picked_labels[-2]):
            picked_labels.pop()

        # Check for variable activities flag
        if self.variable_activities:
            for pick in picked_labels:
                new_dataset += randomize_reading_len(self.readings[pick])
        else:
            for pick in picked_labels:
                new_dataset += self.readings[pick]

        return new_dataset
