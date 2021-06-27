#!/bin/bash

BASE=$HOME/group_act_backend
VENV=$BASE/venv

sudo python3 -m venv $VENV
sudo $VENV/bin/pip3 install -r $BASE/requirements.txt
sudo rm -rf $BASE/group_act_backend/build
sudo aws s3 cp s3://group-act $BASE/group_act_backend/build --recursive
