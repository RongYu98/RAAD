#!/bin/bash
password='false'
password2='true'
while [ "$password" != "$password2" ]; do
    echo -n Password: 
    read -s password
    echo
    echo -n Confirm password: 
    read -s password2
    echo
done
# Run Command
echo Inserting password...
cd backend
python3 -c "import hash_utils; salt = hash_utils.generate_salt(); hash_utils.store_salt(salt); hash_utils.store_password(hash_utils.hmac_hash(\"$(printf "%q" $password)\", salt))"
