#!/bin/bash

. ./unimelb-comp90024-2020-grp-45-openrc.sh; ansible-playbook -vvv --ask-become-pass deploy_couchdb.yaml -i hosts.ini