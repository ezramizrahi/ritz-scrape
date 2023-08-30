from prometheus_client import start_http_server, Gauge
import psutil
import time

# Initialize metrics
cpu_usage = Gauge('scraper_cpu_usage_percent', 'CPU usage of the scraper')
memory_usage = Gauge('scraper_memory_usage_bytes', 'Memory usage of the scraper')
disk_read = Gauge('scraper_disk_read_bytes', 'Disk read in bytes')
disk_write = Gauge('scraper_disk_write_bytes', 'Disk write in bytes')
network_receive = Gauge('scraper_network_receive_bytes', 'Network data received in bytes')
network_send = Gauge('scraper_network_send_bytes', 'Network data sent in bytes')

def collect_metrics():
    # CPU usage
    cpu_usage.set(psutil.cpu_percent(interval=1))

    # Memory usage
    memory_info = psutil.virtual_memory()
    memory_usage.set(memory_info.used)

    # Disk I/O
    disk_info = psutil.disk_io_counters()
    disk_read.set(disk_info.read_bytes)
    disk_write.set(disk_info.write_bytes)

    # Network I/O
    network_info = psutil.net_io_counters()
    network_receive.set(network_info.bytes_recv)
    network_send.set(network_info.bytes_sent)

if __name__ == '__main__':
    # Start the server to expose metrics
    start_http_server(8000)
    
    while True:
        collect_metrics()
        time.sleep(5)