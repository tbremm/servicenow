# servicenow
Contains servicenow api helpers

# Usage
`python ./get_emails_from_groups.py --url_prefix=<url_prefix> -i <path to input file> -o <path to output file> -n <username>> -p <password>>`
* url_prefix: the first part of the url, eg. https://<url_prefix>.service-now.com
* input file: The path (relative or absolute) to the input file
    * Input file should be a newline-separated list of user groups
* output file: The path (relative or absolute) to the output file
    * This will be a newline-separated list of the email addresses of everyone in the given groups
* Username: The username of the account that this will be running as (must have appropriate api and table permissions)
* Password: The password for the given username


# TODO
* Create class for helpers so we don't have to pass the un/pw all the time
