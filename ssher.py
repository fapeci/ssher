import paramiko, time,socket

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


commands = ['show version','show ip interface brief','show tech']
hosts = ['192.168.0.177','192.168.0.178','192.168.0.179']
username ='cisco'
password ='cisco123'

def collector(host,commands,username,password):
    output = ''
    for command in commands:
        try:
            ssh.connect(host, username=username, password=password)
            chan = ssh.invoke_shell()
            time.sleep(1)
            chan.send('en\n')
            chan.send('cisco123\n')
            time.sleep(1)
            chan.send(command + '\n')
            print 'Sending command .... ' + command
            chan.recv(99)
            time.sleep(9)
            read = chan.recv(999999)
            print 'Reading the output from command ...' + command
            output = output + '################ Begin of '+ command +' ################\n'+  read + '\n################# End of '+ command +' ###############\n'
        except EOFError:
            pass
        except paramiko.SSHException:
            pass
        except socket.error:
            pass
        finally:
            ssh.close()
    time.sleep(5)
    return output

for host in hosts:
    print '############### Begin outputting the commands from host '+ host+ '######################\n\n'
    output = collector(host, commands, username, password)
    print output + '\n############### End of outputting the commands from host '+ host+ '######################\n'