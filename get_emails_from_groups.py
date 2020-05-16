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

import sys, getopt, requests


# Returns a dict of <user name>,<email address> for the given group
def get_emails_from_group(url, un, pw, group):
    headers = {'Accept': 'application/json'}
    table_url = 'https://dev57241.service-now.com/api/now/table/sys_user_group?sysparm_query=GOTOname%25253DApplication%252520Development&sysparm_fields=name&sysparm_limit=1'
    response = requests.get(table_url, auth=(un, pw), headers=headers)
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.content)
        exit()

    return response.content


def main(argv):
    all_groups = ''  # Input file containing the groups for which you want the emails for
    emails_csv = ''  # Output file to put the email list
    snow_url = ''  # Which snow instance to use (eg. www.<url_prefix>.service-now.com)
    user_id = ''  # Username for the account used by this program
    password = ''  # Password for the given username
    try:  # handle input args
        opts, args = getopt.getopt(argv, 'he:i:o:n:p', ['url_prefix=', 'groups=', 'emailcsv=', 'userid=', 'password='])
    except getopt.GetoptError:
        print('get_emails_from_groups.py -e <dev|test|prod> -i <groups_file> -0 <email_csv_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('get_emails_from_groups.py -e <environment aka url_prefix> -i <group_csv_file> -0 <email_csv_file>')
            sys.exit()
        elif opt in ('-e', '--url_prefix'):
            # TODO: Validate URL prefix input
            snow_url = 'https://' + arg + '.service-now.com/api/now/'
        elif opt in ('-i', '--groupcsv'):
            all_groups = arg
        elif opt in ('-o', '--emailcsv'):
            emails_csv = arg
        elif opt in ('-n', '--userid'):
            user_id = arg
        elif opt in ('-p', '--password'):
            password = arg

    # Read in groups from the input file (expects newline separated groups)
    groups_file = open(all_groups)
    groups = groups_file.read().splitlines()
    for group in groups:
        print(get_emails_from_group(snow_url, user_id, password, group))


if __name__ == "__main__":
    main(sys.argv[1:])
