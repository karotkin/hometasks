#!/usr/bin/python

import psutil
import datetime
import configparser
import time
import json
import schedule

config = configparser.ConfigParser()
config.read('config.ini')
timeint = config.get('setup', 'int')
filetype = config.get('setup', 'filetype')

snapshot = 1

# CPU_Load
cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
# Overall_Memory_Usage
mem_usage = psutil.Process().memory_info()[0]
# Hard_Disk_Memory_Usage
disk_usage = psutil.disk_usage('/')
# Overal_Virtual_Memory_Usage
total_memory = psutil.virtual_memory()
# IO_Information
disk_part = psutil.disk_io_counters(perdisk=False)
# Network_Information
net_inf = psutil.net_io_counters()

def write_to_txt(myfile='result.txt'):
    global snapshot
    print("info >> top(SNAPSHOT {0})".format(snapshot))
    fmt = '%Y-%m-%d %H:%M:%S %Z'
    currenttime = datetime.datetime.now()
    tstmp = datetime.datetime.strftime(currenttime, fmt)
    text_file = open(myfile, "w")
    text_file.write("Snapshot {0}:, timestamp - {1}:\n".format(snapshot, tstmp))
    text_file.write("CPU: {0}\n".format(cpu_usage[0]))
    text_file.write("MEM: {0}\n".format(mem_usage/1048576))
    text_file.write("DISK TOTAL: {0}Mb\n".format(disk_usage.total/1048576))
    text_file.write("DISK FREE: {0}Mb\n".format(disk_usage.free/1048576))
    text_file.write("DISK USED: {0}Mb\n".format(disk_usage.used/1048576))
    text_file.write("DISK PERCENT: {0}\n".format(disk_usage.percent))
    text_file.write("TOTAL MEMORY: {}Mb\n".format(total_memory.total/1048576))
    text_file.write("USED MEMORY: {}Mb\n".format(total_memory.used/1048576))
    text_file.write("FREE MEMORY: {}Mb\n".format(total_memory.free/1048576))
    text_file.write("MEMORY PERCENT: {0}\n".format(total_memory.percent))
    text_file.write("DISK PARTS: {}\n".format(disk_part))
    text_file.write("BYTES RECIVED: {}\n".format(net_inf.bytes_recv))
    text_file.write("BYTES SENT: {}\n".format(net_inf.bytes_sent))
    text_file.write("PACKETS RECIVED: {}\n".format(net_inf.packets_recv))
    text_file.write("PACKETS SENT: {}\n".format(net_inf.packets_sent))
    text_file.write("\n")
    text_file.close()
    snapshot += 1

def mydict(kf):
    a = list(kf)
    b = kf._fields
    final_dict = dict(zip(a,b))
    return final_dict
def write_to_json(myfile="result.json"):
    global snapshot
    print("info >> top(SNAPSHOT {0})".format(snapshot))
    fmt = '%Y-%m-%d %H:%M:%S %Z'
    currtime = datetime.datetime.now()
    tstmp = datetime.datetime.strftime(currtime, fmt)
    jsonf = open("result.json", "a")
    jsonf.write("\nSnapshot #{0}, Snapshot Time - {1}\n".format(snapshot, tstmp))
    jsonf.write("\nCPU\n")
    json.dump(cpu_usage, jsonf, indent=1)
    jsonf.write("\nVMem Usage\n")
    json.dump(mem_usage, jsonf, indent=1)
    jsonf.write("\nDisk Usage\n")
    json.dump(mydict(disk_usage), jsonf, indent=1)
    jsonf.write("\nDisk Part\n")
    json.dump(mydict(disk_part), jsonf, indent=1)
    jsonf.write("\nNetInf\n")
    json.dump(net_inf, jsonf, indent=1)
    jsonf.write("\n\n")
    jsonf.close()
    snapshot += 1
if filetype == "txt":
    print(filetype + ' in' + timeint + ' minute(s)')
    schedule.every(int(timeint)).minutes.do(write_to_txt)
elif filetype == "json":
    print(filetype + ' in' + timeint + ' minute(s)')
    schedule.every(int(timeint)).minutes.do(write_to_json)
else:
    print("check type in conf")
    quit()
while True:
    schedule.run_pending()
    time.sleep(5)
