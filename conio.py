import sys, time, os, contextlib

def clr_scr():
    sys.stdout.write("\x1b[2J")
    sys.stdout.flush()

black   = 0
red     = 1
green   = 2
yellow  = 3
blue    = 4
magenta = 5
cyan    = 6
white   = 7
bright  = 60

erase_eol = 0
erase_cur = 1
erase_all = 2

def write(row=None, col=None, text=None, bg=None, fg=None, reverse=None, erase=None):
    if row is not None and col is not None:
        sys.stdout.write(f"\x1b[{row+1};{col+1}H")
    if fg is not None:
        sys.stdout.write(f"\x1b[{30+fg}m")
    if bg is not None:
        sys.stdout.write(f"\x1b[{40+bg}m")
    if reverse is not None:
        sys.stdout.write(f"\x1b[7m")
    if text is not None:
        sys.stdout.write(text)
    if reverse is not None:
        sys.stdout.write("\x1b[27m")
    if erase is not None:
        sys.stdout.write(f"\x1b[{erase}K")
    sys.stdout.flush()

if os.name== 'nt':
    from msvcrt import kbhit,getch as _getch
    import ctypes

    @contextlib.contextmanager
    def conio(ansi=True):
        global input_cp
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        input_cp = kernel32.GetConsoleCP()
        try:
            yield
        finally:
            pass

    def wait_keypress(timeout):
        return wait_keypress_until( time.time() + timeout )

    def wait_keypress_until(end_time):
        while time.time() < end_time:
            if kbhit():
                return True
            time.sleep(0.2)
        return False

    keymap =  {
        b'K': 'left',
        b'M': 'right',
        b'H': 'up',
        b'P': 'down',
        b'G': 'home',
        b'O': 'end',
        b'I': 'pgup',
        b'Q': 'pgdn',
        b'R': 'ins',
        b'S': 'del',
        b';': 'f1',
        b'<': 'f2',
        b'=': 'f3',
        b'>': 'f4',
        b'?': 'f5',
        b'@': 'f6',
        b'A': 'f7',
        b'B': 'f8',
        b'C': 'f9',
        b'D': 'f10',
    }
    def getch():
        ch = _getch()
        if ch == b'\x00' or ch == b'\xe0':
            _ch = _getch()
            if _ch in keymap:
                return keymap[_ch]
            return "%x%x" % (ord(ch),ord(_ch))
        return ch.decode(f"cp{input_cp}")

else: # posix
    import termios,select

    @contextlib.contextmanager
    def conio(ansi=True):
        fd = sys.stdin.fileno()
        original_tty_settings = termios.tcgetattr(fd)
        new_term = termios.tcgetattr(fd)
    
        # New terminal setting unbuffered
        new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)
        try:
            yield
        finally:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSAFLUSH, original_tty_settings)

    def kbhit():
        (r, w, e) = select.select([sys.stdin], [], [], 0)
        return sys.stdin in r  # is there input on stdin?

    keymap =  {
        'A': 'up',
        'B': 'down',
        'C': 'right',
        'D': 'left',
        'F': 'end',
        'H': 'home',
        '2': 'ins',
        '3': 'del',
        '5': 'pgup',
        '6': 'pgdn',
        'P': 'f1',
        'Q': 'f2',
        'R': 'f3',
        'S': 'f4',
        '15': 'f5',
        '17': 'f6',
        '18': 'f7',
        '19': 'f8',
        '20': 'f9',
        '21': 'f10',
        '23': 'f11',
        '24': 'f12',
    }
    def getch():
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch = sys.stdin.read(2) # first char is always '[' or 'O'
            ch = ch[1]
            if ch.isdigit():
                while True:
                    _ch = sys.stdin.read(1)
                    if _ch == '~':
                        break
                    ch += _ch
            if ch in keymap:
                return keymap[ch]
            return "1b" + ch
        return ch


    def wait_keypress(timeout):
        (r, w, e) = select.select([sys.stdin], [], [], timeout)
        return sys.stdin in r  # is there input on stdin?

    def wait_keypress_until(end_time):
        timeout = end_time-time.time()
        if timeout <= 0:
            return False
        return wait_keypress(timeout)

if __name__ == "__main__":
    with conio():
        while True:
            if wait_keypress(1):
                key = getch()
                print(key)
                if key=='q':
                    break
            else:
                print('.',end='')
                sys.stdout.flush()
