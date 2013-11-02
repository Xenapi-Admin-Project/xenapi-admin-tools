#!/bin/bash

PROJHOME="/root/bin/xenapi-admin-tools"
XAPSITE="192.168.1.101:/var/www/html/xenapiadmin.com/"
echo '%_signature gpg' > ~/.rpmmacros
echo '%_gpg_path /root/.gnupg' >> ~/.rpmmacros
echo "%_gpg_name $(gpg --dry-run --import RPM-GPG-KEY-xap 2>&1 | grep key | awk -F\" '{print $2}')" >> ~/.rpmmacros
echo '%_gpgbin /usr/bin/gpg' >> ~/.rpmmacros

# Update the git repository
cd "$PROJHOME" ; git pull

# Create archive of files by using git archive
# Create spec file from template


# rpmbuild -ba (with signature)
# To generate an ascii public certificate 
# Private keys are in /root/.gnupg
# gpg --armor --output RPM-GPG-KEY-xap --export 'Grant McWilliams'
rpmbuild -v -ba --sign --clean "$PROJHOME/repodev/SPECS/xenapi-admin-tools.spec"

# Copy rpms to repo
cp "~/rpmbuild/RPMS/i386/xenapi-admin-tools.rpm" "$PROJHOME/repo/xcp/1.6"

# Create Repo Indexes
createrepo "$PROJHOME/repo/xcp/1.6"

# Commit changes to github
cd "$PROJHOME"
git add *
git commit -a

# scp all files to xenapiadmin.com
scp -r "$PROJHOME/repo/xcp/1.6" "$XAPSITE/repo/xcp/" 
