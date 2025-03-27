import xml.etree.ElementTree as ET
import os
import importlib
import importlib.util
import traceback
import logging
from concurrent.futures import ThreadPoolExecutor
import time


def setup_logging(log_path):
    logging.basicConfig(filename=log_path, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')


def parse_testcase_xml(testcase_xml):
    tree = ET.parse(testcase_xml)
    root = tree.getroot()
    test_cases = []
    for test_case in root.findall('testcase'):
        script_path = test_case.find('script_path').text
        params = {}
        for param in test_case.findall('params/param'):
            name = param.get('name')
            value = param.text
            params[name] = value
        test_cases.append((script_path, params))
    execution_mode = root.find('execution_mode').text
    if execution_mode == 'parallel':
        parallel_count = int(root.find('parallel_count').text)
    elif execution_mode == 'serial':
        wait_time = float(root.find('wait_time').text)
    return test_cases, execution_mode, parallel_count if execution_mode == 'parallel' else wait_time


def parse_testbed_xml(testbed_xml):
    from device import Server, Storage
    tree = ET.parse(testbed_xml)
    root = tree.getroot()
    testbed = {}
    for device in root.findall('device'):
        device_type = device.get('type')
        ip = device.find('ip').text
        protocol = device.find('protocol').text
        username = device.find('username').text
        password = device.find('password').text
        if device_type == 'server':
            testbed[device_type] = Server(ip, protocol, username, password)
        elif device_type == 'storage':
            testbed[device_type] = Storage(ip, protocol, username, password)
    return testbed


def parse_testset_xml(testset_xml):
    tree = ET.parse(testset_xml)
    root = tree.getroot()
    log_path = root.find('log_path').text
    testcase_file_elem = root.find('testcase_file')
    testcase_file = testcase_file_elem.text if testcase_file_elem is not None else None
    return log_path, None, None, testcase_file


def run_test_case(script_path, params, testbed):
    try:
        module_name = os.path.splitext(os.path.basename(script_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # 执行 pretest
        if hasattr(module, 'pretest'):
            module.pretest(params, testbed)

        # 执行 testprocedure
        if hasattr(module, 'testprocedure'):
            module.testprocedure(params, testbed)

        # 执行 aftertest
        if hasattr(module, 'aftertest'):
            module.aftertest(params, testbed)

        logging.info(f"Test case {script_path} passed.")
        return True, f"Test case {script_path} passed."
    except Exception as e:
        logging.error(f"Test case {script_path} failed: {str(e)}")
        logging.error(traceback.format_exc())
        return False, f"Test case {script_path} failed: {str(e)}"


def run_hook(hook_script_path, hook_params, test_results, stage):
    if hook_script_path:
        try:
            module_name = os.path.splitext(os.path.basename(hook_script_path))[0]
            spec = importlib.util.spec_from_file_location(module_name, hook_script_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if stage == 'before_all':
                if hasattr(module, 'before_all'):
                    module.before_all(hook_params)
            elif stage == 'after_all':
                if hasattr(module, 'after_all'):
                    module.after_all(test_results, hook_params)
        except Exception as e:
            logging.error(f"Hook script {hook_script_path} failed at {stage}: {str(e)}")


def main():
    import sys
    if len(sys.argv) != 7 or sys.argv[1] != '-tc' or sys.argv[3] != '-tb' or sys.argv[5] != '-ts':
        print("Usage: autos.py -tc testcase.xml -tb testbed.xml -ts testset.xml")
        sys.exit(1)

    testcase_xml = sys.argv[2]
    testbed_xml = sys.argv[4]
    testset_xml = sys.argv[6]

    log_path, hook_script_path, hook_params, testcase_file = parse_testset_xml(testset_xml)
    if testcase_file:
        testcase_xml = testcase_file
    setup_logging(log_path)

    run_hook(hook_script_path, hook_params, [], 'before_all')

    test_cases, execution_mode, param = parse_testcase_xml(testcase_xml)
    testbed = parse_testbed_xml(testbed_xml)

    test_results = []
    passed = 0
    failed = 0

    if execution_mode == 'parallel':
        with ThreadPoolExecutor(max_workers=param) as executor:
            futures = [executor.submit(run_test_case, script_path, params, testbed) for script_path, params in
                       test_cases]
            for future in futures:
                script_path, params = next(
                    (t for t in test_cases if future == executor.submit(run_test_case, t[0], t[1], testbed)),
                    (None, None))
                result, message = future.result()
                test_results.append({'script_path': script_path, 'result': result, 'message': message})
                if result:
                    passed += 1
                else:
                    failed += 1
    elif execution_mode == 'serial':
        for script_path, params in test_cases:
            result, message = run_test_case(script_path, params, testbed)
            test_results.append({'script_path': script_path, 'result': result, 'message': message})
            if result:
                passed += 1
            else:
                failed += 1
            time.sleep(param)

    run_hook(hook_script_path, hook_params, test_results, 'after_all')

    print(f"Tests passed: {passed}, Tests failed: {failed}")


if __name__ == "__main__":
    main()
