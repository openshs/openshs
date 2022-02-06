import random
from collections import OrderedDict, Counter
from indexed import IndexedOrderedDict
from itertools import islice
import csv
from math import ceil
import os

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))
def pick_by_prob(d):
    r = random.uniform(0, sum(d.values()))
    s = 0.0
    for k, w in d.items():
        s += w
        if r < s: return k
    return k

def convert_row_to_key(row):
    return ''.join(row)

def convert_key_to_row(key):
    return [x for x in key]

def strip_idx_from_key(key):
    return key[key.find('_') + 1:]

def strip_sample_and_idx_from_key(key):
    return key[key.find('_', key.find('_') + 1) + 1:]

def strip_sample_from_key(key):
    return key[key.find('_') + 1:]

def find_longest_index(samples):
    """Returns the index of the longest item in an OrderedDict."""
    if type(samples) is OrderedDict and len(samples) > 0:
        longest_idx = 1
        longest_len = 1
        for s in samples:
            if len(samples[s]) > longest_len:
                longest_len = len(samples[s])
                longest_idx = s
        return longest_idx
    else:
        raise TypeError("Please pass in an OrderedDict containing at least a single element.")

def find_longest_activities(samples):
    if len(samples) > 0:
        longest = -1
        for sample in samples:
            if len(samples[sample]) > longest:
                longest = len(samples[sample])
        return longest
    else:
        raise TypeError("Please pass in at least a single element.")

def find_shortest_activities(samples):
    if len(samples) > 0:
        shortest = 999
        for sample in samples:
            if len(samples[sample]) < shortest:
                shortest = len(samples[sample])
        return shortest
    else:
        raise TypeError("Please pass in at least a single element.")

def find_activities_length(samples):
    if len(samples) > 0:
        lens = [len(samples[sample]) for sample in samples]
        return lens
    else:
        raise TypeError("Please pass in at least a single element.")

def activity_counter(samples, time_step):
    """Returns a dictionary where the keys are the activities labels and the values
are the number of the activities occurrence at the spceified time_step.
    samples: OrderedDict,
    time_step: index, starting from 1 and not bigger than the longest activity in samples"""
    if (type(samples) is OrderedDict) and \
       (time_step > 0) and \
       (time_step <= len(samples[find_longest_index(samples)])):
        activities = []
        for s in samples:
            try:
                activities.append(samples[s][time_step-1])
            except IndexError:
                pass
        return Counter(activities)
    else:
        raise TypeError("Please pass in an OrderedDict and a time_step bigger than zero and less than the longest activity in the samples.")

def unique_pattern_counter(reading):
    """Returns an IndexedOrderedDict of unique sub-patterns in a reading"""
    counter = IndexedOrderedDict()
    idx = 0
    for row in reading:
        if counter.get(str(idx) + '_' + convert_row_to_key(row)):
            counter[str(idx) + '_' + convert_row_to_key(row)] += 1
        else:
            idx += 1
            counter[str(idx) + '_' + convert_row_to_key(row)] = 1
    return counter

def readings_counter(readings, time_step):
    readings_count = []
    for reading in readings:
        try:
            readings_count.append(reading.items()[time_step - 1])
        except IndexError:
            pass
    return Counter(readings_count)

def extract_labels(dataset):
    li = []
    for row in dataset:
        li.append(row[-1])
    return li

def strip_labels_column(dataset):
    return [row[:-1] for row in dataset]

def readings_idxdict(indexed_labels, dataset):
    readings_dict = IndexedOrderedDict()
    stripped_dataset = strip_labels_column(dataset)
    for k in indexed_labels:
        readings_dict[k] = take(indexed_labels[k], stripped_dataset)
    return readings_dict

def randomize_reading_len(readings):
    idxs = find_longest_sub_pattern_idx(readings)

    max_len  = idxs[1] - idxs[0]
    min_len  = int(ceil(0.05 * max_len))
    rand_len = random.randint(min_len, max_len)

    start = idxs[0] + min_len
    end   = idxs[0] + rand_len

    return readings[:start] + readings[end:]

def find_longest_sub_pattern_idx(readings):
    start_idx = 0
    longest = 0
    subpats = []
    for i, row in enumerate(readings):
        if readings[start_idx] == row:
            longest += 1
        else:
            subpats.append((start_idx, longest))
            start_idx = longest
            longest += 1
    subpats.append((start_idx, longest))

    ll = 1
    longest = 0
    for i, idx in enumerate(subpats):
        if (idx[1] - idx[0]) > ll:
            ll = idx[1] - idx[0]
            longest = i

    return subpats[longest]

def test2():
    samples = [
               ['0', '1', '1'],
               ['0', '1', '1'],
               ['1', '0', '1'],
               ['1', '0', '1'],
               ['1', '0', '1'],
              ]
    print(find_longest_sub_pattern_idx(samples))

def test():
    activities_samples = OrderedDict()
    activities_samples[1] = ['sleep', 'eat',      'sleep']
    activities_samples[2] = ['sleep', 'personal', 'eat'  ]
    activities_samples[3] = ['sleep', 'eat']
    activities_samples[4] = ['sleep', 'eat']

    readings_samples = [
        [ # 1
            ['0', '1', '1'],
            ['0', '1', '1'],
            ['0', '1', '1'],
            ['0', '1', '1'],
            ['1', '0', '1'],
            ['1', '0', '1'],
            ['1', '0', '1'],
            ['1', '0', '1'],
            ['1', '0', '1']
        ],
        [ # 2
            ['0', '1', '1'],
            ['0', '1', '1'],
            ['0', '1', '1'],
            ['0', '1', '1'],
            ['0', '0', '1'],
            ['0', '0', '1'],
            ['0', '0', '1'],
            ['0', '0', '1'],
            ['0', '0', '1']
        ],
        [ # 3
            ['0', '1', '1'],
            ['0', '1', '1'],
            ['0', '1', '1'],
            ['0', '1', '1'],
            ['0', '1', '1'],
            ['0', '1', '1'],
            ['0', '1', '1'],
            ['0', '1', '1'],
            ['0', '1', '1']
        ],
        [ # 4
            ['0', '1', '1'],
            ['0', '1', '1'],
            ['0', '1', '1'],
            ['0', '0', '1'],
            ['0', '0', '1'],
            ['0', '0', '1'],
            ['0', '1', '1'],
            ['0', '1', '1'],
            ['0', '1', '1']
        ],
        [ # 5
            ['1', '1', '1'],
            ['1', '1', '1'],
            ['1', '1', '1'],
            ['1', '0', '1'],
            ['1', '0', '1'],
            ['1', '0', '1'],
            ['1', '1', '1'],
            ['1', '1', '1'],
            ['1', '1', '1']
        ]
    ]

    readings_list = []
    for reading in readings_samples:
        readings_list.append(unique_pattern_counter(reading))

    k = activity_counter(activities_samples, 3)
    print('-------------------------- Generating activities for time t')

    for _ in range(10):
        print(pick_by_prob(k))
    print('-------------------------- Patterns in readings')

    for r in readings_list:
        print(list(r))

    print('-------------------------- Generating readings for time t')
    k = readings_counter(readings_list, 1)
    for _ in range(10):
        print(pick_by_prob(k))

def main():
    from samplespool import SamplesPool
    for i in range(10):
        pool = SamplesPool([
                os.path.join('samples','sample1.csv'), \
                os.path.join('samples','sample2.csv'), \
                os.path.join('samples','sample3.csv'), \
                os.path.join('samples','sample4.csv'), \
                os.path.join('samples','sample5.csv')
            ])

    #for _ in range(10):
    #    pool.generate_sample()

        writer = csv.writer(open('out' + str(i) + '.csv', 'w'))
        new_dataset = pool.generate_sample()
        writer.writerows(new_dataset)


if __name__ == '__main__':
    main()
    #test2()
