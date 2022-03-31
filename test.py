import json
import csv


def unwesternize(exp):
    return str(exp).split('(').pop()[:-1]


def data_to_tsv(clean_data,sort=True):
    with open("res.tsv", 'wt') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        keys = list(clean_data[0].keys())
        writer.writerow(keys)

        if sort:
            clean_data.sort(key=lambda x:x["name"])

        for e in clean_data:
            row = []
            for key in keys:
                row.append(e[key])
            writer.writerow(row)


with open("pokedex.json", "r") as jsonfile:
    data = json.load(jsonfile)
    max = 6
    clean_data = []

    for e in data:
        row = {}
        for key in e.keys():
            if type(e[key]) == list:
                for i in range(0, max):
                    val = ""
                    if i < len(e[key]) - 1:
                        val = e[key][i]
                    row[f'{key}.{i}'] = val
            elif type(e[key]) == dict:
                obj = e[key]
                for subkey in obj.keys():
                    row[f'{key}.{subkey}'] = obj[subkey]
            else:
                val = e[key]
                if key == "weight" or key == "height":
                    val = unwesternize(e[key])
                row[key] = val
        clean_data.append(dict(sorted(row.items())))

data_to_tsv(clean_data)

