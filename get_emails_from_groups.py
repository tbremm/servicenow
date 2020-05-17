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


def get_emails_from_groups(url, un, pw, groups):
    # Get all the users from the given set of groups
    user_data = []
    for group in groups:
        user_data.append(get_users_from_group(url, un, pw, group))
    flat_user_list = []
    for group_users in user_data:  # Put all users into one non-nested list
        flat_user_list += group_users
    return get_emails_from_users(url, un, pw, flat_user_list)


# Returns a list of user display names for the given group
def get_users_from_group(url, un, pw, group):
    headers = {'Accept': 'application/json'}
    query_url = url + 'table/sys_user_grmember?sysparm_query=group.name=' + group + \
        '&sysparm_display_value=all&sysparm_fields=user'
    response = requests.get(query_url, auth=(un, pw), headers=headers)
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.content)
        exit(2)
    data = json.loads(response.content)
    users = []
    for result in data['result']:
        users.append(result['user']['display_value'])
    return users


# Provide a list of user display names and this will return a list of their email addresses
def get_emails_from_users(url, un, pw, users):
    headers = {'Accept': 'application/json'}
    emails = []
    user_set = set(users)  # Remove duplicates to save on number of requests
    for user in user_set:
        query_url = url + 'table/sys_user?sysparm_query=name=' + user + \
            '&sysparm_display_value=all&sysparm_fields=email'
        response = requests.get(query_url, auth=(un, pw), headers=headers)
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.content)
            exit(3)
        data = json.loads(response.content)
        emails.append(data['result'][0]['email']['display_value'])
    return emails


def main(argv):
    group_in_file = ''  # Input file containing the groups from which you want to harvest emails
    emails = ''  # Output file where the email list (\n separated) gets output
    snow_url = ''  # Which snow instance to use (eg. for www.<url_prefix>.service-now.com, this should be <url_prefix>)
    user_id = ''  # Username for the account used by this program
    password = ''  # Password for the given username

    # Handle input args
    try:
        opts, args = getopt.getopt(argv, 'hu:i:o:n:p:', ['url_prefix=', 'groups=', 'emails=', 'userid=', 'password='])
    except getopt.GetoptError:
        print('get_emails_from_groups.py -e <url_prefix> -i <input_groups_file> -0 <output_emails_file>')
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print('get_emails_from_groups.py -e <environment aka url_prefix> -i <group_csv_file> -0 <email_csv_file>')
            sys.exit(0)
        elif opt in ('-u', '--url_prefix'):
            snow_url = 'https://' + arg + '.service-now.com/api/now/'
        elif opt in ('-i', '--groups'):
            group_in_file = arg
        elif opt in ('-o', '--emails'):
            emails = arg
        elif opt in ('-n', '--userid'):
            user_id = arg
        elif opt in ('-p', '--password'):
            password = arg

    # Read in groups from the input file (expects newline separated groups)
    groups_file = open(group_in_file)
    in_groups = set(groups_file.read().splitlines())  # Use a set to eliminate duplicates
    groups_file.close()

    # Get all the emails from the given list of snow groups
    email_list = get_emails_from_groups(snow_url, user_id, password, in_groups)

    # Write the emails (newline separated) to the output file
    with open(emails, 'w') as out_file:
        out_file.write('\n'.join(email_list))
    out_file.close()
    print('Script complete. See ' + emails + ' for the list of emails.')
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
