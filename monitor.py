import os
import sys
import socket
import time
import datetime as dt

FILE = os.path.join(os.getcwd(), "networkinfo.log")


from datetime import datetime
import pytz
def get_time():
  UTC = pytz.utc
  IST = pytz.timezone("Asia/Kolkata")
  datetime_ist = datetime.now(IST)
  current_time=str(datetime_ist.strftime("%I:%M:%S %p"))
  date=str(datetime_ist.strftime('%d:%m:%Y'))
  return date,current_time 


def ping():
	# to ping a particular IP
	try:
		socket.setdefaulttimeout(3)
		
		# if data interruption occurs for 3
		# seconds, <except> part will be executed

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# AF_INET: address family
		# SOCK_STREAM: type for TCP

		host = "8.8.8.8"
		port = 53

		server_address = (host, port)
		s.connect(server_address)

	except OSError as error:
		return False
		# function returns false value
		# after data interruption

	else:
		s.close()
		# closing the connection after the
		# communication with the server is completed
		return True


def calculate_time(start, stop):

	# calculating unavailabilty
	# time and converting it in seconds
	difference = stop - start
	seconds = float(str(difference.total_seconds()))
	return str(dt.timedelta(seconds=seconds)).split(".")[0]



def first_check():
	# to check if the system was already
	# connected to an internet connection

	if ping():
		# if ping returns true
		live = "\nCONNECTION ACQUIRED\n"
		print(live)
		connection_acquired_time = datetime.now()
		d,t=get_time()
		acquiring_message = f"connection acquired at: {d} {t}" 
		print(acquiring_message)

		with open(FILE, "a") as file:
		
			# writes into the log file
			file.write(live)
			file.write(acquiring_message)

		return True

	else:
		# if ping returns false
		not_live = "\nCONNECTION NOT ACQUIRED\n"
		print(not_live)

		with open(FILE, "a") as file:
		
			# writes into the log file
			file.write(not_live)
		return False


def main():

	# main function to call functions
	monitor_start_time =datetime.now()
	d,t=get_time()
	monitoring_date_time = f"monitoring started at: {d} {t}"

	if first_check():
		# if true
		print(monitoring_date_time)
		# monitoring will only start when
		# the connection will be acquired

	else:
		# if false
		while True:
		
			# infinite loop to see if the connection is acquired
			if not ping():
				
				# if connection not acquired
				time.sleep(1)
			else:
				
				# if connection is acquired
				first_check()
				print(monitoring_date_time)
				break

	with open(FILE, "a") as file:
	
		# write into the file as a into networkinfo.log,
		# "a" - append: opens file for appending,
		# creates the file if it does not exist???
		file.write("\n")
		file.write(monitoring_date_time + "\n")

	while True:
	
		# infinite loop, as we are monitoring
		# the network connection till the machine runs
		if ping():
			
			# if true: the loop will execute after every 5 seconds
			time.sleep(5)

		else:
			# if false: fail message will be displayed
			down_time = datetime.now()
			d,t=get_time()
   
			fail_msg = f"disconnected at: {d} {t} "
			print(fail_msg)

			with open(FILE, "a") as file:
				# writes into the log file
				file.write(fail_msg + "\n")

			while not ping():
			
				# infinite loop, will run till ping() return true
				time.sleep(1)

			up_time =datetime.now()
			
			# after loop breaks, connection restored
			d,t=get_time()
			uptime_message = f"connected again: {d} {t}"

			down_time = calculate_time(down_time, up_time)
			unavailablity_time = "connection was unavailable for: " + down_time

			print(uptime_message)
			print(unavailablity_time)

			with open(FILE, "a") as file:
				
				# log entry for connection restoration time,
				# and unavailability time
				file.write(uptime_message + "\n")
				file.write(unavailablity_time + "\n")
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        os.system("python3 save.py")
        sys.exit(0)
