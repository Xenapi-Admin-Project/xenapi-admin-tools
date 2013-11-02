#!/bin/bash -x
# xanpai-admin-tools-release build script
# mktoolsreleaserpm.sh version 0.1

# package specific settings
DESCRIPTION="Xenapi Admin Tools release file. This package contains yum configuration for the Xenapi Admin Tools Repository, as well as the public GPG keys required to use it."
SUMMARY="Xenapi Admin Tools release file and RPM repository configuration"
ARCH="i386"
NAME="xenapi-admin-tools"
PROVIDES="RPM-GPG-KEY-xap xenapi-admin-tools.repo"
REQUIRES="rpm yum"
FILES="/etc/yum.repos.d/xenapi-admin-tools.repo /etc/pki/rpm-gpg/RPM-GPG-KEY-xap"
RELEASE="1"  # don't change, it's just the start index
RPMBASE="/usr/src/redhat/"
SPECFILE="$RPMBASE/SPECS/${NAME}.spec"

setup()
{
	for DIR in "$RPMBASE" "$RPMBASE/SPECS" ;do
		if [[ ! -d "$DIR" ]] ;then
			echo "Creating $DIR"
			mkdir -p "$DIR"
		fi
	done
}

yesno()
{
	MESSAGE="$1"
	while true; do
		echo "$MESSAGE <yes|no>"
  		read YESNO
  		case $YESNO in
  		  y | yes | Y | Yes | YES ) ANS="1" ; break ;;
  		  n | no | N | No | NO )  ANS="0"   ; break ;;
  		  * ) echo "Please enter yes or no." ;;
  		esac
	done  
}

isnum()
{
	while true ;do
		if [[ ! "$1" =~ ^[0-9]+([.][0-9]+)?$ ]] ;then
			echo "Please enter only numbers separated by a dot e.g. 1.2"
			getversion
			isnum "$NEWVERSION"
		else
			return 0
		fi
	done
}

setup

echo "Building new $NAME rpms"
if ! rpm -q "$NAME" ;then
	OLDVERSION="0.0"
	OLDRELEASE="0.0"
else
	OLDVERSION=$(rpm -qa --queryformat "%{VERSION}" "$NAME")
	OLDRELEASE=$(rpm -qa --queryformat "%{RELEASE}\n" "$NAME" | awk -F\. '{print $1}')
fi
getversion 

if expr "${NEWVERSION}" = "${OLDVERSION}" >/dev/null  ;then
	(( OLDRELEASE++ ))
elif expr "${NEWVERSION}" \< "${OLDVERSION}" >/dev/null  ;then
	echo "$NEWVERSION is not greater than $OLDVERSION"
	getversion 
fi

cd / ;tar -czvpf "$RPMBASE/SOURCES/$NAME-$NEWVERSION.tar.gz" $FILES

echo "Summary: $SUMMARY" >> $SPECFILE
echo "Name: $NAME" >> "$SPECFILE"
echo "Version: $NEWVERSION" >> "$SPECFILE"
echo "Release: $RELEASE" >> "$SPECFILE" 
echo "License: GPL" >> "$SPECFILE"
echo "Group: System Environment/Base" >> "$SPECFILE"
echo "Source: $NAME-$NEWVERSION.tar.gz" >> "$SPECFILE"
echo "Buildroot: /var/tmp/%{name}-buildroot" >> "$SPECFILE"
echo "" >> "$SPECFILE"
for i in $REQUIRES ;do
	echo "Requires: $i" >> "$SPECFILE"
done
for i in $PROVIDES ;do
	echo "Provides: $i" >> "$SPECFILE"
done
echo "" >> "$SPECFILE"
echo "%description" >> "$SPECFILE"
echo $DESCRIPTION >> "$SPECFILE"
echo "%prep" >> "$SPECFILE"
echo "%setup -c -q" >> "$SPECFILE"
echo "" >> "$SPECFILE"
echo "%install" >> "$SPECFILE"
echo cp -a ./ '$RPM_BUILD_ROOT/' >> "$SPECFILE"
echo "" >> "$SPECFILE"
echo "%clean" >> "$SPECFILE"
echo rm -rf '$RPM_BUILD_ROOT' >> "$SPECFILE"
echo "" >> "$SPECFILE"
echo "%post" >> "$SPECFILE"
echo "" >> "$SPECFILE"
echo "%files" >> "$SPECFILE"
echo "%defattr(-,root,root)" >> "$SPECFILE"
for i in $FILES ;do
	echo "$i" >> "$SPECFILE"
done
echo "" >> "$SPECFILE"

# Need to change this so it signs them
echo "Done creating source archive and spec file - now creating binary rpms"
cd "$RPMBASE/SPECS/"
rpmbuild -bb --target=$ARCH ${NAME}.spec

echo "$RPMBASE/RPMS/$ARCH/$NAME-$NEWVERSION-$RELEASE.$ARCH.rpm"
# Copy rpm to git project
# createrepo
# git add all files
# git commit -m <file>
# git push




