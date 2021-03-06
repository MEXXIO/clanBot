#!/bin/sh

# Decrypt the file
# --batch to prevent interactive command --yes to assume "yes" for questions
gpg --quiet --batch --yes --decrypt --passphrase="$api" \
--output ./api.json ./api.json.gpg

gpg --quiet --batch --yes --decrypt --passphrase="$api" \
--output ./char.json ./char.json.gpg

gpg --quiet --batch --yes --decrypt --passphrase="$api" \
--output ./channelList.dat ./channelList.dat.gpg

gpg --quiet --batch --yes --decrypt --passphrase="$api" \
--output ./token.json ./token.json.gpg