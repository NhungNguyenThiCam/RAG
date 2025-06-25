import socket

def find_free_ports(start=8001, end=8100):
    free_ports = []
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                free_ports.append(port)
    return free_ports

ports = find_free_ports()
print("Các cổng rảnh có thể dùng:", ports[:10])  # In ra 10 cổng đầu tiên
