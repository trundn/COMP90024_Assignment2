#!/bin/bash

. ./unimelb-comp90024-2020-grp-45-openrc.sh; ansible-playbook --ask-become-pass -vvv deploy_harvester.yaml -i hosts.ini