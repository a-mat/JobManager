import os
import os.path as path
import csv
import shutil
import logging
import sys
import click
import threading

"""

TODO:
    1) TTL argument needs to be flushed out
    2) Implementation of the deletion command needs to be worked on as well.
    3) Check if black/front slash affects the search for windows 
"""


@click.command()
@click.option('--user',
              help='specify the user that you want')
@click.option('--app',
              help='specify the user that you want')
@click.option('--savedsearch',
              help='specify the user that you want')
@click.option('--ttl',
              help='specify the user that you want')
@click.option('--schedule', type=click.IntRange(1, 1440),
              help='numerical value to represent how often this script runs. Choosing the number \'11\' will run this'
                   ' script every 11 minutes')
@click.option('--path',
              help='specify the path of the dispatch directory (e.g. /opt/splunk/var/run/dispatch')


#userParambb methoad cleans up the whole user input
def userParam(user, app, savedsearch, ttl, schedule,path):
    global dispatchDir
    time = ttl
    dispatchDir = pathFinder() if path is None else path #if path is not specified, pathfinder() will find dispatch dir
    dict = {"user": user, "app": app, "savedsearch": savedsearch}  # dict that will be used to iterate through the .csv

    dict = {k: v for k, v in dict.items() if v != None}  #remove items that the user did not pass
    for k, v in dict.items():  # splits values into array if the user passed conmma delimited values
        dict[k] = v.split(',')


    if schedule is None:  # if block decides if we're going to start the repeated method or do a one shot clean up
        scanDir(dict, dispatchDir)
    else:
        sched = schedule * 60
        repeater(sched, dict, dispatchDir)



# path is typically '/syslog/apps/splunk/var/run/splunk/dispatch' but different splunk installations will put it diff
# it will find the dispatch directory as long as this .py script is in the splunk/bin  , app/<arbitrary>/bin. or
#splunk/var/run/dispatch

def pathFinder():
    global dispatchDir
    currentPath=os.path.realpath(__file__)
    parent_1=os.path.basename(os.path.dirname(currentPath))
    parent_2=os.path.basename(os.path.dirname(os.path.dirname(currentPath)))

    if parent_1 == 'bin':
        if parent_2 == 'splunk':
            dispatchDir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),'var/run/splunk/dispatch')
        elif parent_2 == 'Dispatch Cleanup':
            dispatchDir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))),'var/run/dispatch')
        elif parent_2 == 'jobmanager':

            dispatchDir=os.path.join(os.path.dirname(currentPath),'dispatch')
    return dispatchDir



def scanDir(dict, dispatchDir):
    global list_of_stuff
    list_of_stuff = []
    logging.info("Running down the list in" + dispatchDir)
    try:
        d = os.listdir(dispatchDir)
    except:
        logging.info("directory doesnt exist")
        exit()
    else:
        for dir in d:
            jobpath = (dispatchDir + '/' + dir)
            logging.info("First Job to be examined is: " + dir)
            try:
                jobstat = open(jobpath + "/status.csv")

            except FileNotFoundError:
                logging.info(jobpath + "/status.csv file doesnt exist")

            except OSError:
                logging.info("Error opening up " + jobpath + "/status.csv")

            else:
                reader = csv.DictReader(jobstat)
                delcheck = False
                for r in reader:
                    logging.info('In ' + jobpath + ' job. Examining first line: ')
                    logging.info(r)
                    total = 0
                    for k in dict:
                        for v in dict[k]:

                            if r[k] == v and r['state'] == 'DONE':
                                total += 1
                                logging.info(k + ':' + v + ' matched with  ' + jobpath + '\'s ' + k + ':' + r[k])
                            else:
                                logging.info(k + ':' + v + ' did not match with  ' + jobpath + '\'s ' + k + ':' + r[k])

                    if total == len(dict.keys()):
                        delcheck = True

                if delcheck:
                    logging.info(dir + " job matches the delCheck. It is marked for deletion")
                    list_of_stuff.append(jobpath)
                logging.info("The list of Marked jobs are: " + ','.join(list_of_stuff))

        for d in list_of_stuff:
            logging.info('scan across dispatch directory is complete. Files ' + d + ' will be deleted')
            print(d)
            # shutil.rmtree(folder,ignore_errors=True)


def repeater(sched, d, p):
    scanDir(d, p)
    threading.Timer(sched, repeater, [sched, d, p]).start()


# System argument will take Username, Saved Search Name, APP,
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename='dirdeletion.log')
    logging.info('Script ran')
    userParam()




