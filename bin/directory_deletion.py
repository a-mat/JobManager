import os
import os.path as path
import csv
import shutil
import logging
import sys
import click
import threading

@click.command()
@click.option('--user',
              help='specify the user that you want')
@click.option('--app',
              help='specify the user that you want')
@click.option('--savedsearch',
              help='specify the user that you want')
@click.option('--ttl',
              help='specify the user that you want')
@click.option('--schedule', type=click.IntRange(1,1440 ),
              help='numerical value to represent how often this script runs. Choosing the number \'11\' will run this'
                   ' script every 11 minutes')


def test (user,app,savedsearch,ttl,schedule):
    time=ttl
    sched=schedule*60
    dict={"user":user, "app":app, "savedsearch":savedsearch}
    dict = {k: v for k, v in dict.items() if v != None}
    for k,v in dict.items():
            dict[k]=v.split(',')

    # print(path.abspath(path.join(os.getcwd(),"../..")))

    path="dispatch"
    repeater(sched,dict,path)

   # scanDir(dict,path)



#path='/syslog/apps/splunk/var/run/splunk/dispatch'
#path='dispatch'

def scanDir(dict,path):
    global list_of_stuff
    list_of_stuff=[]
    logging.info("Running down the list in" + path)
    try:
        d=os.listdir(path)
    except:
            logging.info("directory doesnt exist")
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
                    logging.info('In ' + jobpath +' job. Examining first line: ')
                    logging.info(r)
                    total=0
                    for k in dict:
                        for v in dict[k]:

                            if r[k]==v and r['state'] == 'DONE':
                                total+=1
                                logging.info(k + ':' + v +' matched with  ' + jobpath + '\'s ' + k + ':' + r[k] )
                            else:
                                logging.info(k + ':' + v + ' did not match with  ' + jobpath + '\'s ' + k + ':' + r[k])

                    if total== len(dict.keys()):
                        delcheck = True


                if delcheck:
                    logging.info(dir + " job matches the delCheck. It is marked for deletion")
                    list_of_stuff.append(jobpath)
                logging.info("The list of Marked jobs are: " + ','.join(list_of_stuff))



        for d in list_of_stuff:
            logging.info('scan across dispatch directory is complete. Files ' + d + ' will be deleted')
            print(d)
            # shutil.rmtree(folder,ignore_errors=True)



def repeater(sched,d,p):
    scanDir(d,p)
    threading.Timer(sched, repeater, [sched,d,p]).start()



# System argument will take Username, Saved Search Name, APP,
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename='test.log')
    logging.info('Script ran')
    list_of_stuff = []

    test()




