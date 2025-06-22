import logging, sys
def get_logger(name="agent"):
    lg = logging.getLogger(name)
    if lg.handlers:              # 중복 방지
        return lg
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(logging.Formatter(
        "[%(levelname)s] %(asctime)s %(name)s - %(message)s",
        "%Y-%m-%d %H:%M:%S"))
    lg.addHandler(h)
    lg.setLevel(logging.INFO)
    return lg
