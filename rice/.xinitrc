[ -f ~/.Xresources ] && xrdb -merge ~/.Xresources &
feh --bg-scale ~/bg.jpeg &
( python ~/statusbar.py) &
(sleep 5 && discord) &
urxvtd --quiet --opendisplay --fork &
exec dbus-launch --sh-syntax --exit-with-session dwm >> ~/log 
