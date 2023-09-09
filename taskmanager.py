import psutil
import csv
import matplotlib.pyplot as plt
import time
import streamlit as st


def plot_graph(x, y, title):
    plt.plot(x, y)
    plt.title(title)
    plt.show()

with open('systemresources.csv', mode='w', newline='') as file:
    fieldnames = ['timestamp', 'cpu_usage', 'memory_usage', 'disk_usage', 'read_bytes', 'write_bytes']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()

    start_time = time.monotonic()
    while time.monotonic() - start_time < 300:
        #timestamp = from_unixtime(time.time())
        timestamp = (time.ctime())

        cpu_usage = psutil.cpu_percent()

        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent

        disk_info = psutil.disk_usage("/")
        disk_usage = disk_info.percent
        
        io_counters = psutil.disk_io_counters()
        read_bytes = io_counters.read_bytes
        write_bytes = io_counters.write_bytes

        writer.writerow({'timestamp': timestamp, 'cpu_usage': cpu_usage, 'memory_usage': memory_usage, 'disk_usage': disk_usage, 'read_bytes': read_bytes, 'write_bytes': write_bytes})

        time.sleep(1)

    file.close()


def main():
    st.set_page_config(page_title='System Resource Utilization')

    with open('systemresources.csv', mode='r') as file:
        reader = csv.DictReader(file)
        timestamps = []
        cpu_usage = []
        memory_usage = []
        disk_usage = []
        read_bytes = []
        write_bytes = []

        for row in reader:
            timestamps.append((row['timestamp']))
            cpu_usage.append(float(row['cpu_usage']))
            memory_usage.append(float(row['memory_usage']))
            disk_usage.append(float(row['disk_usage']))
            read_bytes.append(float(row['read_bytes']))
            write_bytes.append(float(row['write_bytes']))
    
    st.write('select the graph to be displayed')

    st.button('CPU Usage', on_click=plot_graph(timestamps, cpu_usage, 'CPU usage'))
    st.button('Memory Usage', on_click=plot_graph(timestamps, memory_usage, 'Memory usage'))
    st.button('Disk Usage', on_click=plot_graph(timestamps, disk_usage, 'Disk usage'))
    st.button('Read Bytes', on_click=plot_graph(timestamps, read_bytes, 'Read bytes'))
    st.button('Write Bytes', on_click=plot_graph(timestamps, write_bytes, 'Write bytes'))


if __name__ == '__main__':
    main()