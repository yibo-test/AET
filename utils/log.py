import os
import logging
import time


from logging.handlers import RotatingFileHandler


def log(log_level="DEBUG"):
    # 创建logger，如果参数为空则返回root logger
    logger = logging.getLogger()

    # 设置logger日志等级
    # logger.setLevel(logging.DEBUG)
    logger.setLevel(log_level)

    # 创建handler
    log_size = 1024 * 1024 * 20
    # 将日志写入到文件中
    dir_name = "./logs/"
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    time_str = time.strftime("%Y%m%d", time.localtime())
    fh = RotatingFileHandler(dir_name + f"{time_str}.log", encoding="utf-8", maxBytes=log_size, backupCount=100)
    # 将日志输出到控制台
    ch = logging.StreamHandler()

    # 设置输出日志格式
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(filename)s line:%(lineno)s  %(message)s",
        # datefmt="%Y/%m/%d %X"
    )
    # 注意 logging.Formatter的大小写

    # 为handler指定输出格式，注意大小写
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 为logger添加的日志处理器
    logger.addHandler(fh)
    logger.addHandler(ch)


if __name__ == '__main__':
    log("INFO")
    logging.debug("debug日志")
    logging.info("info日志")
    logging.warning("warning日志")