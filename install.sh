emerge -vuDN @world

#FSTAB
emerge sys-fs/ntfs3g
cp kernel/fstab /etc/fstab


#CHROME
emerge google-chrome-stable


#X11 Install
emerge --pretend --verbose x11-base/xorg-drivers
emerge x11-base/xorg-server
cp -r xorg/xorg.conf.d /etc/X11/
