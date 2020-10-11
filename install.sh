USER=$1

#Portage
cp -r portage /etc/
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
eselect modules has opengl && eselect opengl set nvidia
gpasswd -a $USER video
