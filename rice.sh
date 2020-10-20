if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi
if [ "$#" -ne 1 ]; then
	echo "Remember to pass home directory"
	exit 1
fi
HOME=/home/$1
unzip rice.zip
cd rice
cp .xinitrc ~/.xinitrc
cp .Xresources ~/.Xresources
cp statusbar.py ~/
cp -r dmenu ~/
cp -r dwm ~/
cp -r st ~/

#Install
cd ~/dmenu
make clean install
cd ~/dwm
make clean install
cd ~/st
make clean install
