import subprocess
import psutil
import re
import os
import sys
import time
import signal
import requests
import keyboard
import speedtest
import urllib.request
from getpass import getpass
from termcolor import colored, cprint

def clear_screen():
    # Clear the terminal screen
    if os.name == 'nt':  # For Windows
        _ = os.system('cls')
    else:  # For Linux and macOS
        _ = os.system('clear')
   
def display_logo():
    logo = '''
                 ┬─┐┬┌─┐┬ ┬┬
		 ├┬┘││  ├─┤│
		 ┴└─┴└─┘┴ ┴┴
    '''

    # Split the logo into lines
    logo_lines = logo.strip().split('\n')

    # Calculate the width of the console
    console_width = os.get_terminal_size().columns

    # Calculate the number of spaces needed to center each line of the logo
    num_spaces = (console_width - len(logo_lines[0])) // 2

    # Print the logo with centered alignment
    print('\n' * 2)  # Add some vertical spacing
    for line in logo_lines:
        print(' ' * num_spaces + colored(line.strip(), 'cyan'))
    print('\n' * 2)  # Add some vertical spacing
 
def check_network_status():
    try:
        # Send an HTTP GET request to a well-known website
        response = requests.get('http://www.google.com', timeout=5)

        if response.status_code == 200:
            print(colored('Network is online', 'green'))
        else:
            print(colored('Network is offline', 'red'))
    except requests.ConnectionError:
        print(colored('Network is offline', 'red'))
    except requests.Timeout:
        print(colored('Network connection timed out', 'red'))
    except requests.RequestException:
        print(colored('Error occurred while checking network status', 'red'))

def check_disk_status():
    # Check disk status
    disk_status = subprocess.run(['df', '-h'], capture_output=True, text=True)
    print(colored(disk_status.stdout, 'cyan'))

def check_cpu_load():
    # Check CPU load
    cpu_load = subprocess.run(['top', '-bn', '1'], capture_output=True, text=True)
    
    # Extract the average load using regular expressions
    average_load = re.search(r'load average: ([0-9.]+)', cpu_load.stdout)
    
    if average_load:
        print(colored(f'Average CPU Load: {average_load.group(1)}', 'cyan'))
    else:
        print(colored('Unable to retrieve CPU load information', 'red'))

def check_gpu_load():
    # Check GPU load
    gpu_load = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
    print(colored(gpu_load.stdout, 'cyan'))

def check_apache_status():
    # Check if Apache2 service is running
    apache_status = subprocess.run(['service', 'apache2', 'status'], capture_output=True, text=True)
    
    if 'Active: active (running)' in apache_status.stdout:
        # If Apache2 is running, display a colored message
        print(colored('Apache2 is ON', 'blue'))
        
        # Get the output of 'apachectl -S' command
        apache_info = subprocess.run(['apachectl', '-S'], capture_output=True, text=True)
        
        # Colorize and print the output of 'apachectl -S' command in cyan
        print(colored(apache_info.stdout, 'cyan'))
    else:
        print(colored('Apache2 is OFF', 'red'))

def display_menu():
    print(colored("Menu:", "yellow"))
    print(colored("1. Check Network Status				11. Test Internet Speed", "light_green"))
    print(colored("2. Check Disk Status				12. Run Htop", "light_green"))
    print(colored("3. Check CPU Load				13. Run IfTop", "light_green"))
    print(colored("4. Check GPU Load				14. Run Ranger", "light_green"))
    print(colored("5. Check Apache2 Status				15. Package Installer", "light_green"))
    print(colored("6. CPU Stress Test				16. Package Uninstaller", "light_green"))
    print(colored("7. GPU Stress Test				17. SSH Connection", "light_green"))
    print(colored("8. List Services ON				18. Live System Stats", "light_green"))
    print(colored("9. Ping LocalHost", "light_green"))
    print(colored("10. Ping IP/Domain", "light_green"))
    print(colored("E. Exit						S. Update System", "light_red"))

def get_gpu_stats():
    try:
        output = subprocess.check_output(["nvidia-smi", "--query-gpu=utilization.gpu,power.draw", "--format=csv,noheader,nounits"]).decode("utf-8").strip().split("\n")
        gpu_load, gpu_power = output[0].split(", ")
        return float(gpu_load), float(gpu_power)
    except subprocess.CalledProcessError:
        return None, None


def get_color(load):
    if load < 30:
        return "light_green"
    elif load >= 30 and load < 60:
        return "yellow"
    else:
        return "red"

def print_live_stats():
    while True:
        cpu_load = psutil.cpu_percent()
        gpu_load, gpu_power = get_gpu_stats()
        disk_load = psutil.disk_usage("/").percent
        memory_usage = psutil.virtual_memory().percent

        os.system("clear")  # Clears the terminal screen
        display_logo() # Display logo

        print("\n" + "-" * 30 + " Live System Stats " + "-" * 30)
        print(f"CPU Load: {colored(f'{cpu_load:6.2f}%', get_color(cpu_load))}")

        if gpu_load is not None and gpu_power is not None:
            print(f"GPU Load: {colored(f'{gpu_load:6.2f}%', get_color(gpu_load))}")
            print(f"GPU Power: {colored(f'{gpu_power:6.2f} W', get_color(gpu_power))}")

        print(f"Disk Load: {colored(f'{disk_load:6.2f}%', get_color(disk_load))}")
        print(f"Memory Usage: {colored(f'{memory_usage:6.2f}%', get_color(memory_usage))}")
        print("-" * 75)

        if keyboard.is_pressed("q"): # If pressed "q" the print_live_stats will close
            break

        time.sleep(1)  # Delay to refresh the stats every 1 seconds

        
def ssh_connection():
    host = input(colored("Enter the host address: ", "cyan"))
    port = input(colored("Enter the port number: ", "cyan"))
    username = input(colored("Enter your username: ", "green"))
    password = input(colored("Enter your password: ", "yellow"))

    cprint("Establishing SSH connection...", "magenta")

    command = f"sshpass -p '{password}' ssh -X {username}@{host} -p {port}"
    subprocess.call(command, shell=True)
    print(colored("SSH connection closed.", "light_red"))
    
def update_system():
    print(colored("Updating the system...", "yellow"))
    update_command = ""

    if os.name == 'nt':
        print("System update is not supported on Windows.")
        return
    elif os.name == 'posix':
        if os.path.exists('/usr/bin/apt-get'):
            update_command = 'apt-get update && apt-get upgrade'
        elif os.path.exists('/usr/bin/yum'):
            update_command = 'yum update'
        else:
            print("Unable to determine the system updater command.")
            return

    subprocess.run(update_command, shell=True)

    print(colored("System update completed.", "green"))
    
def uninstall_packages():
    print(colored("Uninstalling packages...", "yellow"))
    package_manager = ""

    if os.name == 'nt':
        print("Package uninstallation is not supported on Windows.")
        return
    elif os.name == 'posix':
        if os.path.exists('/usr/bin/apt-get'):
            package_manager = 'apt-get'
        elif os.path.exists('/usr/bin/yum'):
            package_manager = 'yum'
        else:
            print("Unable to determine the package manager.")
            return

    packages = input("Enter the packages you want to uninstall (comma-separated): ").split(',')
    packages = [pkg.strip() for pkg in packages]

    uninstall_command = [package_manager, 'remove']
    uninstall_command.extend(packages)

    subprocess.run(uninstall_command)

    print(colored("Package uninstallation completed.", "green"))
    
def install_packages():
    print(colored("Installing packages...", "yellow"))
    package_manager = ""

    if os.name == 'nt':
        print("Package installation is not supported on Windows.")
        return
    elif os.name == 'posix':
        if os.path.exists('/usr/bin/apt-get'):
            package_manager = 'apt-get'
        elif os.path.exists('/usr/bin/yum'):
            package_manager = 'yum'
        else:
            print("Unable to determine the package manager.")
            return

    packages = input("Enter the packages you want to install (comma-separated): ").split(',')
    packages = [pkg.strip() for pkg in packages]

    install_command = [package_manager, 'install']
    install_command.extend(packages)

    subprocess.run(install_command)

    print(colored("Package installation completed.", "green"))
    
def run_ranger():
    print(colored("Running ranger...", "yellow"))
    ranger_process = subprocess.Popen(["ranger"], preexec_fn=os.setsid)

    def stop_ranger(e):
        os.killpg(os.getpgid(ranger_process.pid), signal.SIGTERM)
        keyboard.unhook_all()

    keyboard.on_press_key('q', stop_ranger)
    ranger_process.wait()

    print(colored("Exited ranger.", "green"))
    
def run_iftop():
    print(colored("Running iftop...", "yellow"))
    iftop_process = subprocess.Popen(["iftop"], preexec_fn=os.setsid)

    def stop_iftop(e):
        os.killpg(os.getpgid(iftop_process.pid), signal.SIGTERM)
        keyboard.unhook_all()

    keyboard.on_press_key('q', stop_iftop)
    iftop_process.wait()

    print(colored("Exited iftop.", "green"))
    
def run_htop():
    print(colored("Running htop...", "yellow"))
    print(colored("Press Q to exit htop", "yellow"))
    htop_process = subprocess.Popen(["htop"], preexec_fn=os.setsid)

    def stop_htop(e):
        os.killpg(os.getpgid(htop_process.pid), signal.SIGTERM)
        keyboard.unhook_all()

    keyboard.on_press_key('q', stop_htop)
    htop_process.wait()

    print(colored("Exited htop.", "green"))
    
def measure_internet_speed():
    print("Measuring internet speed...")
    
    speed_test = speedtest.Speedtest()
    download_speed = speed_test.download() / 1024 / 1024
    upload_speed = speed_test.upload() / 1024 / 1024
    
    print(f"Download speed: {download_speed:.2f} Mbps")
    print(f"Upload speed: {upload_speed:.2f} Mbps")
    print("Speed measurement completed.")

def ping_localhost():
    print(colored("Pinging localhost...", "yellow"))
    print(colored("Press Q to exit Ping", "yellow"))
    
    ping_process = subprocess.Popen(['ping', 'localhost'], stdout=subprocess.PIPE)

    start_time = time.time()
    stop_flag = False

    def stop_ping(e):
        nonlocal stop_flag
        stop_flag = True
        ping_process.terminate()

    keyboard.on_press_key('q', stop_ping)

    while ping_process.poll() is None and not stop_flag:
        elapsed_time = time.time() - start_time
        if elapsed_time > 5:  # Check for ping response every 5 seconds
            print(ping_process.stdout.readline().decode().strip())
            start_time = time.time()

    if not stop_flag:
        print(colored("Ping completed.", "green"))
        
def ping_address():
    address = input("Enter IP address or domain to ping: ")
    print(colored(f"Pinging {address}...", "yellow"))
    print(colored(f"Press Q to exit Ping", "yellow"))
    
    ping_process = subprocess.Popen(['ping', address], stdout=subprocess.PIPE)

    start_time = time.time()
    stop_flag = False

    def stop_ping(e):
        nonlocal stop_flag
        stop_flag = True
        ping_process.terminate()

    keyboard.on_press_key('q', stop_ping)

    while ping_process.poll() is None and not stop_flag:
        elapsed_time = time.time() - start_time
        if elapsed_time > 5:  # Check for ping response every 5 seconds
            print(ping_process.stdout.readline().decode().strip())
            start_time = time.time()

    if not stop_flag:
        print(colored("Ping completed.", "green"))
        
def list_services_on():
    print("Services currently ON:")
    services = ['apache2', 'mysql', 'nginx']

    for service in services:
        try:
            result = subprocess.run(['systemctl', 'is-active', service], capture_output=True, text=True, check=True)

            if result.stdout.strip() == 'active':
                print(colored(f"{service}: ON", 'green'))
            else:
                print(colored(f"{service}: OFF", 'red'))
        except subprocess.CalledProcessError:
            print(colored(f"Failed to check {service} status", 'red'))

def perform_cpu_stress_test():
    duration = int(input("Enter stress test duration (in seconds): "))

    print(colored(f"Performing CPU stress test for {duration} seconds...", "yellow"))

    start_time = time.time()
    load_values = []

    while time.time() - start_time < duration:
        load = psutil.cpu_percent(interval=1, percpu=False)
        load_values.append(load)
        average_load = sum(load_values) / len(load_values)

        print(f"Average CPU Load: {average_load:.2f}%")
        time.sleep(1)

    print(colored("CPU stress test completed.", "green"))

    
def perform_gpu_stress_test():
    duration = int(input("Enter stress test duration (in seconds): "))

    print(colored(f"Performing GPU stress test for {duration} seconds...", "yellow"))
    print(colored("Press 'q' to stop the stress test.", "yellow"))

    start_time = time.time()
    stop_flag = False

    def stop_test(e):
        nonlocal stop_flag
        stop_flag = True

    keyboard.on_press_key('q', stop_test)

    while time.time() - start_time < duration and not stop_flag:
        # Perform intensive mathematical calculations
        # You can replace this with your own workload or use libraries like NumPy or TensorFlow
        result = 0
        for i in range(10 ** 7):
            result += i

    if not stop_flag:
        print(colored("GPU stress test completed.", "green"))

        
def main():
    if not os.geteuid() == 0:
        print("This program needs to be run with sudo privileges.")
        sys.exit(1)

    while True:
        clear_screen()
        display_logo()
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                check_network_status()
            except Exception as e:
                print(colored(f"Failed to check network status: {str(e)}", 'red'))
        elif choice == '2':
            try:
                check_disk_status()
            except Exception as e:
                print(colored(f"Failed to check disk status: {str(e)}", 'red'))
        elif choice == '3':
            try:
                check_cpu_load()
            except Exception as e:
                print(colored(f"Failed to check CPU load: {str(e)}", 'red'))
        elif choice == '4':
            try:
                check_gpu_load()
            except Exception as e:
                print(colored(f"Failed to check GPU load: {str(e)}", 'red'))
        elif choice == '5':
            try:
                check_apache_status()
            except Exception as e:
                print(colored(f"Failed to check Apache2 status: {str(e)}", 'red'))
        elif choice == '6':
            try:
                perform_cpu_stress_test()
            except Exception as e:
                print(colored(f"Failed to perform CPU stress test: {str(e)}", 'red'))
        elif choice == '7':
            try:
                perform_gpu_stress_test()
            except Exception as e:
                print(colored(f"Failed to perform GPU stress test: {str(e)}", 'red'))
        elif choice == '8':
             list_services_on()
        elif choice == '9':
            try:
                ping_localhost()
            except Exception as e:
                print(colored(f"Failed to Ping LocalHost: {str(e)}", 'red'))
        elif choice == '10':
            try:
                ping_address()
            except Exception as e:
                print(colored(f"Failed to Ping Address: {str(e)}", 'red'))
        elif choice == '11':
            try:
                measure_internet_speed()
            except Exception as e:
                print(colored(f"Failed to Test Internet Speed: {str(e)}", 'red'))
        elif choice == '12':
            try:
                run_htop()
            except Exception as e:
                print(colored(f"Failed to run Htop: {str(e)}", 'red'))
        elif choice == '13':
            try:
                run_iftop()
            except Exception as e:
                print(colored(f"Failed to run Iftop: {str(e)}", 'red'))
        elif choice == '14':
            try:
                run_ranger()
            except Exception as e:
                print(colored(f"Failed to run Ranger: {str(e)}", 'red'))
        elif choice == '15':
            try:
                install_packages()
            except Exception as e:
                print(colored(f"Failed to Download Package: {str(e)}", 'red'))
        elif choice == '16':
            try:
                uninstall_packages()
            except Exception as e:
                print(colored(f"Failed to Update System: {str(e)}", 'red'))
        elif choice == '17':
            try:
                ssh_connection()
            except Exception as e:
                print(colored(f"Failed to Connect to Host: {str(e)}", 'red'))
        elif choice == '18':
            try:
                print_live_stats()
            except Exception as e:
                print(colored(f"Failed to Display the System Stats: {str(e)}", 'red'))
        elif choice == 's':
            try:
                update_system()
            except Exception as e:
                print(colored(f"Failed to Exit the Menu: {str(e)}", 'red'))
        elif choice == 'e':
              print("Exiting...")
              break
        else:
            print("Invalid choice. Please try again.")

        input("Press Enter to continue...")
        clear_screen()  # Clear the screen before going back to the menu

# Call the main function to start the program
if __name__ == "__main__":
    main()
clear_screen()
