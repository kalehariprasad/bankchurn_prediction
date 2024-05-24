import os, sys

class CustomException(Exception):
    def __init__(self,error_message:Exception,error_detail:sys):
        self.error_message=CustomException.get_error_details(error_message=error_message
                                                             ,error_detail=error_detail)

    @staticmethod   
    def get_error_details(error_message:Exception,error_detail:sys)->str:
        _,_,exce_tb=error_detail.exc_info()
        exception_block_line_number=exce_tb.tb_frame.f_lineno
        try_block_line_number=exce_tb.tb_lineno
        file_name=exce_tb.tb_frame.f_code.co_filename

        error_message=f"""
                    error occured while executing [{file_name}] at try block[{try_block_line_number}]
                    and exeception block line number [{exception_block_line_number}] 
                    error message is [{error_message}]"""
        
        return error_message
    
    def __str__(self) -> str:
        return self.error_message
    
    def __repr__(self) -> str:
        return CustomException.__name__.str()