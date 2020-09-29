#! /bin/sh

SRCS="."
DEST=pi@rover.bogus.domain:Projects/Sunfounder_Smart_Video_Car_Kit_for_RaspberryPi/

OPTS='-av --exclude-from=.rsyncignore'

rsync $OPTS $SRCS $DEST
