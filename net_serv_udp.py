#! /usr/bin/python3

import os
import socket
import random
import json
from datetime import datetime

log_f = './rgr_list.json'
log_f_tmp = './rgr_list.tmp'
db_rgz = {}

if __name__ == '__main__':
	try:
		with open(log_f, "r") as open_log:
			db_rgz = json.load(open_log)
	except FileNotFoundError:
		pass

	try:
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
			sock.bind(("127.0.0.1", 40069))
			while True:
				req, addr = sock.recvfrom(1024)
				if req:
					user_name = req.decode('utf-8')
					if user_name in db_rgz:
						sock.sendto(db_rgz[user_name]['n_var'].encode('utf-8'), addr)
						print("Attention, user $" + user_name  + "$ is trying to get a new variant! " + "Old:" + json.dumps(db_rgz[user_name]))
					else:
						with open(log_f_tmp, "w") as write_log:
							date_time = datetime.now()
							date_mod = datetime.strftime(date_time, "%Y-%m-%d-%H-%M-%S")
							var_rgz = str(random.randint(1,20))
							db_rgz[user_name] = {
								"date": date_mod, 
								"n_var": var_rgz,
							}
							json.dump(db_rgz, write_log)
							sock.sendto(var_rgz.encode('utf-8'), addr)
							print(user_name + ":" + json.dumps(db_rgz[user_name]))
				pass
	except KeyboardInterrupt:
		try:
			os.rename(log_f_tmp, log_f)
		except OSError as err_os:
			print(err_os)
		print("\nClose app!")