To set bosboot & bootlist

instructions:-
  1. Download bosboot.py, devices.py & aix_precheck.yml
  2. mkdir library
  3. mv bosboot.py library/
  4. run playbook
      # ansible-playbook aix_precheck.yml -i hostfile -u username

to check syntax error in yaml file:-
  1. yum install yamllint
  2. # yamllint aix_precheck.yml
