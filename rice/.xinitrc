[ -f ~/.Xresources ] && xrdb -merge ~/.Xresources &
(exec conky | while read -r; do echo $REPLY | sed -e 's/:1:/\^/g' | sed -e 's/:2:/\#/g' | { read bob; echo $bob; xsetroot -name "$bob";} done ) &
feh --bg-scale ~/Downloads/bg.jpg &
(sleep 5 && discord) &
urxvtd --quiet --opendisplay --fork &
exec dbus-launch --sh-syntax --exit-with-session dwm
