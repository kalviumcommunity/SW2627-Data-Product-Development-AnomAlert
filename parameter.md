## Dataset Column Description

1. event_id

## Description:
A unique sequential identifier assigned to every authentication event in the dataset. It ensures that each login event can be uniquely identified and referenced during analysis.

## Purpose:
Used to uniquely distinguish each authentication record and maintain data integrity.

2. timestamp

## Description:
Records the exact date and time when an authentication event occurred. The events in this dataset span from May 1, 2026, to May 30, 2026.

## Purpose:
Helps analyze login trends over time, identify peak authentication periods, and detect unusual login timings that may indicate suspicious activity.

3. user_id

## Description:
A unique identifier assigned to each user in the format U0001–U0500. This identifier represents individual users without revealing personal information.

## Purpose:
Enables tracking of user authentication history and behavioral patterns across multiple login events.

4. user_role

## Description:
Specifies the access level assigned to the user. The dataset includes two roles:

Standard – Regular user account
Admin – Privileged account with elevated permissions

## Purpose:
Helps identify high-privilege accounts that require additional security monitoring due to their increased access rights.

5. src_host

## Description:
Represents the source workstation or host from which the authentication request originated.

## Purpose:
Used to identify the device initiating the login request and detect authentication attempts from unfamiliar or unauthorized devices.

6. src_subnet

## Description:
Represents the network subnet associated with the source host. Internal devices generally belong to private network ranges, while simulated external or attacker systems may use different subnet configurations.

## Purpose:
Helps determine whether an authentication request originated from an internal organizational network or an external source.

7. dst_host

## Description:
Identifies the destination workstation, server, or domain controller that the user attempted to access.

## Purpose:
Used to determine which system was being accessed and to identify unusual or unauthorized access attempts to critical resources.

8. auth_protocol

## Description:
Specifies the authentication protocol used during the login process. The dataset includes:

Kerberos
NTLM

## Purpose:
Helps analyze authentication mechanisms used within the network and identify protocol-specific security patterns or vulnerabilities.

9. logon_type

## Description:
Indicates the type of authentication activity performed. Common logon types include:

Interactive
Network
Service
Remote Interactive

## Purpose:
Helps distinguish between local logins, remote access, network authentications, and service account activities, enabling better behavioral analysis.

10. auth_result

## Description:
Indicates the outcome of each authentication attempt as either Success or Failure.

## Purpose:
Used to identify failed login patterns, detect repeated authentication failures, and support the identification of potential brute-force attacks or unauthorized access attempts.