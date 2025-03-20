import random

def packet_handler(packet_size):
    print(f"Packet captured: {packet_size} bytes")

def main():
    print("Starting simulated packet capture...")

    # Simulating 10 packets with random sizes
    for _ in range(10):
        packet_size = 64 + random.randint(0, 1000)  # Random packet size (64-1064 bytes)
        packet_handler(packet_size)

    print("Packet capture simulation completed.")

if __name__ == "__main__":
    main()