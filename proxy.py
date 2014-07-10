"""Pseudo terminal utilities."""

# Bugs: No signal handling.  Doesn't set slave termios and window size.
#       Only tested on Linux.
# See:  W. Richard Stevens. 1992.  Advanced Programming in the
#       UNIX Environment.  Chapter 19.
# Author: Steen Lumholt -- with additions by Guido.

from select import select
import os
import tty

__all__ = ["openpty","fork","spawn"]

STDIN_FILENO = 0
STDOUT_FILENO = 1
STDERR_FILENO = 2

CHILD = 0

def openpty():
    """openpty() -> (master_fd, slave_fd)
    Open a pty master/slave pair, using os.openpty() if possible."""

    try:
        return os.openpty()
    except (AttributeError, OSError):
        pass
    master_fd, slave_name = _open_terminal()
    slave_fd = slave_open(slave_name)
    return master_fd, slave_fd

def master_open():
    """master_open() -> (master_fd, slave_name)
    Open a pty master and return the fd, and the filename of the slave end.
    Deprecated, use openpty() instead."""

    try:
        master_fd, slave_fd = os.openpty()
    except (AttributeError, OSError):
        pass
    else:
        slave_name = os.ttyname(slave_fd)
        os.close(slave_fd)
        return master_fd, slave_name

    return _open_terminal()

def _open_terminal():
    """Open pty master and return (master_fd, tty_name).
    SGI and generic BSD version, for when openpty() fails."""
    try:
        import sgi
    except ImportError:
        pass
    else:
        try:
            tty_name, master_fd = sgi._getpty(os.O_RDWR, 0o666, 0)
        except IOError as msg:
            raise os.error(msg)
        return master_fd, tty_name
    for x in 'pqrstuvwxyzPQRST':
        for y in '0123456789abcdef':
            pty_name = '/dev/pty' + x + y
            try:
                fd = os.open(pty_name, os.O_RDWR)
            except os.error:
                continue
            return (fd, '/dev/tty' + x + y)
    raise os.error('out of pty devices')

def slave_open(tty_name):
    """slave_open(tty_name) -> slave_fd
    Open the pty slave and acquire the controlling terminal, returning
    opened filedescriptor.
    Deprecated, use openpty() instead."""

    result = os.open(tty_name, os.O_RDWR)
    try:
        from fcntl import ioctl, I_PUSH
    except ImportError:
        return result
    try:
        ioctl(result, I_PUSH, "ptem")
        ioctl(result, I_PUSH, "ldterm")
    except IOError:
        pass
    return result

def fork():
    """fork() -> (pid, master_fd)
    Fork and make the child a session leader with a controlling terminal."""

    try:
        pid, fd = os.forkpty()
    except (AttributeError, OSError):
        pass
    else:
        if pid == CHILD:
            try:
                os.setsid()
            except OSError:
                # os.forkpty() already set us session leader
                pass
        return pid, fd

    master_fd, slave_fd = openpty()
    pid = os.fork()
    if pid == CHILD:
        # Establish a new session.
        os.setsid()
        os.close(master_fd)

        # Slave becomes stdin/stdout/stderr of child.
        os.dup2(slave_fd, STDIN_FILENO)
        os.dup2(slave_fd, STDOUT_FILENO)
        os.dup2(slave_fd, STDERR_FILENO)
        if (slave_fd > STDERR_FILENO):
            os.close (slave_fd)

        # Explicitly open the tty to make it become a controlling tty.
        tmp_fd = os.open(os.ttyname(STDOUT_FILENO), os.O_RDWR)
        os.close(tmp_fd)
    else:
        os.close(slave_fd)

    # Parent and child process.
    return pid, master_fd

def _writen(fd, data):
    """Write all the data to a descriptor."""
    while data:
        n = os.write(fd, data)
        data = data[n:]

def _read(fd):
    """Default read function."""
    return os.read(fd, 1024)

def _copy(master_fd, master_read=_read, stdin_read=_read):
    """Parent copy loop.
    Copies
            pty master -> standard output   (master_read)
            standard input -> pty master    (stdin_read)"""
    while 1:
        rfds, wfds, xfds = select(
                [master_fd, STDIN_FILENO], [], [])
        if master_fd in rfds:
            data = master_read(master_fd)
            os.write(STDOUT_FILENO, data)
        if STDIN_FILENO in rfds:
            data = stdin_read(STDIN_FILENO)
            _writen(master_fd, data)

def spawn(argv, master_read=_read, stdin_read=_read):
    """Create a spawned process."""
    if type(argv) == type(''):
        argv = (argv,)
    pid, master_fd = fork()
    if pid == CHILD:
        os.execlp(argv[0], *argv)
    try:
        mode = tty.tcgetattr(STDIN_FILENO)
        tty.setraw(STDIN_FILENO)
        restore = 1
    except tty.error:    # This is the same as termios.error
        restore = 0
    try:
        _copy(master_fd, master_read, stdin_read)
    except (IOError, OSError):
        if restore:
            tty.tcsetattr(STDIN_FILENO, tty.TCSAFLUSH, mode)

    os.close(master_fd)



import array
import fcntl
import os
import select
import signal
import sys
import termios
import tty
import yaml

# The following escape codes are xterm codes.
# See http://rtfm.etla.org/xterm/ctlseq.html for more.
START_ALTERNATE_MODE = set('\x1b[?{0}h'.format(i) for i in ('1049', '47', '1047'))
END_ALTERNATE_MODE = set('\x1b[?{0}l'.format(i) for i in ('1049', '47', '1047'))
ALTERNATE_MODE_FLAGS = tuple(START_ALTERNATE_MODE) + tuple(END_ALTERNATE_MODE)
MACROS = {}

with open('config.yaml') as data_file:
    MACROS = yaml.load(data_file)

def findlast(s, substrs):
    '''
    Finds whichever of the given substrings occurs last in the given string and returns that substring, or returns None if no such strings occur.
    '''
    i = -1
    result = None
    for substr in substrs:
        pos = s.rfind(substr)
        if pos > i:
            i = pos
            result = substr
    return result

class Interceptor(object):
    '''
    This class does the actual work of the pseudo terminal. The spawn() function is the main entrypoint.
    '''

    def __init__(self):
        self.master_fd = None

    def spawn(self, argv=None):
        '''
        Create a spawned process.
        Based on the code for spawn().
        '''
        assert self.master_fd is None
        if not argv:
            argv = [os.environ['SHELL']]

        pid, master_fd = fork()
        self.master_fd = master_fd
        if pid == CHILD:
            os.execlp(argv[0], *argv)

        old_handler = signal.signal(signal.SIGWINCH, self._signal_winch)
        try:
            mode = tty.tcgetattr(STDIN_FILENO)
            tty.setraw(STDIN_FILENO)
            restore = 1
        except tty.error:    # This is the same as termios.error
            restore = 0
        self._init_fd()
        try:
            self._copy()
        except (IOError, OSError):
            if restore:
                tty.tcsetattr(STDIN_FILENO, tty.TCSAFLUSH, mode)

        os.close(master_fd)
        self.master_fd = None
        signal.signal(signal.SIGWINCH, old_handler)

    def _init_fd(self):
        '''
        Called once when the pty is first set up.
        '''
        self._set_pty_size()

    def _signal_winch(self, signum, frame):
        '''
        Signal handler for SIGWINCH - window size has changed.
        '''
        self._set_pty_size()

    def _set_pty_size(self):
        '''
        Sets the window size of the child pty based on the window size of our own controlling terminal.
        '''
        assert self.master_fd is not None

        # Get the terminal size of the real terminal, set it on the pseudoterminal.
        buf = array.array('h', [0, 0, 0, 0])
        fcntl.ioctl(STDOUT_FILENO, termios.TIOCGWINSZ, buf, True)
        fcntl.ioctl(self.master_fd, termios.TIOCSWINSZ, buf)

    def _copy(self):
        '''
        Main select loop. Passes all data to self.master_read() or self.stdin_read().
        '''
        user_data = ""
        assert self.master_fd is not None
        master_fd = self.master_fd
        while 1:
            try:
                rfds, wfds, xfds = select.select([master_fd, STDIN_FILENO], [], [])
            except select.error as e:
                if e[0] == 4:   # Interrupted system call.
                    continue

            if master_fd in rfds:
                data = os.read(self.master_fd, 1024)
                self.master_read(data)
            if STDIN_FILENO in rfds:
                next_char = os.read(STDIN_FILENO, 1024)
                user_data = user_data + next_char
                user_data = user_data.lower()
                #sys.stdout.write(next_char)
                #sys.stdout.flush()
                if next_char == "\\":
                    user_data = ""
                elif next_char == "\r":
                    self.stdin_read(user_data+"\n")
                    user_data = ""
                if user_data in MACROS:
                    self.stdin_read(MACROS[user_data])
                    user_data = ""

    def write_stdout(self, data):
        '''
        Writes to stdout as if the child process had written the data.
        '''
        os.write(STDOUT_FILENO, data)

    def write_master(self, data):
        '''
        Writes to the child process from its controlling terminal.
        '''
        master_fd = self.master_fd
        assert master_fd is not None
        while data != '':
            n = os.write(master_fd, data)
            data = data[n:]

    def master_read(self, data):
        '''
        Called when there is data to be sent from the child process back to the user.
        '''
        flag = findlast(data, ALTERNATE_MODE_FLAGS)
        if flag is not None:
            if flag in START_ALTERNATE_MODE:
                # This code is executed when the child process switches the terminal into alternate mode. The line below assumes that the user has opened vim, and writes a message.
                self.write_master('')
            elif flag in END_ALTERNATE_MODE:
                # This code is executed when the child process switches the terminal back out of alternate mode. The line below assumes that the user has returned to the command prompt.
                self.write_master('')
        self.write_stdout(data)

    def stdin_read(self, data):
        '''
        Called when there is data to be sent from the user/controlling terminal down to the child process.
        '''
        self.write_master(data)

if __name__ == '__main__':
    i = Interceptor()
    i.write_stdout('\npty started.\n')
    i.spawn(sys.argv[1:])
    i.write_stdout('\npty terminated.\n')
