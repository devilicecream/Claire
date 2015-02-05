#!/usr/bin/env python
__author__ = 'walter'

import smtplib
from claire.reporter import Reporter
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailReporter(Reporter):
    def __init__(self, config):
        self.smtp_username = config.get_or_none('reporter', 'smtp_username')
        self.smtp_password = config.get_or_none('reporter', 'smtp_password')
        self.smtp_host = config.get_or_none('reporter', 'smtp_host')
        self.smtp_port = config.get_or_none('reporter', 'smtp_port')
        self.smtp_tls_enabled = config.get_or_none('reporter', 'smtp_tls_enabled', func_name='getboolean')
        self.email = config.get_or_none('reporter', 'email')
        self.report = config.get_or_none('reporter', 'report')

    def report_process(self, process, server):
        if not self.report or self.report == 'process':
            self.send_email("Process %s DOWN" % process.name,
                            "Process %s is down on %s" % (process.name, server.hostname),
                            process.__repr__())

    def report_server(self, server):
        if not self.report or self.report == 'server':
            self.send_email("Server UNREACHABLE",
                            "Server %s is unreachable" % server.hostname,
                            server.__repr__())

    def send_email(self, subject, title, body):
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.smtp_username
        msg['To'] = self.email

        text = "%s\n%s" % (title, body)
        html = """\
        <html>
          <head></head>
          <body>
            <h1>%s</h1>
            <p>
               %s
            </p>
          </body>
        </html>
        """ % (title, body.replace("\n", "<br/>").replace("\t", "----"))

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)

        if self.smtp_port:
            s = smtplib.SMTP(self.smtp_host, port=self.smtp_port)
        else:
            s = smtplib.SMTP(self.smtp_host)
        s.ehlo()
        if self.smtp_tls_enabled:
            s.starttls()
        if self.smtp_username and self.smtp_password:
            s.login(self.smtp_username, self.smtp_password)
        s.sendmail(self.smtp_username, self.email, msg.as_string())
        s.quit()