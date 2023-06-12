import subprocess
import psutil
import re
import os
import time
import requests
import keyboard
from termcolor import colored

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

    print(colored(logo, 'light_cyan'))
         
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
    print(colored("1. Check Network Status", "light_green"))
    print(colored("2. Check Disk Status", "light_green"))
    print(colored("3. Check CPU Load", "light_green"))
    print(colored("4. Check GPU Load", "light_green"))
    print(colored("5. Check Apache2 Status", "light_green"))
    print(colored("6. CPU Stress Test", "light_green"))
    print(colored("7. GPU Stress Test", "light_green"))
    print(colored("8. List Services ON", "light_green"))
    print(colored("E. Exit", "light_red"))

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
    while True:
        clear_screen()  # Clear the screen before displaying the menu
        display_logo()  # Display the logo
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
        elif choice == 'e':
              print("Exiting...")
              break
        else:
            print("Invalid choice. Please try again.")

        input("Press Enter to continue...")
        clear_screen()  # Clear the screen before going back to the menu

# Call the main function to start the program
main()
clear_screen()
