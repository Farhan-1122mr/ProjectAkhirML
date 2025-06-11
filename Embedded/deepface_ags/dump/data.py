class Data:
    def __init__(self, bfile, filesize, filename=None):
        self.filename = filename
        self.file = bfile
        self.filesize = filesize