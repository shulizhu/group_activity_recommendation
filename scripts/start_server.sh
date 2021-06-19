#!/bin/bash

sudo systemctl restart nginx
sudo systemctl start group-act-backend
sudo systemctl enable group-act-backend
