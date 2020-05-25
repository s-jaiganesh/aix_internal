To set bosboot & bootlist

instructions:-
  1. Download emgr.py and emgr-preview.yml
  2. mkdir library
  3. mv emgr.py library/
  4. run playbook
      # ansible-playbook emgr-preview.yml -i hostfile -u username

to check syntax error in yaml file:-
  1. yum install yamllint
  2. run below command
      # yamllint emgr-preview.yml
