import sys
from Network_security.Logging import logging
class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message= error_message
        __,__,exe_tb=error_details.exc_info()
        self.lineno=exe_tb.tb_lineno
        self.file_name=exe_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return  "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format
        self.file_name, self.lineno, str(self.error_message)
        

