curl -v -X POST -u Administrator:password \
http://localhost:8091/settings/querySettings \
-d 'queryTmpSpaceDir=/tmp' \
-d 'queryTmpSpaceSize=2048'