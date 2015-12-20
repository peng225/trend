#!/usr/bin/python

import math
import string
import datetime

# Normal distribution.
def norm_dist(sigma, x):
    return math.exp(-(x**2)/(2.0 * (sigma**2)))

def read(input_file):
    # Open input and output files.
    fin = open(input_file)
    lines = fin.readlines()
    fin.close()
    date = []
    value = []

    # Get raw date information.
    for line in lines:
        words = line.split()
        # Get date.
        raw_date = words[0].split('/')
        year = int(raw_date[0])
        month = int(raw_date[1])
        day = int(raw_date[2])
        date.append(datetime.date(year, month, day))

        # Get value.
        value.append(int(words[1]))

    return date, value

def datewrite(output_file, date, values):
    fout = open(output_file, 'w')
    for i in range(len(date)):
        fout.write(str(date[i]).replace("-", "/"))
        for j in range(len(values)):
            fout.write(" " + str(values[j][i]))
        fout.write("\n")
    fout.close()

def write(output_file, values):
    fout = open(output_file, 'w')
    for i in range(len(values[0])):
        fout.write(str(i))
        for j in range(len(values)):
            fout.write(" " + str(values[j][i]))
        fout.write("\n")
    fout.close()


def trend(date, value, verbose):
    ROUND_DIGIT = 2
    VALID_DIFF = 21  # Three weeks.
    ovalue = []

    # Iterate over all date information
    for i in range(len(date)):
        if verbose:
            print ""
            print "i: " + str(i)
        cnt = 0.0
        avg = 0.0
        after_3week_point = i
        for k in range(i, len(date)):
            date_diff = (date[k] - date[i]).days
            if VALID_DIFF < date_diff:                
                break
            else:
                after_3week_point = k
        if verbose:
            print "After 3 week point: " + str(after_3week_point)
        # Iterate over the range [0. i] from backward.
        for j in list(reversed(range(after_3week_point + 1))):
            date_diff = (date[i] - date[j]).days
            if verbose:
                print "j: " + str(j)
                print "date diff: " +  str(date_diff)
            abs_date_diff = abs(date_diff)
            if abs_date_diff <= VALID_DIFF:
                # words = lines[j].split()
                coeff = norm_dist(VALID_DIFF/2.0, abs_date_diff)
                avg += float(value[j]) * coeff
                cnt += coeff
                if verbose:
                    print "coeff: " + str(coeff)
                    print "dat: " + str(float(words[-1]))
                    print "Added " + str(float(words[-1]) * coeff)
            else:
                if verbose:
                    print "break"
                break
        avg /= cnt
        ovalue.append(round(avg, ROUND_DIGIT))
        if verbose:
            print "Finally added " + str(round(avg, ROUND_DIGIT))
            print ovalue[i]
    return ovalue


# Other than trend
def others(value, trend):
    ovalue = []
    # val_avg = sum(value) / len(value)

    for i in range(len(value)):
        ovalue.append(value[i] - trend[i])
        
    return ovalue

def autocorrel(date, oths, fgetmid):
    ROUND_DIGIT = 3
    completed_val = []
    completed_date = []
    for i in range(len(date) - 1):
        date_diff = (date[i + 1] - date[i]).days
        for j in range(date_diff):
            dmid = date[i] + datetime.timedelta(days = j)
            completed_date.append(dmid)
            completed_val.append(fgetmid(date[i], dmid, date[i + 1], oths[i], oths[i + 1]))
                
    completed_date.append(date[-1])
    completed_val.append(oths[-1])

    acrel = [0 for i in range(len(completed_val) / 2)]
    for tau in range(len(completed_val) / 2):
        for i in range(len(completed_val) - tau):
            acrel[tau] += completed_val[i] * completed_val[i + tau]
        acrel[tau] = math.sqrt(abs(acrel[tau])) * sign(acrel[tau])
        acrel[tau] /= (len(completed_val) - tau)
        acrel[tau] = round(acrel[tau], ROUND_DIGIT)
        
    return acrel

def linearmid(dleft, dmid, dright, vleft, vright):
    return (float)(vleft * (dright - dmid).days + vright * (dmid - dleft).days) / (dright - dleft).days

def stairmid(dleft, dmid, dright, vleft, vright):
    return vleft

def sign(val):
    if val >= 0:
        return 1.0
    else:
        return -1.0
