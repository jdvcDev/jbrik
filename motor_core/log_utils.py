from inspect import currentframe, getframeinfo
import resource.jbrik_config as cfg

def log(arg):
    truncpath = cfg.log["truncpath"]
    print("(" + getframeinfo(currentframe().f_back).filename.replace(truncpath, "") + " "
          + currentframe().f_back.f_lineno.__str__() + "): " + arg.__str__())

