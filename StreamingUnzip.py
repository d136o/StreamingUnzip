import argparse
import io
import sys
import zipfile

class _ZipDataStream_(io.IOBase):

    def __init__(self, stream):
        self.offset = 0
        self.stream = stream
        
    def _consume_(self, n=0):
        
        while n > 0:
            consumed = len(self.stream.read(n))
            self.offset = self.offset + consumed
            n = n - consumed
        return
        
    def read(self, n=1):
        b = self.stream.read(n)
        self.offset = self.offset + len(b)
        return b
        
    def seek(self, offset, whence=0):

        if offset < self.offset:
            raise IOError("Can't seek to position before currernt")
        
        else:
            self._consume_(offset-self.offset)
            return
        
    def seekable(self):
        return False

    def tell(self):
        return self.offset

    def write(self, b):
        raise io.UnsupportedOperation


class StreamingUnzipFile(zipfile.ZipFile):
    """We extract the central directory from centralDirFile, then use it
    to parse the inputStream, it is output to outputStream.
    """
    
    def __init__(self, centralDirFile, centralDirFileOffset, inputStream, outputStream):
        
        super(StreamingUnzipFile, self).__init__(centralDirFile)
        
        if not isinstance(centralDirFile, basestring):
            centralDirFile.close()
        
        self.fp = _ZipDataStream_(inputStream)
        self._filePassed = 1
        self._consumed_all_entries = False
        self._outputStream = outputStream
                
        #fix offset in each of the zip file entries
        for info in self.infolist():
            info.header_offset = info.header_offset + centralDirFileOffset
            

    def generateFileStreams(self):
        '''Generates file like objects for each of the entries in this
        streaming zip file. 
        '''
        if not self._consumed_all_entries:
            for info in self.infolist():
                yield self.open(info)
        self._consumed_all_entries = True

    def streamOut(self):
        for f in self.generateFileStreams():
            for l in f:
                sys.stdout.write(l)
        self._outputStream.flush()

def main(argv=None):
    
    if argv is None:
        argv = sys.argv
        
    parser = argparse.ArgumentParser()
    parser.add_argument('centralDirFile',
                        help='The file from which the zip\'s central directory will be read')
    parser.add_argument('centralDirFileOffset',
                        help='The centralDirectoryFile\s offset withing the actual zip archive',
                        type=int)

    args = parser.parse_args(argv[1:])

    suz = StreamingUnzipFile(args.centralDirFile,
                             args.centralDirFileOffset,
                             sys.stdin,
                             sys.stdout)

    suz.streamOut()



if __name__=='__main__':
    sys.exit(main())

