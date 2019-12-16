import os
import csv
import shutil
import logging
import sys
import click

@click.command()
@click.option('--user',
              help='specify the user that you want')
@click.option('--app',
              help='specify the user that you want')
@click.option('--savedsearch',
              help='specify the user that you want')
@click.option('--ttl',
              help='specify the user that you want')

def test (user,app,savedsearch,ttl):
    time=ttl
    dict={"user":user, "app":app, "savedsearcj":savedsearch}
    dict = {k: v for k, v in dict.items() if v != None}
    print(dict)
    print("didnt work")

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO,filename='test.log')
logging.info('Script ran')

#path='/syslog/apps/splunk/var/run/splunk/dispatch'
#path='dispatch'

def scanDir():
    global list_of_stuff
    logging.info("Running down the list in" + path)
    try:
        d=os.listdir(path)
    except:
            print("directory doesnt exist")
            exit()
    else:
        for dir in d:
            jobpath = (path+'/'+dir)
            logging.info("First Job to be examined is: "+ dir)
            try:
                jobstat=open(jobpath + "/status.csv")

            except FileNotFoundError:
                logging.info(jobpath + "/status.csv file doesnt exist")
            except OSError:
                logging.info("Error opening up " + jobpath + "/status.csv")

            else:
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


            #shutil.rmtree(folder,ignore_errors=True)
            #break


def delList(file_list):
    logging.info("Deleting " + ','.join(file_list))
    for d in file_list:
        print(d)
    # shutil.rmtree(folder,ignore_errors=True)





# System argument will take Username, Saved Search Name, APP,
if __name__ == "__main__":
    print("before")
    test()
    print("mp[e")
   # try:
    #    test()

    #except:
    #    print("there was an error with the arguments")
    #    exit()
    #try:
     #   dispatchPath=sys.argv[4]
    #except:
    #    path="dispatch"
    #else:
     #   path=dispatchPath
    #finally:
     #   list_of_stuff=[]
      #  scanDir()
       # delList(list_of_stuff)


