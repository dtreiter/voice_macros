execfile("./ptylib.py") # TODO use proper import
execfile("./config.py") # TODO use proper import
import array
import fcntl
import os
import select
import signal
import sys
import termios
import tty

# The following escape codes are xterm codes.
# See http://rtfm.etla.org/xterm/ctlseq.html for more.
START_ALTERNATE_MODE = set('\x1b[?{0}h'.format(i) for i in ('1049', '47', '1047'))
END_ALTERNATE_MODE = set('\x1b[?{0}l'.format(i) for i in ('1049', '47', '1047'))
ALTERNATE_MODE_FLAGS = tuple(START_ALTERNATE_MODE) + tuple(END_ALTERNATE_MODE)

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

class InputBuffer(object):
    def __init__(self):
        self.text = ""

    def add_char(self, char):
        self.text = self.text + char

    def normalize(self):
        self.text = self.text.lower().strip()

    def clear(self):
        self.text = ""

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
        assert self.master_fd is not None
        master_fd = self.master_fd
        input_mode = "MACRO"
        current_mac_fun = ""
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
                input_buffer.add_char(next_char)
                unformatted_text = input_buffer.text.lower().strip() # just uncapitalizes and removes whitespace
                #sys.stdout.write(next_char)
                #sys.stdout.flush()
                if input_mode is "MACRO":
                    if next_char == "\\":
                        input_buffer.clear()
                    elif next_char == "\r":
                        self.stdin_read(unformatted_text+"\n")
                        input_buffer.clear()
                    elif "configuration" in unformatted_text:
                        execfile("./config.py") # TODO use proper import
                        input_buffer.clear()
                    elif "scratch" in unformatted_text:
                        input_buffer.clear()
                    elif "snore" in unformatted_text:
                        input_mode = "SNORE"
                    elif unformatted_text in MACRO_FUNCTIONS:
                        input_mode = "MACRO_FUNCTION"
                        current_mac_fun = unformatted_text
                        input_buffer.clear()
                    else:
                        # first replace any words which map to something else
                        # then we'll handle plain letters
                        # we'll concatenate everything into processed_command to send to the subshell
                        processed_command = ""
                        commands = input_buffer.text.split(" ")
                        for command in commands:
                            if command.lower() in WORD_MACROS:
                                # TODO possible bug here ie. EGG -> e, but EGG is probably spelt out
                                #      manually my the narrator
                                processed_command = processed_command + WORD_MACROS[command.lower()]
                            elif command == command.upper():
                                # make sure all letters are uppercase! mac's dictation seems to do this
                                # by default so I'm using it as an additional safegaurd
                                processed_command = processed_command + command.lower()
                            else:
                                # throw a dumb error for now.
                                # TODO change this to some useful error once I have a status line
                                processed_command = processed_command
                                break
                        self.stdin_read(processed_command)
                        input_buffer.clear()
                elif input_mode is "MACRO_FUNCTION":
                    self.stdin_read(MACRO_FUNCTIONS[current_mac_fun](input_buffer.text))
                    input_mode = "MACRO"
                    input_buffer.clear()
                elif input_mode is "SNORE":
                    if next_char == "\\":
                        input_mode = "MACRO"
                    else:
                        self.stdin_read(next_char)

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
    input_mode = "MACRO"
    input_buffer = InputBuffer()
    i = Interceptor()
    i.write_stdout('\npty started.\n')
    i.spawn(sys.argv[1:])
    i.write_stdout('\npty terminated.\n')
