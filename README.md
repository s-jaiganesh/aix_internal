To set bosboot & bootlist

instructions:-
  1. Download bosboot.py, devices.py & aix_precheck.yml
  2. mkdir library
  3. mv bosboot.py library/
  4. run playbook
      # ansible-playbook aix_precheck.yml -i hostfile -u username
