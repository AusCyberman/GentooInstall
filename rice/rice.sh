if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi
echo ROOT
if [ "$#" -ne 1 ]; then
	echo "Remember to pass home directory"
	exit 1
fi
HOME=/home/$1
emerge rxvt-unicode xrdb media-fonts/inconsolata media-fonts/fontawesome conky
cp .xinitrc ~/.xinitrc
cp .conkyrc ~/.conkyrc
cp .Xresources ~/.Xresources
cp get_audio.lua ~/
cp -r dmenu ~/
cp -r dwm ~/



#Install
cd ~/dmenu
make clean install
cd ~/dwm
make clean install

