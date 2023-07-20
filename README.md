# Backup Dell Switches Automatically using Python and TFTP server

## Goal

This script is for automatically backing up dell switches to a TFTP server. In my tests, I had some problems saving the configuration backup just by copying the contents because of the amount of data for the terminal, which shows an extra show, so the logic would be increased.

## TFTP Server configuration used:


``` sudo apt install tftpd-hpa ```

``` sudo nano /etc/default/tftpd-hpa ```

```
# /etc/default/tftpd-hpa

TFTP_USERNAME="tftp"
TFTP_DIRECTORY="/tftp"
TFTP_ADDRESS=":69"
TFTP_OPTIONS="--secure --create"
```

``` sudo mkdir /tftp ```

``` sudo chown tftp:tftp /tftp ```

``` sudo systemctl restart tftpd-hpa ```

## Dependencies

### Paramiko

``` pip3 install paramiko ```

## How to run

``` python ./script.py ```
