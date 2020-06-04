import sys
from collections import defaultdict

def calculate_percentages(results):
    percentages = defaultdict(lambda: 0)

    # Accumulate the number of results of a particular type
    for result in results:
        percentages[result] += 1

    for classifier, value in percentages.items():
        percentages[classifier] = float(value) / float(len(results))

    return percentages

def print_percentages(p):
    for label, percentage in p.items():
        label = label.strip('\n')
        print("%s: %s" % (label, percentage))

def main():
    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " results-file")
        exit()

    results = []

    with open(sys.argv[1], 'rt') as f:
        for line in f:
            results.append(line)

    p = calculate_percentages(results)
    print_percentages(p)

if __name__ == '__main__':
    main()