import time
import ping3 
import threading


def convert_ip2int(ip):
    hex_ip = list(map(hex,list(map(int,ip.split('.')))))
    ip_value = int(''.join([val[2:].zfill(2) for val in hex_ip]), 16)
    return ip_value

def convert_ip2int_start_range(ip, ip_range):
    value = convert_ip2int(ip)
    bit_unchange = 32 - ip_range
    init_val = int(bin(value)[2:].zfill(32)[:-bit_unchange] + bit_unchange * '0', 2)
    return init_val

def convert_int2ip(value):
    hex_val = hex(value)[2:].zfill(8)
    ip_list = []
    for i in range(4):
        ip_list.append(str(int(hex_val[i*2: (i+1) * 2], 16)))
    return '.'.join(ip_list)

def is_valid_ip(ip):
    ip_list = ip.split('.')
    if len(ip_list) > 4:
        return False
    for sec in ip_list:
        if int(sec) == 0 or int(sec) > 255:
            return False
    return True

def ping_ip(ip, c, timeout):
    succ = 0
    avg_ping = 0
    for i in range(c):
        try:
            ping = ping3.ping(ip, unit='ms')
            if not ping == None:
                avg_ping += ping / 4
                succ += 1
        except:
            pass
    return avg_ping, succ, c

def return_ips(inp, c=4, timeout=1, filename='tmp.txt'):
    ip, ip_range= inp.split('/')
    ip_range = int(ip_range)
    ip_count = 2 ** (32 - ip_range)
    init_ip = convert_ip2int_start_range(ip, ip_range)
    stats = []
    idx = int(filename.split('.')[0])
    total[idx] = ip_count
    for i in range(1, ip_count):
        tasks[idx] += 1
        ip_add = convert_int2ip(init_ip + i)
        res = ping_ip(ip_add, c=c, timeout=timeout)
        if res[1] == res[2]:
            stats.append((ip_add, res[0], res[1]))
    stats.sort(key=lambda x: x[1])
    with open(filename, 'w') as f:
        for i in range(len(stats)):
            f.write('%s %.2f ms %d/%d' % (stats[0], stat[1], stat[2], stat[2]))
    print("%s done!" % filename)



    


    
inp = ['103.21.244.0/22',
       '103.22.200.0/22',]
#       '103.31.4.0/22',
#       '104.16.0.0/13',
#       '104.24.0.0/14',
#       '108.162.192.0/18',
#       '131.0.72.0/22', 
#       '141.101.64.0/18',
#       '162.158.0.0/15',
#       '172.64.0.0/13',
#       '173.245.48.0/20',
#       '188.114.96.0/20',
#       '190.93.240.0/20',
#       '197.234.240.0/22',
#       '198.41.128.0/17']


global tasks 
global total 
total = [0] * len(inp)
tasks = [0] * len(inp)
threads = []
for i, val in enumerate(inp):
    threads.append(threading.Thread(target=return_ips, args=(val, 4, 0.2, '%d.txt' % i), daemon=True))
    threads[-1].start()

while True:
    end = True
    toprint = [] 
    for i in range(len(tasks)):
        end = end and (tasks[i] == (total[i]-1))
        per = int(tasks[i]/total[i])
        per_inv = 30 - per
        res = '[' + '=' * per + ' ' * per_inv + ']' + '%d: %d / %d' % (i, tasks[i], total[i])
        toprint.append(res)
    result = '\n'.join(toprint)
    print ("\033[0;0H", end='')
    print('\r%s' % result, end='')
    time.sleep(1)
        




