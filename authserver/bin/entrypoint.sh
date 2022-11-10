#!/bin/sh

set -eo pipefail

# $ authserver/bin/authserver-linux --help
# usage: authserver --private-key=PRIVATE-KEY [<flags>]
#
# ODAS Auth Server.
#
# Flags:
#       --help                     Show context-sensitive help (also try --help-long and --help-man).
#   -p, --port=5001                Port to bind to
#   -d, --directory="/tmp/tokens"  Directory to place tokens in
#   -k, --private-key=PRIVATE-KEY  Path to private key
#   -a, --algorithm=rsa512         Signing algorithm
#       --disable-delete           Disable automatic key garbage collection
#   -g, --group="okera"            Group to chown to

# start daemon
authserver-linux -p $PORT -d $TOKEN_DIR -k $PRIVATE_KEY_FILE -a $ALGORITHM -g $GID