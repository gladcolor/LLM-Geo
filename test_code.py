#
# import traceback
#
# code = """
# def test_func():
#     print("Inside test_func.")
#     raise Exception("An error occurred in test_func.")
#     print("Should have an error")
# test_func()
# """
#
# try:
#     print(code)
#     exec(compile(code, '<at runtime>', 'exec'))
# except Exception as e:
#     exc_type, exc_value, exc_traceback = type(e), e, e.__traceback__
#     traceback_details = traceback.extract_tb(exc_traceback)
#
#     filename = traceback_details[-1].filename
#     line_number = traceback_details[-1].lineno
#     function_name = traceback_details[-1].name
#     code_lines = code.split('\n')
#     code_lines = [line for line in code_lines if line.strip() != '']
#
#     print("code lines:", code_lines)
#
#     # line = traceback_details[-1].line
#     line = code_lines[line_number]
#
#     print(f"Exception occurred in file: {filename}")
#     print(f"Line number: {line_number}")
#     print(f"Function that caused the exception: {function_name}")
#     print(f"Exception type: {exc_type.__name__}")
#     print(f"Exception message: {exc_value}")
#     print(f"Line of code that caused the exception: {line}")


code = """
def f1():
    f2()

def f2():
    1 / 0

f1()
"""

a = compile(code, 'Complete program', 'exec')

import sys
import traceback

# try:
#     exec(a)
# except:
#     etype, exc, tb = sys.exc_info()
#     exttb = traceback.extract_tb(tb)
#
#     ## Fill the missing data:
#     exttb2 = [(fn, lnnr, funcname,
#                (code.splitlines()[lnnr-1] if fn=='Solution'
#                 else line))
#               for fn, lnnr, funcname, line in exttb]
#
#     # Print:
#     error_info_str = 'Traceback (most recent call last):\n'
#     # sys.stderr.write('Traceback (most recent call last):\n')
#     for line in traceback.format_list(exttb2[1:]):
#         # sys.stderr.write(line)
#         error_info_str += line
#     for line in traceback.format_exception_only(etype, exc):
#         # sys.stderr.write(line)
#         error_info_str += line
#
#     print(error_info_str)


class LLM_Test():
    def execute_complete_program(self, code: str, try_cnt: int = 1) -> str:
        compiled_code = compile(code, 'Complete program', 'exec')

        count = 0
        while count < try_cnt:
            print(f"\n\n-------------- Running code (trial # {count + 1}/{try_cnt}) --------------\n\n")
            try:
                count += 1
                exec(compiled_code, globals())  # #pass only globals() not locals()
                #!!!!    all variables in code will become global variables! May cause huge issues!     !!!!
                print("\n\n--------------- Done ---------------\n\n")
                return code

            # except SyntaxError as err:
            #     error_class = err.__class__.__name__
            #     detail = err.args[0]
            #     line_number = err.lineno
            #
            except Exception as err:

                cl, exc, tb = sys.exc_info()
                line_number = traceback.extract_tb(tb)[-1][1]

                # print("An error occurred: ", traceback.extract_tb(tb))

                # if count == try_cnt:
                #     print(f"Failed to execute and debug the code within {try_cnt} times.")
                #     return code

                error_info_str = self.get_debug_prompt(exception=err, code=code)
                # print("Sending error information to LLM for debugging...")
                # print("Prompt:\n", debug_prompt)

        return error_info_str


    def get_debug_prompt(self, exception, code):
        etype, exc, tb = sys.exc_info()
        exttb = traceback.extract_tb(tb)

        ## Fill the missing data:
        exttb2 = [(fn, lnnr, funcname,
                   (code.splitlines()[lnnr - 1] if fn == 'Complete program'
                    else line))
                  for fn, lnnr, funcname, line in exttb]

        # Print:
        print(f"traceback.format_exc():\n{traceback.format_exc()}")

        error_info_str = 'Traceback (most recent call last):\n'
        # sys.stderr.write('Traceback (most recent call last):\n')
        for line in traceback.format_list(exttb2[1:]):
            # sys.stderr.write(line)
            error_info_str += line
        for line in traceback.format_exception_only(etype, exc):
            # sys.stderr.write(line)
            error_info_str += line

        # traceback.print_exc()

        # print("error_info_str:", error_info_str)


        return error_info_str


code = """
def f1():
    f2()

def f2():
    1 / 0

f1()
"""


llm = LLM_Test()

error_info_str = llm.execute_complete_program(code=code)

print(f"error_info_str：\n{error_info_str}")