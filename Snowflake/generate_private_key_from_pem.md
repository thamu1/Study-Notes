Encoded Private Key Must be generated from PEM file using the following command:
--------------------------------------------------------------------------------

STEPS:
-----
  > openssl pkcs8 -topk8 -nocrypt -in "C:/Thamo/<folder name>/snowflake_private_key.pem" -out cdbi.p8

  > Replace all / -> _ and + -> - in the generated cdbi.p8 file content.
  
  > Use it in the Encoded Private Key field below.
  
  > snowflake_base64_url_encoded_private_key="<Generated Key Here>" # accessing from DBT or other languages(python etc..)