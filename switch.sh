ARCH="$(arch)"
STREAM=$1

echo $STREAM
sudo systemctl stop zincati.service
sudo rpm-ostree rebase "fedora/${ARCH}/coreos/${STREAM}"
rpm-ostree status
sudo systemctl reboot