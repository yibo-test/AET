import time
import os
from BeautifulReport import BeautifulReport


class Report(BeautifulReport):

    def generate_report(self, description, filename: str = None, report_dir='./report/', log_path=None, theme='theme_default'):
        if filename is None:
            time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
            filename = f"report_{time_str}"

        if report_dir == "./report/":
            if not os.path.exists(report_dir):
                os.mkdir(report_dir)

        self.report(description, filename, report_dir, log_path, theme)
