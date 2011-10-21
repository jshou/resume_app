#!/usr/bin/python2.5
import os
import sys
import cgi,cgitb
from Resume import *
cgitb.enable()

form = cgi.FieldStorage()
for item in form:
    form[item].value = form[item].value.replace("#",r"\#")
    form[item].value = form[item].value.replace("&",r"\&")

print "Content-Type: text/html;charset=utf-8\r\n\r\n"

#for k in form:
#    print k, form[k]
#    print "<br/>"
#print "<br/>"
#
#for k in form:
#    print k, form[k].value
#    print "<br/>"

required_fields = ['name','tel','email']
for field in required_fields:
    if field not in form:
        print "%s required." % field
        sys.exit(1)

# non required fields
nrf = {'title':'','add1':'','add2':''}
print "Creating resume...<br/><br/>"
for i in nrf:
    if i in form:
        nrf[i] = form[i].value

resume = Resume(form['name'].value, form['title'].value, form['tel'].value,nrf['email'],nrf['add1'],nrf['add2'])

print "Filling in sections...<br/>"
name = ''
fields = []
type = ''
for field in form:
    if field.startswith("section-name"):
        # create old object
        if fields:
            #find out which kind of section,
            if type=="text":
                print "adding text <br/>"
                resume.add_section(Text(name,fields))
            elif type=="description":
                print "adding description<br/>"
                resume.add_section(Description(name,fields))
            elif type=="institution":
                print "adding institution<br/>"
                resume.add_section(Institutions(name,fields))
        # start creating new object
        name = form[field].value
        fields = []
        type = ''
    elif field.startswith("section-text"):
        text = form[field].value
        fields.append(text)
        type = "text"
    elif field.startswith("description"):
        fields.append((field,form[field].value))
        type = "description"
    elif field.startswith("resume-institution"):
        fields.append((field,form[field].value))
        type = "institution"

# creating last object
if fields:
    #find out which kind of section,
    if type=="text":
        print "adding text <br/>"
        resume.add_section(Text(name,fields))
    elif type=="description":
        print "adding description<br/>"
        resume.add_section(Description(name,fields))
        print fields
    elif type=="institution":
        print "adding institution<br/>"
        resume.add_section(Institutions(name,fields))

filename = open('counter').read().strip()
file = open(filename+'.tex','w')
resume.print_resume(file)

next_filename = (int(filename) + 1) % 10
print>>open('counter','w'), next_filename

os.system('pdflatex --shell-escape %s.tex >/dev/null &'%filename)
print "<script type='text/javascript'>window.location='%s.pdf'</script>"%filename
