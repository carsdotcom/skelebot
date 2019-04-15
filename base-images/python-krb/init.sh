#!/bin/bash

user=$1
kinit -k -t /krb/auth.keytab $user
