PKG_NAME=pastcodd_1.1-1_all

deb:
	mkdir -p ${PKG_NAME}/usr/bin
	cp ../pastcodd.py ${PKG_NAME}/usr/bin/
	mkdir -p ${PKG_NAME}/DEBIAN
	cp control ${PKG_NAME}/DEBIAN
	cp postinst ${PKG_NAME}/DEBIAN
	dpkg-deb --build ${PKG_NAME}
	mkdir -p ${PKG_NAME}/etc/init.d
	cp pastcodd ${PKG_NAME}/etc/init.d/

clean:	
	rm -f ${PKG_NAME}.deb
	rm -rf ${PKG_NAME}
