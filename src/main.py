from logger import Logger, LogLevel

def main():
    log = Logger("MyLogger")
    log.set_toggle_file_logging(True)
    log.set_toggle_db_logging(True)

    log.error("Testing Error Message Logging to Console")
    log.warning("Testing Warning Message Logging to Console")
    log.success("Testing Success Message Logging to Console %d" % 6)
    log.information("Testing Information Message Logging to Console")
    log.debug("Testing Debug Message Logging to Console")
    log.trace("Testing Trace Message Logging to Console")

    log.set_log_level(LogLevel.LOW)

    log.fatal("Testing Fatal Message Logging to Console")
    log.error("Testing Error Message Logging to Console")
    log.warning("Testing Warning Message Logging to Console")
    log.success("Testing Success Message Logging to Console %d" % 6)
    log.information("Testing Information Message Logging to Console")
    log.debug("Testing Debug Message Logging to Console")
    log.trace("Testing Trace Message Logging to Console")

    log2 = Logger("Logger Two")
    log2.set_toggle_file_logging(True)
    log2.set_toggle_db_logging(True)
    log2.fatal("Testing Fatal Message Logging to Console")
    log2.error("Testing Error Message Logging to Console")
    log2.warning("Testing Warning Message Logging to Console")
    log2.success("Testing Success Message Logging to Console %d" % 6)
    log2.information("Testing Information Message Logging to Console")
    log2.debug("Testing Debug Message Logging to Console")
    log2.trace("Testing Trace Message Logging to Console")

if __name__ == "__main__":
    main()