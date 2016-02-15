# Takes one or several text files, comma separated, from the IEM ASOS/AWOS
#   data feed at http://mesonet.agron.iastate.edu/request/download.phtml
#   and calculates wind chill for each observation.
# After the computation of wind chill is completed, a new csv file is written
#   containing all the data processed. That file may be quite large depending
#   on the period of time processed.



def windchill(t, w):
    '''
    windchill calculates the wind chill for a given temperature and wind
    speed.
    
    Inputs:
    -------
    Note: Code will attempt to cast 't', 'w' into appropriate types
    t       float       Ambient air temperature in degrees Fahrenheit
    w       int         Wind speed or gust in knots
    
    
    Returns:
    -------
    int     Calculated wind chill for given temperature and wind speed
    '''
        
    # Test inputs, reutrn or throw errors.
    
    # Test for missing value
    if t == 'M' or w == 'M':
        
        # If either temperature or wind speed are missing, return 'NA'
        
        return 'NA'
    
    # Test for invalid types
    try:
        t = float(t)
    except:
        print 'Invalid temperature'
        raise
    
    try:
        w = int(round(float(w) * 1.15078))      # Convert knots to mph, round result
    except:
        print 'Invalid wind value'
        raise
    
    # Mathify and return results.
    if t > 50:
        return 'NA'     # Wind chill is not defined for air temps above 50*F
    elif w <= 3:
        wc = round(t)   # Wind chill is not defined for wind speeds of 3 mph or less
    else:
        wc = round((35.74 + (0.6215 * t) - (35.75 * (w**0.16)) + (0.4275 * t * (w ** 0.16))))
    
    return int(wc)

# END "def windchill(t, w)"



def main():

    from os import path
    
    rootdir = path.join(r'f:\\', r'User_Folders', r'kevin.huyck', r'cases')
    
    infiles = ['DLH-2000-2002.txt', 'DLH-2003-2007.txt','DLH-2008-2016-0211.txt']
    datums = []
    
    of = open(path.join(rootdir, "DLH-wc.csv"), 'w')
    of.write('station, valid, tmpf, dwpf, wchill, relh, drct, sknt, ' + \
                        'p01i, alti, mslp, vsby, gust, skyc1, skyc2, ' + \
                        'skyc3, skyc4, skyl1, skyl2, skyl3, skyl4, ' + \
                        'presentwx, metar' + '\n')
    
    for filestring in infiles:
        
        columns = []
        
        try:
            rf = open(path.join(rootdir, filestring), 'r')
            while True:
                line = rf.readline()
                
                if line == '':
                    break
                    
                elif line.strip()[0] == '#':
                    continue
                
                elif line.strip()[0:7] == 'station':
                    continue
                
                else:
                    station, valid, tmpf, dwpf, relh, drct, sknt, p01i, \
                            alti, mslp, vsby, gust, skyc1, skyc2, skyc3, \
                            skyc4, skyl1, skyl2, skyl3, skyl4, presentwx, \
                            metar = line.strip().split(',')
                    of.write(station + ',' + \
                             valid + ',' + \
                             tmpf + ',' + \
                             dwpf + ',' + \
                             str(windchill(tmpf, sknt)) + ',' + \
                             relh + ',' + \
                             drct + ',' + \
                             sknt + ',' + \
                             p01i + ',' + \
                             alti + ',' + \
                             mslp + ',' + \
                             vsby + ',' + \
                             gust + ',' + \
                             skyc1 + ',' + \
                             skyc2 + ',' + \
                             skyc3 + ',' + \
                             skyc4 + ',' + \
                             skyl1 + ',' + \
                             skyl2 + ',' + \
                             skyl3 + ',' + \
                             skyl4 + ',' + \
                             presentwx + ',' + \
                             metar + ',' + \
                             '\n')
            rf.close()
        except:
            raise
    
    # Close output file
    of.close()

# END "def main():"



if __name__ == "__main__":
    
    # A wrapper to get around the temporary poor file structure on the HMT machine
    from sys import prefix, exit
    from os import system, path
    if 'ArcGIS' in prefix and path.exists('C:\Python27\python.exe'):
        from subprocess import call
        _path = path.realpath(__file__)
        # TESTING! Print the path variable
        # print _path
        # system('cmd /k "C:\Python27\python.exe %s' % _path)
        call(['cmd', '/C', 'C:\Python27\python.exe %s' % _path])
        exit
    else:
        # TESTING! Print whether we went straight through or had a small diversion
        # print 'Straight-through'
        main()

# END "if __name__ == "__main__""