from collections import defaultdict

def get_candidate_lists(datapoints):
    result = defaultdict(lambda: [])

    for dp in datapoints:
        result[dp.candidate].append(dp)

    return result

def create_candidate_var(datapoints):
    var_name = '_'.join(datapoints[0].candidate.lower().split(' ')) + "_data"
    data = []    

    for dp in datapoints:
        data.append(dp.value)

    return var_name +  " = " + str(data) + ";\n"

def create_xlabels_var(datapoints):
    labels = []

    for dp in datapoints:
        labels.append(dp.xlabel)

    return "xlabels = " + str(labels) + ";\n"

def build_js(datapoints):
    js = ""
    data_by_candidate = get_candidate_lists(datapoints)
    xlabels_js = None
    
    for candidate, data in data_by_candidate.items():
        data.sort(key=lambda x: x.get_date_int())
        js += create_candidate_var(data)

        if not xlabels_js:
            xlabels_js = create_xlabels_var(data)

    js += xlabels_js

    return js
