import subprocess
import time

command = "echo 1 > /sys/class/gpio/gpio48/value"
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
output, error = process.communicate()
print("turn on output: " + str(output))
print("turn on error: " + str(error))

time.sleep(0.5)

command = "i2cset -y 2 0x1b 0x0b 0x00 0x00 0x00 0x00 i"
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
output, error = process.communicate()
print("i2cset 1 output: " + str(output))
print("i2cset 1 error: " + str(error))

time.sleep(0.1)

command = "i2cset -y 2 0x1b 0x0c 0x00 0x00 0x00 0x15 i"
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
output, error = process.communicate()
print("i2cset 2 output: " + str(output))
print("i2cset 2 error: " + str(error))