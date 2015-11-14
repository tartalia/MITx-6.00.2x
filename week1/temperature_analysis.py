import pylab

def get_data():
    f = open('julyTemps.txt', 'r')
    low_temps, high_temps, days = [], [], []
    for line in f:
        fields = line.split(' ')
        if fields[0].isdigit():
            high_temps.append(int(fields[1]))
            low_temps.append(int(fields[2]))
    return low_temps, high_temps

def produce_plot(low_temps, high_temps, diff_temps):
    days = range(1, 32)
    pylab.plot(days, low_temps)
    pylab.title('Day by Day Ranges in Temperature in Boston in July 2012')
    pylab.xlabel('Days')
    pylab.ylabel('Temperature Ranges')
    pylab.show()

low_temps, high_temps = get_data()
diff_temps = map(lambda x, y: x - y, high_temps, low_temps)

produce_plot(low_temps, high_temps, diff_temps)

# print low_temps
# print high_temps
# print diff_temps
