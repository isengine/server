SECOND=${2:-$1}
NAME=${SECOND//[^a-zA-Z0-9.-]/_}

mkcert --key-file ${NAME}.key --cert-file ${NAME}.crt $1

mv ${NAME}.key /var/mkcert
mv ${NAME}.crt /var/mkcert

cp rootCA.pem /var/mkcert/${NAME}.ca
