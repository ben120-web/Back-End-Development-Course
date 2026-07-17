# Security policy

Please report suspected vulnerabilities privately through GitHub's security
advisory interface. Do not include credentials or exploit details in a public
issue.

This project constrains agent filesystem paths and gives child processes an
allowlisted environment that excludes API credentials. It is not an isolation
boundary for hostile code: executed programs retain the current user's network
and operating-system permissions. Use a disposable, least-privileged container
or microVM for untrusted workloads.
