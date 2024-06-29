import paramiko
import os

def send_file_to_vm(ssh, local_file, remote_path):
    sftp = ssh.open_sftp()
    sftp.put(local_file, remote_path)
    sftp.close()
    print('sent file')

def compile_file_on_vm(ssh, remote_path):
    stdin, stdout, stderr = ssh.exec_command(f"g++ {remote_path} -o {remote_path}.out")
    compile_output = stdout.read().decode('utf-8')
    if compile_output:
        print(f"Compilation output: {compile_output}")
    print(stderr)

def extract_syscalls_on_vm(ssh, executable_path):
    stdin, stdout, stderr = ssh.exec_command(f"strace -o {executable_path}.strace {executable_path}")
    # Wait for the command to finish
    stdout.channel.recv_exit_status()

def retrieve_syscalls_from_vm(ssh, remote_file_path, local_file_path):
    sftp = ssh.open_sftp()
    sftp.get(remote_file_path, local_file_path)
    sftp.close()

def main():
    # SSH connection details
    host = '192.168.134.128'
    port = 22
    username = 'kali'
    password = 'kali'

    # Local file to send to VM
    local_file_path = 'tester.cpp'
    # Remote directory on VM to store the file
    remote_dir = '/home/kali/Desktop/'
    # Remote path to store the file
    remote_file_path = os.path.join(remote_dir, os.path.basename(local_file_path))

    # Connect to VM using SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)

    try:
        # Send file to VM
        send_file_to_vm(ssh, local_file_path, remote_file_path)

        # Compile file on VM
        compile_file_on_vm(ssh, remote_file_path)

        # Extract system calls from executable on VM
        extract_syscalls_on_vm(ssh, remote_file_path + ".out")

        # Retrieve system calls file from VM
        remote_syscalls_file = remote_file_path + ".out.strace"
        local_syscalls_file = "test_syscalls.txt"
        retrieve_syscalls_from_vm(ssh, remote_syscalls_file, local_syscalls_file)

        print(f"System calls file retrieved and saved as {local_syscalls_file}")
    
        


    finally:
        ssh.close()

if __name__ == "__main__":
    main()
