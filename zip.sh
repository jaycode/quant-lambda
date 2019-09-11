#!/bin/bash

create_layer () {
	rm -f ./layers/aws-$1-layer.zip
	cd ./layers/$1-layer
	zip -r aws-$1-layer.zip python
	mv aws-$1-layer.zip ..
	cd ${OLDPWD}	
}

create_function () {
	cd functions
	rm -f ./zipped/$1.zip
	zip -r ./zipped/$1.zip ./$1.py
	cd ${OLDPWD}
}

# Only need to do once, uncomment when need to install
# create_layer "psycopg2"
# create_layer "pandas"
# create_layer "pyexcel"
# create_layer "xlrd"
create_layer "openpyxl"
create_layer "helpers"

create_function "front_gate"
create_function "create_tables"
zip -g ./functions/zipped/create_tables.zip ./queries.py
create_function "convert_to_xls"
create_function "get_sheet_names"
create_function "insert_rows"
zip -g ./functions/zipped/insert_rows.zip ./queries.py
create_function "trigger_quant-lambda"
create_function "create_views"
zip -g ./functions/zipped/create_views.zip ./queries.py


echo Functions are ready at \`./functions/zipped\` directory and layers at \`./layers\` directory.

