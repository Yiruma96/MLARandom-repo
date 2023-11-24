# coding=utf-8
import sys
import logging
import time


class ProgressBar(object):
    DEFAULT_BAR_LENGTH = 50
    DEFAULT_CHAR_ON  = '>'
    DEFAULT_CHAR_OFF = ' '

    def __init__(self, end, start=0, word='', limit=5000):
        time.sleep(0.05)

        if end < limit:
            self.show = False
        else:
            self.show = True
        self.end    = end
        self.start  = start
        self._barLength = self.__class__.DEFAULT_BAR_LENGTH
        self.word = word
        self.setLevel(self.start)
        self._plotted = False

    def setLevel(self, level):
        self._level = level
        if level < self.start:  self._level = self.start
        if level > self.end:    self._level = self.end

        self._ratio = float(self._level - self.start) / float(self.end - self.start)
        self._levelChars = int(self._ratio * self._barLength)

    def plotProgress(self):
        tab = '\t'
        sys.stdout.write("\r%s%s%3i%% [%s%s]" %(
            self.word, tab*5, int(self._ratio * 100.0),
            self.__class__.DEFAULT_CHAR_ON  * int(self._levelChars),
            self.__class__.DEFAULT_CHAR_OFF * int(self._barLength - self._levelChars),
        ))
        sys.stdout.flush()
        self._plotted = True

    def setAndPlot(self, level):
        oldChars = self._levelChars
        self.setLevel(level)
        if (not self._plotted) or (oldChars != self._levelChars):
            self.plotProgress()

    def __add__(self, other):
        if not self.show:
            return self
        assert type(other) in [float, int], "can only add a number"
        self.setAndPlot(self._level + other)
        return self

    def __sub__(self, other):
        return self.__add__(-other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __isub__(self, other):
        return self.__add__(-other)

    def finish(self):
        if self.show: sys.stdout.write("\n")

# http://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
class ColorFormatter(logging.Formatter):
    FORMAT = ("%(asctime)s [%(levelname)-18s] %(message)s "
              "($BOLD%(filename)s$RESET:%(lineno)d)")

    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

    RESET_SEQ = "\033[0m"
    COLOR_SEQ = "\033[1;%dm"
    BOLD_SEQ = "\033[1m"

    COLORS = {
      'WARNING': GREEN,
      'INFO': YELLOW,
      'DEBUG': BLUE,
      'CRITICAL': RED,
      'ERROR': RED
    }

    def formatter_msg(self, msg, use_color = True):
        if use_color:
            msg = msg.replace("$RESET", self.RESET_SEQ).replace("$BOLD", self.BOLD_SEQ)
        else:
            msg = msg.replace("$RESET", "").replace("$BOLD", "")
        return msg

    def __init__(self, use_color=True):
        msg = self.formatter_msg(self.FORMAT, use_color)
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in self.COLORS:
            fore_color = 30 + self.COLORS[levelname]
            levelname_color = self.COLOR_SEQ % fore_color + levelname + self.RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)





def bytes2Str(bytes):
    length = 40

    def formatLength(singleByte):
        return '0' * (2 - len(singleByte)) + singleByte

    temp = ""
    for i in bytes:
        temp += '\\x'+formatLength(str(hex(i))[2:])
    return temp + ' ' * (length - len(temp))










def buildLookupTbl(cntInfo):
    '''
    Build the mapping table
        The location of cntInfo itself represents the index of the parent
        Relax the mappings to contain which child corresponds to which parent
    Example
        cntInfo [2,3] -> {0:0, 1:0, 2:1, 3:1, 4:1}
        The first two children map to the parent index 0,
          and the next three map to the parent index 1
        Say 'cntInfo' contains how many function each object contains;
          The first object has two functions and the second has three.
    :param cntInfo: list()
    :return:
    '''

    lookup_t = dict()
    child_idx = 0
    for parent_idx, child_cnt in enumerate(cntInfo):
        while child_cnt > 0:
            lookup_t[child_idx] = parent_idx
            child_idx += 1
            child_cnt -= 1

    return lookup_t

def getOffsetFrom(targetCnt, sizeLayout):
    '''
    Compute relative addresses from corresponding layout
    Example:
        targetCnt  : [3, 1]                   # num of funcs in each obj
        sizeLayout : [0x60, 0x40, 0x20, 0x20] # sizes of each func
        offsetsFrom: [0x0, 0x60, 0xa0, 0xc0]  # returns func offsets from the objs
    :param targetCnt:
    :param sizeLayout:
    :return:
    '''

    offsetsFrom = list()
    assert sum(targetCnt) == len(sizeLayout), "Size does NOT match!"

    layoutIdx = 0
    for tc in targetCnt:
        for targetIdx in range(tc):
            # The beginning offset from the layout
            if targetIdx == 0:
                offsetsFrom.append(0x0)
            # The offset has to be the sum of the previous object sizes
            else:
                offsetsFrom.append(offsetsFrom[-1] + sizeLayout[layoutIdx - 1])
            layoutIdx += 1

    return offsetsFrom

def getOffset(sizeLayout):
    '''
    假设所有的object是顺序连接的
    '''

    offset = [0x0]
    for i in range(1, len(sizeLayout)):
        offset.append(offset[-1] + sizeLayout[i-1])
    return offset

def computeRelaOffset(offset, relaOffset):
    ''' Return relative offsets from the given offset '''
    return [x + relaOffset for x in offset]

def toSigned32(n):
    ''' Return a 32-bit signed number for n '''
    n = n & 0xffffffff
    return n | (-(n & 0x80000000))

def hexPrint(target):
    ''' Help the output with a simple hex format '''
    return [hex(x) for x in target]

def toHex(val, bits=32):
    ''' Help the output for the two's complement representation '''
    return hex((val + (1 << bits)) % (1 << bits))

def _show_elapsed(start, end):
    elapsed = end - start
    time_format = ''
    if elapsed > 86400:
        time_format += str(int(elapsed // 86400)) + ' day(s) '
        elapsed = elapsed % 86400
    if elapsed > 3600:
        time_format += str(int(elapsed // 3600)) + ' hour(s) '
        elapsed = elapsed % 3600
    if elapsed > 60:
        time_format += str(int(elapsed // 60)) + ' min(s) '
        elapsed = elapsed % 60
    time_format += str(round(elapsed, 3)) + ' sec(s)'
    return time_format
