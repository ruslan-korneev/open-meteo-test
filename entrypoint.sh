#!/bin/bash

dj collectstatic --noinput
dj migrate
"$@"