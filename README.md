LM_from_DB
==========

This is the SQL-source version n-gram probability calculator derived 
from the NLTK tools script.

This script is originally re-designed for log-probability calculation 
since my huge n-gram model is stored in SQL for convenience. So some 
advanced features in the original version which use standard LM is 
not implemented.

This script use MySQLDB python SQL interface to communicate with your 
database, feel free to modify to other DB interfaces.

The place you need to edit:
Edit MySQL interface:
connection = MySQLdb.connect(host = "localhost", port = 3306,\
                              user = "root", passwd = "cikuutest!")
to fit to your DB settings.

This is the n-gram entry count:
self.cnt_sum = (1, 1024908267229, 889143670228, 733110350273, \
                503325708296, 349051688901)
each stands for the [n-1]-gram count as the comment shows
#sum[0] = 1
#sum[1] = 1024908267229
#sum[2] = 889143670228
#sum[3] = 733110350273
#sum[4] = 503325708296
#sum[5] = 349051688901

The replacer script is for string RE replacement, you can turn it off 
if you don't need that feature.
 
BTW, you can uncomment the starting def _estimator(fdist, bins) func, 
if you want to use pickle (not tested). 

And also, you should install the original NLTK tools since it import 
the NLTK tokenizer. (Yes, you can disable it and use your own tokenizer
as well...)

---------------------------------------------------------------------
Something you should know:
as your DB table format, look at this line:
self.slct = "select cnt from gramc where gram like '%s' "
it assume that in your DB: "web1t" (modify to yours)
table name "gramc" (modify to yours)
has at least two columns "gram" and "cnt", each stands for your ngram 
entry and its count.