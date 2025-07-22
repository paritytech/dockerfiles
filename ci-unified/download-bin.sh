#!/bin/bash

DL_PATH="$HOME/.tmp/"
VERSION="latest"
ASSET_NAME="solc-static-linux"
BASE_URL="https://github.com/ethereum/solidity"
BIN_NAME="solc"

case $1 in

  solc)
    ASSET_NAME="solc-static-linux"
    BASE_URL="https://github.com/ethereum/solidity/releases"
    BIN_NAME="solc"
    ;;

  resolc | revive)
    ASSET_NAME="resolc-x86_64-unknown-linux-musl"
    BASE_URL="https://github.com/paritytech/revive/releases"
    BIN_NAME="resolc"
    ;;

  *)
    echo -n "unknown name"
    ;;
esac

if [[ "" == $2 ]]; then
  VERSION="latest"
else
  VERSION=$2
fi


ASSET_URL="$BASE_URL/download/$VERSION/$ASSET_NAME"

if [[ "latest" == $VERSION ]]; then
  ASSET_URL="$BASE_URL/latest/download/$ASSET_NAME"
fi

echo "Downloading $ASSET_NAME $VERSION from $ASSET_URL"

mkdir -p $DL_PATH
curl -Lsf --show-error -o $DL_PATH/$ASSET_NAME $ASSET_URL
cp $DL_PATH/$ASSET_NAME /usr/local/bin/$BIN_NAME

chmod 755 /usr/local/bin/$BIN_NAME