import smtplib,sys,os, logging, logging.handlers

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

message_template = """To: {}
From: {}
Subject: Tugas SMTP PROGJAR

Ini tugas progjar buat testing smtp.
"""

class SMTP:
    def __init__(self, server, fromaddr, toaddr, password, port):
        self.server = server
        self.fromaddr = fromaddr
        self.password = password
        self.toaddr = toaddr
        self.port = port
        self.message = message_template.format(self.toaddr, self.fromaddr)
        self.smtp = smtplib.SMTP(self.server, self.port)

    def run(self):
        self.smtp.set_debuglevel(1)
        self.smtp.starttls()
        logging.basicConfig(filename='./smtp_debug.log', level=logging.INFO)
        self.smtp.login(self.fromaddr, self.password)
        self.smtp.sendmail(self.fromaddr, self.toaddr, self.message)
        self.smtp.quit()
    # def flush(self):
    #     try:
    #         self.smtp.set_debuglevel(1)
    #         self.smtp.starttls()
    #         self.smtp.login(self.fromaddr, self.password)
    #         self.smtp.sendmail(self.fromaddr, self.toaddrs, self.message)
    #         self.smtp.quit()
    #     except:
    #         self.handleError(None)  # no particular record


if __name__ == '__main__':
    with open(os.path.join(BASE_DIR, 'smtp.conf')) as config_file:
        config = dict(line.strip().split('=') for line in config_file)

    SERVER = config['server']
    FROMADDR = config['fromaddr']
    TOADDR = config['toaddr']
    PASS = config['pass']
    PORT = config['port']

    smtp = SMTP(SERVER, FROMADDR, TOADDR, PASS, int(PORT))
    smtp.run()

    # logger = logging.getLogger("smtp_logger")
    # logger.setLevel(logging.DEBUG)
    # smtp_handler = SMTP(SERVER, FROMADDR, TOADDR, PASS, int(PORT), 10)
    # logger.addHandler(smtp_handler)
    # smtp_handler.flush()
    # smtp_handler.close()
