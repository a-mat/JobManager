# JobManager
 
This script allows you to clean up any remaining jobs in your directory that are done.It searches for the keyword "DONE" in the directory and marks them for deletion.

The goal of this script is to allow you to delete DONE jobs and can be filtered down at a User Level and App Level. 
    
 ## Usage
 
 ```
 directory_deletion.py [--user ListUsers][--app ListApp ][--savedsearches ListSS][--schedule timer][--path dispatchPath]
 ```
 
 # Flags
 
   `--user ListUsers`
        specify the user that will have their jobs deleted . Multiple users can be listed as long as they are comma delimited 
   
   `--app ListApp`
        Specify the app that will have its jobs deleted . Multiple apps can be listed as long as they are comma delimited       
  
   `--savedsearches ListSS`
        Specify the searches that will be deleted . Multiple searches can be listed as long as they are comma delimited    
    
   `--schedule timer`
        How often this script will restart and look for jobs to be deleted. Script can run as quick as every minute or once every 14               hours.Int value that is in  minutes. m Range: 1<=timer<=1440
   
   `--path dispatchPath` 
        Path of the dispatch directory (e.g. \'/opt/splunk/var/run/dispatch\').If no match is specified, the script will look for the           the dispatch directory as long as this script is placed in any of the following directories: \'SPLUNK_HOME/bin\' , 
        \'SPLUNK_HOME/etc/apps/\<app\>/bin\' , or \'SPLUNK_HOME/var/run/dispatch\'. No quotes needed.
    
        
    
 ***All of the Flags are optional. If they are omitted, the script will assume that no filter is given for that flag.***
 
 `directory_deletion.py --user Todd  --savedsearch inventorysearch_24hr --schedule 5`
    The script will delete Todd's completed inventorysearch_24hr search job in all apps everu 5 minutes
    
  `directory_deletion.py --user Todd,Mary  --apps search --schedule 20`
    The script will delete all of Todd's and Mary's completed jobs in the search app every 20 min
 
  `directory_deletion.py --path /opt/siem/splunk/var/run/dispatch`
    The script will delete all completed jobs in all the apps every 24 hours in the /opt/siem/splunk/var/run/dispatch directory    
   
   `directory_deletion.py`
     The script will delete all completed jobs in all the apps every 24 hours
