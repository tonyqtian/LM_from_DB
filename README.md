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

The replacer script is for string RE replacement, you can turn it off 
if you don't need that feature.
 
BTW, you can uncomment the starting def _estimator(fdist, bins) func, 
if you want to use pickle (not tested). 