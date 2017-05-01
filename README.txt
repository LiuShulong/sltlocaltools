
sltlocaltools
===

![stringsToxls](http://img.blog.csdn.net/20170501134701254?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdGFpc2hhbmR1YmE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

![xlsToStrings](http://img.blog.csdn.net/20170501134717317?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdGFpc2hhbmR1YmE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

sltlocaltools is a tool to help search iOS localizabel.strings and convert it between xls and strings.

Installing
---

`pip install sltlocaltools`

Usage
---

convert strings to xls

`python xlsconvertor.py -t 1 -sd ~/Desktop/test -x ~/Desktop/my.xls`

convert xls to strings

`python xlsconvertor.py -t 1 -sd ~/Desktop/test -x ~/Desktop/my.xls`

-	-t : 1 means convert to xls,2 means convert to strings
-  -s : localizable strings dir path
-  -x : xls file path