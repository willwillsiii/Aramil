#!/bin/bash
BACKUP_FILENAME=aradev-`date +%a_%b_%d_%H-%M-%S_%Z_%Y`.tar.gz
tar -zcf /home/pi/backups/aradev/$BACKUP_FILENAME -C /opt/ aradev/ && \
echo "/opt/aradev backed up to /home/pi/backups/aradev/$BACKUP_FILENAME"
