from scrapy.pipelines.files import FilesPipeline
import os
from scrapy.http import Request
import hashlib
from scrapy.utils.python import to_bytes
import re


class DocumentDownloaderPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        line = super(DocumentDownloaderPipeline,
                     self).file_path(request)
        line = line + '.pdf'
        return re.sub(r'\ |\?|\!|\/|\;|\:|\&', '', line)
