import Syslog_Client
#File to contain basic information for ease of access

validation_failure = 'Validation has failed. '
validation_success = 'Validation Succeeded'
jiraFQDN = 'https://team-1584999324424.atlassian.net'
avx_fqdn = 'Https://appviewx.pd.gp'
splunk_server = '35.194.20.71'

log = Syslog_Client.Syslog('35.194.20.71')


def send_syslog(msg):
    log.send(msg, splunk_syslog_testing.Level.NOTICE)
