import sys
from Network_security.Logging import logging
class NetworkSecurityException(Exception):
    def __init__(self,error_message,system_error:sys):
        __,__,exc_tb= system_error.exc_info()
        self.file_name= exc_tb.tb_frame.f_code.co_filename 
        self.error_message= error_message
        self.system_error= system_error

    def __str__(self):
        return  "Error occured in python script name[{0}] line number [{1}] error message[{2}]".format(self.file_name
                                                                                             ,self.lineno,str(self.error_message))
        

