import glob
import inspect
import sys
import unittest
import pathlib
import getopt

sys.path.append('..')


def run_filters(suit, case):
    """
    约束：
    用例模块文件名以"test_"开始
    用例函数名以"test_"开始
    """
    if case.startswith('test_'):
        return
    suites = unittest.TestSuite()
    is_find = True
    for module in glob.glob('test*.py'):
        module_name = pathlib.Path(module).stem
        classes = inspect.getmembers(__import__(module_name), inspect.isclass)
        for name, cls in classes:
            if name == suit and getattr(cls, case) is not None:
                suites.addTest(cls(case))
                is_find = False
        if not is_find:
            break
    unittest.TextTestRunner().run(suites)


def run_all():
    suites = unittest.TestSuite()
    tests = unittest.defaultTestLoader.discover('.', pattern='test*.py')
    suites.addTest(tests)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suites)


def show_all():
    print("== all testcase info ==")
    for module in glob.glob('test*.py'):
        module_name = pathlib.Path(module).stem
        classes = inspect.getmembers(__import__(module_name), inspect.isclass)
        for cls_name, cls in classes:
            if issubclass(cls, unittest.TestCase):
                print('%s:' % cls_name)
                functions = inspect.getmembers(cls, inspect.isfunction)
                for func_name, func in functions:
                    if func_name.startswith('test_'):
                        print('    %s' % func_name)


def show_help():
    print('-f, --filters=  : filter test case, format[testsuit:testcase]')
    print('-a, --all       : show all test case')
    print('-h, --help      : show help info')


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], '-f:-h-a', ['filters=', 'help', 'all'])
    except Exception:
        show_help()
        sys.exit(0)
    if (len(opts)) == 0:
        show_help()
    for opt_key, opt_value in opts:
        if opt_key in ('-f', '--filters'):
            if opt_value == '*':
                run_all()
            else:
                filters = opt_value.strip().split('.')
                if len(filters) == 2:
                    run_filters(*filters)
                else:
                    show_help()
        elif opt_key in ('-a', '--all'):
            show_all()
        else:
            show_help()
