# Jira Automation Flask Application

This application is to sit in between Jira Software, and any other automation platforms that would be used in correlation with Jira.

## Setup

You need to create a config file (.py) to pull variables from regarding credentials. The filename needs to be: secure_conf.py

it needs to contain the following variables,  with your user specific values.

```bash
jira_username = 'service_account'
jira_api_token = 'service_password'
```

## Workflow

The first thing that Jira should hit is the /validate route. This will, based on the ticket type, run validation on any fields that need to be validated in order to perform automation. The application will then post back to Jira stating whether or not the validation has passed.

The second thing that Jira should hit, is the /trigger_method route. This will route to the correlating collections of methods to trigger or perform the automation related with the ticket type. This is where we will handle result posting of automation back to Jira.



## Contributing
To add an automation task to this application, the following pieces must be in place:

### Jira
Jira must have custom fields, and workflows in place.

### Flask
The following things need to be added into the flask application to perform the automation:

Validation methods:
In general, if you need to split your field validation into multiple methods, you should have a "parent" method that will contain a list of the results that your "Child" methods will return. Pass that list back to the main validate method.

Example:
##### Child Methods to validate IP address formatting from a custom field:

```python
    def validate_ip_network(self):
        ip_data = self.ip_address.replace(" ", "/").replace("\r", "").replace("//", "/").split('\n')
        for ip_address in ip_data:
            try:
                ip_network_check = ipaddress.ip_network(ip_address)
            except Exception as errmsg:
                self.add_errmsg_comment(errmsg)
                return conf.validation_failure
        return conf.validation_success

    # Validate IP child tasks / Try to check and see if an IP is global. if global, then pass, if not, throw error
    # and pass comment to Jira.
    def validate_ip_global(self):
        ip_data = self.ip_address.replace(" ", "/").replace("\r", "").replace("//", "/").split('\n')
        for ip in ip_data:
            try:
                ip_network_check = ipaddress.ip_network(ip)
                ip_is_global = ip_network_check.is_global
                if not ip_is_global:
                    self.add_errmsg_comment(f'{ip} is a private IP address')
                    return conf.validation_failure
            except Exception as errmsg:
                self.add_errmsg_comment(errmsg)
                return conf.validation_failure
        return conf.validation_success
```

##### Parent method to validate child methods and return a success or failure
```python
    def validate_ip_grammar(self):
        validation_result_list = [self.validate_ip_network(), self.validate_ip_global()]
        if conf.validation_failure in validation_result_list:
            return conf.validation_failure
        else:
            return conf.validation_success
```
See how the child functions for validation are called in the validation_result_list? Make sure your validation passes back a failure or success. You can then use this in the validation mapper as pictured below:

```python
    def validate_customfields(self):
        customfield_validation_mapper = {
            'IP-Whitelist': self.validate_ip_grammar()
        }
        self.validation_results.append(customfield_validation_mapper.get(self.issue_type))
        print(self.validation_results)
        return self.validation_results
```

This same concept is followed for the methods route. 
