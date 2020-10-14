[ -f ~/.Xresources ] && xrdb -merge ~/.Xresources &
(exec python ~/PycharmProjects/taskbar/main.py | while read -r; do echo $REPLY | { read bob; echo $bob; xsetroot -name "$bob";} done ) &
feh --bg-scale ~/background.jpg &
(sleep 5 && discord) &
urxvtd --quiet --opendisplay --fork &
exec dbus-launch --sh-syntax --exit-with-session dwm
