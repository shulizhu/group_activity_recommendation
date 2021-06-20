#!/bin/bash

$BASE=$HOME/group_act_backend
$VENV=$BASE/venv

sudo python3 -m venv $VENV
sudo $VENV/bin/pip3 install -r -r $BASE/requirements.txt
