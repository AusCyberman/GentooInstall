
#Portage

emerge --config sys-libs/timezone-data
emerge sys-kernel/gentoo-sources
#FSTAB
emerge sys-fs/ntfs3g
emerge sys-kernel/linux-firmware
emerge sys-apps/pciutils
cp kernel/.config /usr/src/linux/.config
cd /usr/src/linux
make -j17 && make -j17 modules_install && make install


#X11 Install
emerge --pretend --verbose x11-base/xorg-drivers
emerge x11-base/xorg-server
cp -r xorg/xorg.conf.d /etc/X11/
eselect modules has opengl && eselect opengl set nvidia
eselect modules has opencl && eselect opencl set nvidia
