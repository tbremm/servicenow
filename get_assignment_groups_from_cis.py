#!/usr/bin/env python

# Copyright 2020 Timothy Bremm <timothy.bremm@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import getopt
import requests
import json


def get_ag_from_ci(url, un, pw, ci):
    headers = {'Accept': 'application/json'}
    query_url = url + 'table/cmdb_ci?sysparm_query=nameLIKE' + ci + \
        '&sysparm_display_value=true&sysparm_fields=assignment_group&sysparm_limit=1'
    response = requests.get(query_url, auth=(un, pw), headers=headers)
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.content)
        exit(2)
    data = json.loads(response.content)
    if data['result'][0]['assignment_group'] != '':
        return ci, data['result'][0]['assignment_group']['display_value']
    return ci, 'unknown'


def get_ags_from_cis(url, un, pw, cis):
    ags = [''] * len(cis)
    cis_set = set(cis)
    for i, ci in enumerate(cis_set):
        ags[i] = get_ag_from_ci(url, un, pw, ci)
    return ags


def print_help_message():
    print('Usage:')
    print('python get_assignment_groups_from_cis.py -u <url_prefix> -i <input_cis_file> -o <output_groups_file> '
          '-n <username> -p <password>')
    print()
    print('-u, --url_prefix: the first part of the url, eg. https://<url_prefix>.service-now.com')
    print('-i, --cis: The path (relative or absolute) to the input file containing the CIs')
    print('\tInput file should be a newline-separated list of Configuration Items (CIs)')
    print('-o, --groups: The path (relative or absolute) to the output file containing the resulting assignment groups')
    print('\tThis will be a comma-separated list of CIs and assignment groups (creates or overwrites)')
    print('-n, --userid: The username of the account that this will be running as (must have appropriate api and '
          'table permissions)')
    print('-p, --password: The password for the given username')
    print('-h: Prints this help message')
    return


def main(argv):
    ci_in_file = ''  # Input file containing the groups from which you want to harvest assignment groups
    group_out_file = ''  # Output file where the CI/AG list (comma separated) gets output
    snow_url = ''  # Which snow instance to use (eg. for www.<url_prefix>.service-now.com, this should be <url_prefix>)
    user_id = ''  # Username for the account used by this program
    password = ''  # Password for the given username

    # Handle input args
    try:
        opts, args = getopt.getopt(argv, 'h:u:i:o:n:p:', ['url_prefix=', 'cis=', 'groups=', 'userid=', 'password='])
    except getopt.GetoptError:
        print_help_message()
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print_help_message()
            sys.exit(0)
        elif opt in ('-u', '--url_prefix'):
            snow_url = 'https://' + arg + '.service-now.com/api/now/'
        elif opt in ('-i', '--cis'):
            ci_in_file = arg
        elif opt in ('-o', '--groups'):
            group_out_file = arg
        elif opt in ('-n', '--userid'):
            user_id = arg
        elif opt in ('-p', '--password'):
            password = arg

    # Read in groups from the input file (expects newline separated groups)
    groups_file = open(ci_in_file)
    in_cis = set(groups_file.read().splitlines())  # Use a set to eliminate duplicates
    groups_file.close()

    cis_ags = get_ags_from_cis(snow_url, user_id, password, in_cis)

    # Write the CIs and AGs (CSV format) to the output file
    with open(group_out_file, 'w') as out_file:
        out_file.write('CI, Assignment Group\n')
        for ci_ag in cis_ags:
            out_file.write(ci_ag[0] + ', ' + ci_ag[1] + '\n')
    out_file.close()
    print('Script complete. See ' + group_out_file + ' for the list of CIs and Assignment Groups.')
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
