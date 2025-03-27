
说明文档

一、项目概述
此项目是一个自动化测试框架，用于执行一系列的测试用例，并且支持并行和串行执行模式。它能够读取配置文件（如测试用例文件、测试床文件、测试集文件），执行测试用例，记录日志，并在测试前后执行钩子脚本

二、文件说明
autos.py

1.功能：作为测试框架的主文件，负责读取配置文件，解析测试用例，根据执行模式（并行或串行）执行测试用例，记录日志，并在测试前后执行钩子脚本。
2.主要函数：
    1.setup_logging(log_path)：设置日志记录，将日志信息保存到指定的文件中。
    2.parse_testcase_xml(testcase_xml)：解析测试用例文件，获取测试用例的脚本路径、参数，以及整个测试用例集的执行模式（并行或串行）和相关参数（并行数量或串行等待时间）。
    3.parse_testbed_xml(testbed_xml)：解析测试床文件，获取测试所需的设备信息，如服务器和存储设备的 IP、协议、用户名和密码。
    4.parse_testset_xml(testset_xml)：解析测试集文件，获取日志路径、钩子脚本路径、钩子参数和测试用例文件路径。
    5.run_test_case(script_path, params, testbed)：执行单个测试用例，包括执行测试用例脚本中的 pretest、testprocedure 和 aftertest 函数。
    6.run_hook(hook_script_path, hook_params, test_results, stage)：执行钩子脚本，支持在所有测试用例执行前和执行后执行钩子函数。
    7.main()：程序的入口函数，负责读取命令行参数，调用上述函数完成测试用例的执行和日志记录。

testcase1.py 和 testcase2.py

    1.功能：示例测试用例文件，包含 pretest、testprocedure 和 aftertest 函数，分别用于测试用例的前置处理、测试过程和后置处理。

testcase.xml

    1.功能：配置测试用例的文件，包含每个测试用例的脚本路径、参数，以及整个测试用例集的执行模式（并行或串行）和相关参数（并行数量或串行等待时间）。

testbed.xml

    1.功能：配置测试床的文件，包含测试所需的设备信息，如服务器和存储设备的 IP、协议、用户名和密码。

testset.xml

    1.功能：配置测试集的文件，包含日志路径、钩子脚本路径、钩子参数和测试用例文件路径。

hook.py

    1.功能：钩子脚本文件，包含 before_all 和 after_all 函数，分别在所有测试用例执行前和执行后被调用。

device.py
    1.功能：定义设备类的文件，包含 Device 基类和 Server、Storage 子类，用于封装设备的连接和操作方法。

test_autos.py
    1.功能：对 autos.py 中的函数进行单元测试的文件，确保各个函数的功能正常

三、执行流程
  1.运行 autos.py 脚本，通过命令行参数指定测试用例文件、测试床文件和测试集文件。
  2.autos.py 读取测试集文件，获取日志路径、钩子脚本路径、钩子参数和测试用例文件路径。
  3.设置日志记录，调用 setup_logging 函数。
  4.执行钩子脚本的 before_all 函数，调用 run_hook 函数。
  5.解析测试用例文件，获取测试用例的脚本路径、参数，以及执行模式和相关参数，调用 parse_testcase_xml 函数。
  6.解析测试床文件，获取测试所需的设备信息，调用 parse_testbed_xml 函数。
  7.根据执行模式（并行或串行）执行测试用例：
    1.并行执行：使用 ThreadPoolExecutor 并行执行测试用例，调用 run_test_case 函数。
    2.串行执行：按顺序执行测试用例，每个测试用例执行完后等待指定的时间，调用 run_test_case 函数。
  8.执行钩子脚本的 after_all 函数，调用 run_hook 函数。
  9.输出测试结果，包括通过的测试用例数量和失败的测试用例数量。
  
四、架构逻辑图

<img width="415" alt="image" src="https://github.com/user-attachments/assets/78fcd7a8-0510-4d37-afc4-ffd8d5d7a1fc" />


这个架构逻辑图展示了整个测试框架的执行流程，从启动 autos.py 脚本开始，经过读取配置文件、执行钩子脚本、解析测试用例和测试床文件，根据执行模式执行测试用例，最后输出测试结果。
