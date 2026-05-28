import psutil

x = psutil.cpu_percent(interval = 5, percpu = True)

y = psutil.cpu_freq()


print (x)
print (y)