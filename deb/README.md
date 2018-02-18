# Debian Packaging

Things in the directory or for the making of a minimal debian (.deb file) that can be
apt-get installed on the device. To actually build the debian package you need to run
this on a linux box that has dpkg-deb installed. dpkg-deb comes from the dpkg package
so it should already be installed on your system.

Yes, this works from a docker image too: I used armhero/raspbian to simulate the
device.

# Installing
Copy to device, then:

```
dpkg -i ./pastcodd_1.1-1_all.deb
```

# Uninstalling

```
dpkg -P pastcodd
```
