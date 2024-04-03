# doh_checker

A doh support check tool to check recursive server support what type of DoH.

```
Usage: python3 doh_checker.py ip_to_be_checked
```
Possible result and meaning:
* GETBASE64PARAM：RFC8484 format
* POST：RFC8484 post format
* JSON：RFC8427 format
