# Make Debian package (for Debian stretch)


Install `schroot` and edit `/etc/schroot.conf` to add an entry for a stretch
chroot:

    cat >> /etc/schroot.conf <<EOF
    [stretch]
    type=directory
    description=Debian stretch
    directory=/usr/local/schroot/stretch
    users=frank
    root-users=YOUR-ACCOUNT
    EOF

Install a stretch chroot:

    mkdir /usr/local/schroot/stretch
    debootstrap stretch /usr/local/schroot/stretch

    
