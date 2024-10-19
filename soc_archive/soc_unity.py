import socket
import struct

# UDPの受信設定
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(("10.20.153.194", 5002))  # IPアドレスを指定してバインド


print("Waiting for UDP data...")

while True:
    data, addr = udp_socket.recvfrom(1024)  # データを受信
    x, y, z = struct.unpack('fff', data[:12])  # 受信したデータからX, Y, Z座標を抽出
    print(f"Received position: X={x}, Y={y}, Z={z} from {addr}")
