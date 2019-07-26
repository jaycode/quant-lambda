#!/bin/bash

rm -f ./function.zip

cd ./package

zip -r9 ${OLDPWD}/function.zip .

cd ${OLDPWD}

zip -g ./function.zip ./lambda_function.py

echo The file is ready at \`./function.zip\`. Please use it for lambda deployment.

