
import os
import glob
import md5
import paramiko

hostname = '192.168.1.93'  # remote hostname where SSH server is running
port = 22
username = 'pi'
password = None
rsa_private_key = r"c:\rootCygwin\home\s227783\.ssh\id_rsa"

dir_local = r"c:\tmp"
dir_remote = "remote_machine_folder"
glob_pattern = '*.xml'
files_copied = 0

RECV_BYTES = 4096


paramiko.common.logging.basicConfig(level=paramiko.common.INFO)


def agent_auth(transport, username):
    """
    Attempt to authenticate to the given transport using any of the private
    keys available from an SSH agent or from a local private RSA key file (assumes no pass phrase).
    """
    global ki
    try:
        ki = paramiko.RSAKey.from_private_key_file(rsa_private_key)
    except Exception, e:
        print 'Failed loading' % (rsa_private_key, e)

    agent = paramiko.Agent()
    agent_keys = agent.get_keys() + (ki,)
    if len(agent_keys) == 0:
        return

    for key in agent_keys:
        print 'Trying ssh-agent key %s' % key.get_fingerprint().encode('hex'),
        try:
            transport.auth_publickey(username, key)
            print '... success!'
            return
        except paramiko.SSHException, e:
            print '... failed!', e


def remotecopyfiles():
    for fname in glob.glob(dir_local + os.sep + glob_pattern):
        is_up_to_date = False
        if fname.lower().endswith('xml'):
            local_file = os.path.join(dir_local, fname)
            remote_file = dir_remote + '/' + os.path.basename(fname)

            # if remote file exists
            try:
                if sftp.stat(remote_file):
                    local_file_data = open(local_file, "rb").read()
                    remote_file_data = sftp.open(remote_file).read()
                    md1 = md5.new(local_file_data).digest()
                    md2 = md5.new(remote_file_data).digest()
                    if md1 == md2:
                        is_up_to_date = True
                        print "UNCHANGED:", os.path.basename(fname)
                    else:
                        print "MODIFIED:", os.path.basename(fname),
            except:
                print "NEW: ", os.path.basename(fname),

            if not is_up_to_date:
                print 'Copying', local_file, 'to ', remote_file
                sftp.put(local_file, remote_file)
                files_copied += 1
    return files_copied


try:
    print 'Establishing SSH connection to:', hostname, port, '...'
    t = paramiko.Transport((hostname, port))
    t.start_client()

    agent_auth(t, username)

    if not t.is_authenticated():
        print 'RSA key auth failed! Trying password login...'
        t.connect(username=username, password=password, hostkey=hostkey)
    else:
        sftp = t.open_session()
    sftp = paramiko.SFTPClient.from_transport(t)

    try:
        sftp.mkdir(dir_remote)
    except IOError, e:
        print '(assuming ', dir_remote, 'exists)', e

    stdout_data = []
    stderr_data = []
    session = t.open_channel(kind='session')
    session.exec_command("python --version")
    while True:
        if session.recv_ready():
            stdout_data.append(session.recv(RECV_BYTES))
        if session.recv_stderr_ready():
            stderr_data.append(session.recv_stderr(RECV_BYTES))
        if session.exit_status_ready():
            break

    print ('exit status: ', session.recv_exit_status())
    print (b''.join(stdout_data))
    print (b''.join(stderr_data))

    t.close()

except Exception, e:
    print '*** Caught exception: %s: %s' % (e.__class__, e)
    try:
        t.close()
    except:
        pass
print '=' * 60
print 'Total files copied:', files_copied
print 'All operations complete!'
print '=' * 60
