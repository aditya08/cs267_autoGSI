'''
Copyright 2018 Aditya Devarakonda

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

PROGRAM BEHAVIOR DISCLAIMER:
    1. This program automatically sends SSL-encrypted emails to a list of people and depends on students' names on the Pre-course survey CSV file and group assignment CSV file to be identical. This program further assumes that student email addresses are correctly entered into the Pre-course survey. Any errors with student email addresses will result in undefined behavior.
    
    2. Test this program before you use it for its intended purpose.

'''

import pandas as pd, numpy as np
import smtplib, argparse, getpass
import sys, time

parser = argparse.ArgumentParser(description='CS267 Automated Group Emailing Script')
parser.add_argument('roster', metavar='ROSTER', help='Path to the class roster (currently, only CSV format allowed)')
parser.add_argument('groups', metavar='GRPS', help='Path to the groups file (currently, only CSV format allowed)')

def group_emails(roster, groups):
    dfr = pd.read_csv(roster)
    dfr = dfr[['Name', 'Preferred E-mail address']]

    npr = dfr.values
    dfg = pd.read_csv(groups, header=None)
    npg = dfg.values
    [ngroups, nstudents] = npg.shape
    
    listofgroups = []
    addrs_in_group = []
    for i in range(ngroups):
        for j in range(len(npg[i])):
            try:
                loc = np.where(npr[:,0] == npg[i,j])[0][0]
                addrs_in_group.append(npr[loc,1])
            except:
                break
        #print(addrs_in_group)
        #print('\n')
        #time.sleep(0.5)
        listofgroups.append(addrs_in_group[:])
        addrs_in_group = []
    return listofgroups

def email_groups(emails_by_group):
    FROM = input('Enter your address: ')
    SUBJECT = input('Subject of this email: ')
    print('Type the body of your email: ')
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    TEXT = "\n\n".join(lines)

    print("From:%s Subject:%s Body:%s" % (FROM, SUBJECT, TEXT))
    #Prepare message
    print('There are %d groups' % len(emails_by_group))
    print(emails_by_group)
    password = getpass.getpass(prompt='Please enter your email address password:')
    for i in emails_by_group:
        print(i)
        msg = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ", ".join(i), SUBJECT, TEXT)
        try:
            server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server_ssl.ehlo()
            server_ssl.login(FROM, password)
            server_ssl.sendmail(FROM, i, msg)
            server_ssl.close()
            print('successfully sent the mail')
        except:
            print('SSL send failed. Trying without SSL')
            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.ehlo()
                server.starttls()
                server.login(FROM, password)
                server.sendmail(FROM, i, msg)
                server.close()
                print('successfully sent the mail')
            except:
                print('failed to send mail')
        time.sleep(2)
    return
    
def main():
    
    global args
    args = parser.parse_args()
    emails_by_group = group_emails(args.roster, args.groups)
    email_groups(emails_by_group)

if __name__ == "__main__":
    main()
