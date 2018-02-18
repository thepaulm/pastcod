PKG_NAME=pastcodd_1.1-1_all

deb: layout
	dpkg-deb --build ${PKG_NAME}

layout:
	mkdir -p ${PKG_NAME}/usr/bin
	cp ../pastcodd.py ${PKG_NAME}/usr/bin/
	mkdir -p ${PKG_NAME}/DEBIAN
	cp control ${PKG_NAME}/DEBIAN
	cp postinst ${PKG_NAME}/DEBIAN
	cp prerm ${PKG_NAME}/DEBIAN
	chmod -R 755 ${PKG_NAME}/DEBIAN
	mkdir -p ${PKG_NAME}/lib/systemd/system
	cp pastcodd.service ${PKG_NAME}/lib/systemd/system

clean:	
	rm -f ${PKG_NAME}.deb
	rm -rf ${PKG_NAME}
