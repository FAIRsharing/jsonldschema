import json
import os
from semDiff.fullDiff import FullDiffGenerator
import multiprocessing


output_base_path = os.path.join(os.path.dirname(__file__), "../fullDiffOutput/")


def make_diff(network1, network2):
    print("-----------------------------")
    print("Comparing %s VS %s, please wait" % (network1["name"], network2["name"]))
    overlaps = FullDiffGenerator(network1, network2)
    print("Result:", json.dumps(overlaps.json))

    filename = network1["name"] + "_VS_" + network2["name"] + ".json"

    with open(os.path.join(output_base_path, filename), "w") as outputFile:
        outputFile.write(json.dumps(overlaps.json, indent=4))
        outputFile.close()


if __name__ == '__main__':

    MIACME_schema_url = "https://w3id.org/mircat/miacme/schema/miacme_schema.json"
    MIACA_schema_url = "https://w3id.org/mircat/miaca/schema/miaca_schema.json"
    MyFlowCyt_schema_url = "https://w3id.org/mircat/miflowcyt/schema/miflowcyt_schema.json"
    MIACA_MIACME_merge_schema_url = \
        "https://w3id.org/mircat/miaca_miacme_merge/schema/miaca_miacme_merged_schema.json"
    MIACA_MIFLOWCYT_merge_schema_url = \
        "https://w3id.org/mircat/miaca_miflowcyt_merge/schema/miaca_miflowcyt_merged_schema.json"
    MIACME_MIACA_merge_schem_url = \
        "https://w3id.org/mircat/miacme_miaca_merge/schema/miacme_miaca_merged_schema.json"
    MIACME_MIFLOWCYT_merge_schem_url = \
        "https://w3id.org/mircat/miaca_miflowcyt_merge/schema/miacme_miflowcyt_merged_schema.json"
    MIFLOWCYT_MIACA_merge_schem_url = \
        "https://w3id.org/mircat/miflowcyt_miaca_merge/schema/miflowcyt_miaca_merged_schema.json"
    MIFLOWCYT_MIACME_merge_schem_url = \
        "https://w3id.org/mircat/miflowcyt_miacme_merge/schema/miflowcyt_miacme_merged_schema.json"

    regex = {
        "/schema": "/context/obo",
        "_schema.json": "_obo_context.jsonld"
    }

    # REGEX 2 is for merged networks
    regex2 = {
        "/schema": "/context/",
        "_schema.json": "_context.jsonld"
    }

    MIACME_network = {
        "name": "MIACME",
        "regex": regex,
        "url": MIACME_schema_url
    }
    MIACA_network = {
        "name": "MIACA",
        "regex": regex,
        "url": MIACA_schema_url
    }
    MyFlowCyt_network = {
        "name": "MIFlowCyt",
        "regex": regex,
        "url": MyFlowCyt_schema_url
    }
    MIACA_MIACME_merge_network = {
        "name": "MIACA_MIACME_merge",
        "regex": regex2,
        "url": MIACA_MIACME_merge_schema_url
    }
    MIACA_MIFLOWCYT_merge_network = {
        "name": "MIACA_MIFLOWCYT_merge",
        "regex": regex2,
        "url": MIACA_MIFLOWCYT_merge_schema_url
    }
    MIACA_MIFLOWCYT_merge_network = {
        "name": "MIACA_MIFLOWCYT_merge",
        "regex": regex2,
        "url": MIACA_MIFLOWCYT_merge_schema_url
    }
    MIACME_MIACA_merge_network = {
        "name": "MIACME_MIACA_merge",
        "regex": regex2,
        "url": MIACME_MIACA_merge_schem_url
    }

    processes = [
        (MIACA_network, MIACME_network),
        (MIACA_network, MyFlowCyt_network),
        (MIACA_network, MIACA_network),

        (MIACME_network, MIACME_network),
        (MIACME_network, MyFlowCyt_network),
        (MIACME_network, MIACA_network),

        (MyFlowCyt_network, MIACME_network),
        (MyFlowCyt_network, MyFlowCyt_network),
        (MyFlowCyt_network, MIACA_network)
    ]

    cpu_count = multiprocessing.cpu_count()
    p = multiprocessing.Pool(processes=cpu_count)
    result = [p.apply_async(make_diff, args=(x, y)) for (x, y) in processes]

    output = [pp.get() for pp in result]

    make_diff(MIACA_MIACME_merge_network, MIACA_network)
    make_diff(MIACA_network, MIACA_MIACME_merge_network)
    make_diff(MIACA_network, MIACA_MIFLOWCYT_merge_network)
