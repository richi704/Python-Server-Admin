import subprocess

def install_with_pip(package):
    try:
        subprocess.check_call(['sudo', 'pip', 'install', package])
    except subprocess.CalledProcessError:
        print(f"Failed to install {package} with pip.")

def install_with_apt(package):
    try:
        subprocess.check_call(['sudo', 'apt', 'install', '-y', package])
    except subprocess.CalledProcessError:
        print(f"Failed to install {package} with apt.")

def install_packages_from_requirements(requirements_file):
    with open(requirements_file, 'r') as file:
        packages = file.read().splitlines()

    for package in packages:
        install_with_pip(package)
        install_with_apt(package)

# Example usage
requirements_file = 'requirements.txt'
install_packages_from_requirements(requirements_file)
