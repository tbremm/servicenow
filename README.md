# servicenow
Contains servicenow api helpers

# Usage
`python ./get_emails_from_groups.py -u <url_prefix> -i <input file> -o <output file> -n <username> -p <password>`
* -u, --url_prefix: the first part of the url, eg. https://<url_prefix>.service-now.com
* -i, --groups: The path (relative or absolute) to the input file containing the groups
    * Input file should be a newline-separated list of user groups
* -o, --emails: The path (relative or absolute) to the output file containing the resulting emails
    * This will be a newline-separated list of the email addresses of everyone in the given groups
* -n, --userid: The username of the account that this will be running as (must have appropriate api and table permissions)
* -p, --password: The password for the given username
* -h: Prints a usage help message

Note that this can take a bit of time because it makes a separate API call for each group and for each user


# TODO
* Create class for helpers so we don't have to pass the un/pw all the time
