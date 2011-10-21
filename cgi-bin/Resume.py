# This file defines a class for printing out a LaTeX resume

class Resume:
    def __init__(self,name,title,tel,email,add1,add2):
        self.name = name
        self.title = title
        self.tel = tel
        self.email = email
        self.add1 = add1
        self.add2 = add2
        self.sections = []

    def print_resume(self,outstream):
        outstream.write(self.boilerplate_beginning()+'\n')
        outstream.write(self.header()+'\n')
        for s in self.sections:
            outstream.write(str(s)+'\n')
        outstream.write(self.boilerplate_end()+'\n')

    def add_section(self,section):
        self.sections.append(section)

    def header(self):
        return r"""
\newcommand{\myheader}{
\begin{tabular*}{1.006\textwidth}{l@{\extracolsep{\fill}}r}
	\textbf{{\LARGE %(name)s}}  & %(title)s\\
	%(add1)s &  Tel: %(tel)s\\
	%(add2)s &  Email: %(email)s \\
\end{tabular*}
\\
\vspace{0.1in}}

\myheader
""" % {'name':self.name,'title':self.title,'tel':self.tel,'email':self.email,'add1':self.add1,'add2':self.add2}

    def boilerplate_beginning(self):
        return r"""
% resume.tex
%
% (c) 2002 Matthew Boedicker <mboedick@mboedick.org> (original author) http://mboedick.org
% (c) 2003 David J. Grant <dgrant@ieee.org> http://www.davidgrant.ca
% (c) 2007 Todd C. Miller <Todd.Miller@courtesan.com> http://www.courtesan.com/todd
% (c) 2009 Derek R. Hildreth <derek@derekhildreth.com> http://www.derekhildreth.com 
% (c) 2009 Joshua S. Hou <jshou@u.washington.edu>
%This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/1.0/ or send a letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.


\documentclass[letterpaper,11pt]{article}

%-----------------------------------------------------------
\usepackage{latexsym}
\usepackage{fullpage}
\usepackage{color}
\usepackage{verbatim}
\usepackage[pdftex]{hyperref}
\usepackage{fancybox}
\hypersetup{
    colorlinks,%
    citecolor=black,%
    filecolor=black,%
    linkcolor=black,%
    urlcolor=black     % can put red here to visualize the links
}
\urlstyle{same}
\definecolor{mygrey}{gray}{.85}
\textheight=9.0in
\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Adjust margins
\addtolength{\oddsidemargin}{-0.375in}
\addtolength{\evensidemargin}{0.375in}
\addtolength{\textwidth}{0.5in}
\addtolength{\topmargin}{-.375in}
\addtolength{\textheight}{0.75in}

%-----------------------------------------------------------
%Custom commands
\newcommand{\resitem}[1]{\item #1 \vspace{-2pt}}

\newcommand{\resheading}[1]{{\large \colorbox{mygrey}{\begin{minipage}{\textwidth}{\textbf{#1 \vphantom{p\^{E}}}}\end{minipage}}}}

%\newcommand{\rescontent}[1]{\colorbox{white}{\begin{minipage}{\textwidth}{#1 \vphantom{p\^{E}}}\end{minipage}}}

\newcommand{\ressubheading}[4]{ % {bold title}{location}{position/degree/GPA}{date}
\begin{tabular*}{\textwidth}{l@{\extracolsep{\fill}}r}
		\textbf{#1} & #2 \\
		\textit{#3} & \textit{#4} \\
\end{tabular*}\vspace{-6pt}}


\newenvironment{section-content}
{\begin{Sbox}\begin{minipage}{\textwidth}\vspace{0.04in}}
{\end{minipage}\end{Sbox}\colorbox{white}{\TheSbox}\vspace{0.1in}}

\newenvironment{graybox}
{\begin{Sbox}\begin{minipage}{\textwidth}\bfseries}
{\end{minipage}\end{Sbox}\colorbox{mygrey}{\TheSbox}}
%-----------------------------------------------------------

\begin{document}
"""

    def boilerplate_end(self):
        return r'\end{document}'

class Text:
    def __init__(self,name,fields): # fields should be a length one list with a textfield in it
        self.name = name
        self.text = fields[0]

    def __str__(self):
        return r"""
\resheading{%(name)s}
	\begin{section-content}
    %(text)s
	\end{section-content}
""" % {'name':self.name, 'text':self.text}

class Description:
    def __init__(self,name,fields):
        self.name = name
        self.descriptions = []
        
        description_header = ''
        curr_header_used = True
        for (field,value) in fields:
            if field.startswith("description-header"):
                if curr_header_used==False:
                    self.descriptions.append((description_header,''))
                    curr_header_used = True
                description_header = value
                curr_header_used = False
            elif field.startswith("description-content"):
                self.descriptions.append((description_header,value))
                description_header = ''
                curr_header_used = True
        # last section
        if curr_header_used==False:
            self.descriptions.append((description_header,''))
            curr_header_used = True

    def __str__(self):
        top = r'''\resheading{%s}
                  \begin{section-content}
                  \begin{description}''' % self.name
        end = r'''\end{description}
                  \end{section-content}'''
        middle = '\n'.join([r'\item[%s] {\footnotesize %s}' % (header,descr) for (header,descr) in self.descriptions])
        return top+middle+end

class Institutions:
    def __init__(self,name,fields):
        self.name = name
        self.institutions = []

        institution_name = ''
        title = ''
        location = ''
        dates = ''
        description = ''

        for (field,value) in fields:
            if field.startswith("resume-institution-name"):
                # add an institution to the list, clear out old institution
                if institution_name:
                    self.institutions.append(Institution(institution_name,title,location,dates,description))
                institution_name = ''
                title = ''
                location = ''
                dates = ''
                description = ''
                # start the new institution
                institution_name = value
            elif field.startswith("resume-institution-title"):
                title = value
            elif field.startswith('resume-institution-location'):
                location = value
            elif field.startswith('resume-institution-dates'):
                dates = value
            elif field.startswith('resume-institution-description'):
                description = value
        # last section, add this institution to the list
        self.institutions.append(Institution(institution_name,title,location,dates,description))

    def __str__(self):
        top = r'''\resheading{%s}
                  \begin{section-content}''' % self.name
        end = r'''\end{section-content}'''
        middle = '\n'.join([str(i) for i in self.institutions])
        return top+middle+end

class Institution:
    def __init__(self,name,title,location,dates,description):
        self.name = name
        self.title = title
        self.location = location
        self.dates = dates
        self.description = description

    def __str__(self):
        return r"""
        \ressubheading{%(name)s}{%(location)s}{%(title)s}{%(date)s}
        {\footnotesize
            \begin{itemize}
            \resitem{%(description)s}
            \end{itemize}
        }
""" % {'name':self.name, 'location':self.location, 'title':self.title, 'date':self.dates, 'description':self.description}
