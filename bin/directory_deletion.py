import os
import csv
import shutil
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO,filename='test.log')
logging.info('Script ran')

path='/syslog/apps/splunk/var/run/splunk/dispatch'
path='dispatch'
list_of_stuff = []
logging.info("Running down the list in" + path)
for dir in os.listdir(path):
        jobpath = (path+'/'+dir)
        logging.info("First Job to be examined is: "+ dir)
        with open(jobpath + "/status.csv") as jobstat:
            reader = csv.DictReader(jobstat)
            delcheck = False
            for r in reader:

                if (r['state'] == 'DONE' and r['user'] == '427958'):
                    # print(dir + "My job and it is over")
                    logging.info(dir + "is  DONE and matches the User")
                    delcheck = True
                    break
                elif r['user'] == '427958':
                    # print(dir + " job is not done and is currently: " + r['state'] )
                    # logging.info(dir + " job is not done and is currently: " + r['state'])
                    pass
                else:
                    # print(dir + " is not yours")
                    # logging.info(dir + " not my job so not going to get deleted")
                    pass
            if delcheck:
                logging.info(dir + "matches the delCheck. It is marked for deletion")
        list_of_stuff.append(jobpath)
logging.info("The list of Marked jobs are: " + ','.join(list_of_stuff))

for folder in list_of_stuff:
    #shutil.rmtree(folder,ignore_errors=True)
    break

def delList(file_list):
    print(file_list)

delList(list_of_stuff)

if __name__ == "__main__":
# main method
