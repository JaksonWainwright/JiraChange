import splunk_syslog_testing

log = splunk_syslog_testing.Syslog('35.194.20.71')


log.send('test2', splunk_syslog_testing.Level.WARNING)