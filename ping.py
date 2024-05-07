import subprocess

def check_ip_status(ip_address):
    try:
        subprocess.run(["ping", "-c", "1", ip_address], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{ip_address} is up")
    except subprocess.CalledProcessError:
        print(f"{ip_address} is down")

if __name__ == "__main__":
    ip_address = input("Enter the IP address to ping: ")
    check_ip_status(ip_address)
