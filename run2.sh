#!/bin/sh
cd modbus_1/
nohup python3 SEND_DATA_HOURLY.py >/dev/null 2>&1 &
