from clearpath_config.system.system import HostsConfig, Host

INVALID_HOSTNAMES = [
    "space in hostname",
    "underscore_in_hostname",
    "-start-hypens-end-",
    "trailing.period.",
    "exceedingly----------long----------names-----------\
        which----------are----------longer----------than----------\
        two----------hundred----------and----------fifty----------\
        three----------ASCII----------characters----------are----------\
        not-----------allowed----------as----------hostnames",
]

VALID_HOSTNAMES = ["cpr-x999-9999", "cpr-proj01"]

INVALID_IP = [
    "regular.string",
    "0.X.0.0",  # non integer field
    "255.0.0",  # too few fields
    "255.0.0.0.0",  # too many fields
    "0.0.256.0",  # field wider than 8 bits
]

VALID_IP = ["192.168.131.1"]


class TestHostsConfig:
    hosts = HostsConfig()

    def test_platform(self):
        errors = []
        # Invalid Inputs
        for hostname in INVALID_HOSTNAMES:
            try:
                self.hosts.set_platform_hostname(hostname)
            except AssertionError:
                pass  # Do nothing, failure is expected
            else:
                errors.append("Invalid Hostname %s was incorrectly accepted" % hostname)
        for ip in INVALID_IP:
            try:
                self.hosts.set_platform_ip(ip)
            except AssertionError:
                pass  # Do nothing, failure is expected
            else:
                errors.append("Invalid IP '%s' was incorrectly accepted" % ip)
        # Valid Inputs
        for hostname in VALID_HOSTNAMES:
            try:
                self.hosts.set_platform_hostname(hostname)
            except AssertionError as e:
                errors.append(
                    "Valid Hostname %s was incorrectly rejected with following message:\n\t%s"
                    % (hostname, e.args[0])
                )
            if hostname != self.hosts.get_platform_hostname():
                errors.append(
                    "Valid Hostname %s was incorrectly set as %s"
                    % (ip, self.hosts.get_platform_hostname())
                )
        for ip in VALID_IP:
            try:
                self.hosts.set_platform_ip(ip)
            except AssertionError as e:
                errors.append(
                    "Valid IP %s was incorrectly rejected with following message:\n\t%s"
                    % (ip, e.args[0])
                )
            if ip != self.hosts.get_platform_ip():
                errors.append(
                    "Valid IP %s was incorrectly set as %s"
                    % (ip, self.hosts.get_platform_ip())
                )
        # Duplicate Inputs
        hostname = VALID_HOSTNAMES[0]
        ip = VALID_IP[0]
        self.hosts = HostsConfig()
        # Set Value Once
        try:
            self.hosts.set_platform(Host(hostname, ip))
        except AssertionError as e:
            errors.append(
                "Valid Hostname, IP %s were incorrectly rejected with the following message:\n\t%s"
                % ((hostname, ip), e.args[0])
            )
        if (
            hostname != self.hosts.get_platform_hostname()
            or ip != self.hosts.get_platform_ip()
        ):
            errors.append(
                "Valid Hostname and IP %s were incorrectly set as %s"
                % ((hostname, ip), self.hosts.get_platform())
            )
        # Set Value Again
        try:
            self.hosts.set_platform(Host(hostname, ip))
        except AssertionError:
            pass  # Do nothing, expected
        else:
            errors.append(
                "Duplicate Hostname '%s' and IP '%s' accepted." % (hostname, ip)
            )
        assert not errors, "Errors: %s" % "\n".join(errors)

    def test_onboard(self):
        self.hosts = HostsConfig()
        errors = []
        # Adding Invalid Inputs
        for hostname in INVALID_HOSTNAMES:
            ip = VALID_IP[0]
            try:
                self.hosts.add_onboard(hostname=hostname, ip=ip)
            except AssertionError:
                pass  # Do nothing, expected
            else:
                errors.append("Invalid Hostname %s was incorrectly accepted" % hostname)
        for ip in INVALID_IP:
            hostname = VALID_HOSTNAMES[0]
            try:
                self.hosts.add_onboard(hostname=hostname, ip=ip)
            except AssertionError:
                pass  # Do nothing, expected
            else:
                errors.append("Invalid IP '%s' was incorrectly accepted" % ip)
        # Adding, Duplicating, and Removing Valid Inputs
        for hostname in VALID_HOSTNAMES:
            for ip in VALID_IP:
                # Add
                try:
                    self.hosts.add_onboard(hostname=hostname, ip=ip)
                except AssertionError as e:
                    errors.append(
                        "Valid Hostname %s was incorrectly rejected with following message:\n\t%s"
                        % (hostname, e.args[0])
                    )
                # Check Duplicates
                try:
                    self.hosts.add_onboard(hostname=hostname, ip=ip)
                except AssertionError:
                    pass  # Do nothing, expected
                else:
                    errors.append(
                        "Duplicate Hostname '%s' and IP '%s' accepted." % (hostname, ip)
                    )
                # Remove
                try:
                    self.hosts.remove_onboard(hostname=hostname, ip=ip)
                except AssertionError as e:
                    errors.append(
                        "Unable to remove existing hostname and ip with following message:\n\t%s"
                        % e.args[0]
                    )
                for host in self.hosts.get_onboard():
                    if hostname == host.get_hostname() or ip == host.get_ip():
                        errors.append(
                            "Remove failed. Host '%s','%s' was not removed"
                            % (host.get_hostname(), host.get_ip())
                        )
        assert not errors, "Errors: %s" % "\n".join(errors)

    def test_remote(self):
        self.hosts = HostsConfig()
        errors = []
        # Adding Invalid Inputs
        for hostname in INVALID_HOSTNAMES:
            ip = VALID_IP[0]
            try:
                self.hosts.add_remote(hostname=hostname, ip=ip)
            except AssertionError:
                pass  # Do nothing, expected
            else:
                errors.append("Invalid Hostname %s was incorrectly accepted" % hostname)
        for ip in INVALID_IP:
            hostname = VALID_HOSTNAMES[0]
            try:
                self.hosts.add_remote(hostname=hostname, ip=ip)
            except AssertionError:
                pass  # Do nothing, expected
            else:
                errors.append("Invalid IP '%s' was incorrectly accepted" % ip)
        # Adding, Duplicating, and Removing Valid Inputs
        for hostname in VALID_HOSTNAMES:
            for ip in VALID_IP:
                # Add
                try:
                    self.hosts.add_remote(hostname=hostname, ip=ip)
                except AssertionError as e:
                    errors.append(
                        "Valid Hostname %s was incorrectly rejected with following message:\n\t%s"
                        % (hostname, e.args[0])
                    )
                # Check Duplicates
                try:
                    self.hosts.add_remote(hostname=hostname, ip=ip)
                except AssertionError:
                    pass  # Do nothing, expected
                else:
                    errors.append(
                        "Duplicate Hostname '%s' and IP '%s' accepted." % (hostname, ip)
                    )
                # Remove
                try:
                    self.hosts.remove_remote(hostname=hostname, ip=ip)
                except AssertionError as e:
                    errors.append(
                        "Unable to remove existing hostname and ip with following message:\n\t%s"
                        % e.args[0]
                    )
                for host in self.hosts.get_remote():
                    if hostname == host.get_hostname() or ip == host.get_ip():
                        errors.append(
                            "Remove failed. Host '%s','%s' was not removed"
                            % (host.get_hostname(), host.get_ip())
                        )
        assert not errors, "Errors: %s" % "\n".join(errors)
