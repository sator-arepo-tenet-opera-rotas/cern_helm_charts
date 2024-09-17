import argparse, sys, os
import json,yaml
import re
from pprint import pprint as pp

re_search = '(rate|changes|delta|deriv|holt_winters|idelta|increase|irate|predict_linear|rate|resets)(\(.*\[)(\d+[smhdwy])(\].*)'
re_replace = 'i(delta|rate)\('
re_aggregation = '(avg|min|max|sum|count|quantile|stddev|stdvar)\('

# Do not generate rules for rule names that contain rules_skip_list
rules_skip_list = [
    'apiserver',
    'kube-scheduler',
]
rules_skip_list = []

def convert_prometheus_rule_to_aggregated(prom_rule_spec):
    """Searches the PrometheusRules specs and transforms the metric rules into
        aggregated rules. Some operations that are done:
        - Alarmistic rules are discarded and not considered for aggregation.
        - Add interval to each rule_group (defines the execution frequency)
        - Add aggregate label to all metrics
        - Replace the metrics window

    Args:
        prom_rule_spec (dict): The spec dictionary.

    Returns:
        dict: The aggregated spec dictionary.
    """
    # The following parsing syntax can be checked here:
    # URL: https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/
    for group in range(len(prom_rule_spec['groups'])):
        rule_group = prom_rule_spec['groups'][group]
        # Add or overwrite the interval for the downsampled data
        rule_group['interval'] = "{{.Values.evaluationInterval}}"
        # Set different name
        rule_group['name'] = "cern." + rule_group['name'].replace('.rules','.aggregated-rules')
        # Get all the rules
        rules = rule_group['rules']
        # From the rules array, delete all rules concerning alerts
        # The end result we will have only metric evaluation rules
        rules = list(filter(lambda r: 'alert' not in r.keys(), rules))
        # Go through each rule and alter it in conformance of what we want
        for rule in range(len(rules)):
            # Create or append rate label to rule
            # TODO: CHECK MULTI LABELS
            if "labels" not in rules[rule]:
                rules[rule]["labels"] = {}
            rules[rule]["labels"]["aggregate"] = "{{.Values.evaluationInterval}}" # defined on helm chart
            # This might not be needed if we can use the label "rate" as the identifier and the metric name can coexist with the other file
            rules[rule]['record'] = "cern:" + rules[rule]['record']
            # Replace the matched interval for our defined sample interval
            rules[rule]['expr'] = re.sub(re_search, "\\1\\2" + "\\4", rules[rule]['expr']).replace("[]", "[{{.Values.metricWindow}}]") #defined on helm chart
            # Replace all resolution data for implicit averaging function
            rules[rule]['expr'] = re.sub(re_replace, "\\1(", rules[rule]['expr'])
            # # Replace all <aggregation> data for <aggregation>_over_time functions
            # rules[rule]['expr'] = re.sub(re_aggregation, "\\1_over_time(", rules[rule]['expr'])

        if rule_group['rules']:
            # Save modifications
            rule_group['rules'] = rules
        else:
            rule_group = None

    # Before returning, drop the enpty groups
    new_rule_spec = list(filter(lambda r: 0 != len(r['rules']), prom_rule_spec['groups']))
    pp (new_rule_spec)

    # Return aggregated Spec
    return {'groups': new_rule_spec}

def aggregated_rules_builder(prom_rules):
    """Performs all logic to gather, parse, build and create aggregated
        rules from the existent rules.

    Args:
        prom_rules (str): Comma separated PrometheusRules names.

    Returns:
        bool: True if success. False otherwise.
    """
    # Generate Rules for each of the
    for prom_rule in prom_rules:
        # We dont need to generate our own rules.
        if 'cern' in prom_rule or len(prom_rule) == 0:
            print ("SKIPPING PrometheusRule - " + prom_rule)
            continue

        # Do not generate rules specified by us.
        if any(skip_name in prom_rule for skip_name in rules_skip_list):
            print ("SKIPPING PrometheusRule due to skip name list - " + prom_rule)
            continue

        # Get the K8s manifest for the rule under evaluation
        data = os.popen(str.join(' ',
            ['kubectl',
            '-n', 'kube-system',
            '-o', 'json',
            'get', 'PrometheusRule', prom_rule,
            ])).read()

        # Load Json
        json_data = json.loads(data)

        # Strip K8s stuff
        prom_rule_spec = unwrap_from_k8s_manifest(json_data)

        # Convert the rules into aggregated rules
        new_rule_spec = convert_prometheus_rule_to_aggregated(prom_rule_spec)

        # New rules are enpty, nothing to record
        if len(new_rule_spec['groups']) == 0:
            continue

        # Wrap rule with K8s PrometheusRule manifest
        new_rule_file_name = "cern." + prom_rule + ".yaml"
        # print typenew_rule_spec)
        aggregated_prometheus_rule = wrap_into_k8s_manifest(new_rule_file_name, new_rule_spec)

        # Save the generated rules file
        new_rule_file_path = "../templates/generated/" + new_rule_file_name
        f = open(new_rule_file_path, "w")
        f.write(yaml.safe_dump(aggregated_prometheus_rule))
        f.close()

    return True

def wrap_into_k8s_manifest(file_name, data):
    """Appends the necessary k8s object definitions for the PrometheusRule type.

    Args:
        file_name (str): the name of the file .
        data (dict): The spec dictionary.

    Returns:
        dict: Returns the spec dictionary of the k8s manifest.
    """
    aggregated_prometheus_rule = {
        'apiVersion': 'monitoring.coreos.com/v1',
        'kind': 'PrometheusRule',
        'metadata': {
            'labels': {
                'app': 'prometheus',
                'release': 'prometheus-operator',
            },
            'name': file_name.replace('.rules.','.aggregated-rules.'),
            'namespace': 'kube-system',
        },
        'spec': data
    }

    return aggregated_prometheus_rule


def unwrap_from_k8s_manifest(json_data):
    """Strips away the k8s specific objects and retrieves only relevant data.

    Args:
        json_data (str): the name of the file .

    Returns:
        dict: Returns the spec dictionary.
    """
    return json_data['spec']

if __name__ == "__main__":
    """Parse input arguments and call the relevant functions. """

    parser = argparse.ArgumentParser()

    parser.add_argument('--rules', help='A string with all the available, space separated, PrometheusRules.')

    args=parser.parse_args()

    # Split PrometheusRules.
    aggregated_rules_builder(args.rules.split(','))
