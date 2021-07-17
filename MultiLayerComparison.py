from typing import Sequence
import numpy as np
from array import *
import subprocess
import re
import nltk
import string

def multiLayerComparison(fname1,fname2):
    ## LAYER 1 
    # INDENTATION COMPARISON 
    '''
    This code compares two text files for similarity based on the degree of indent match.
    fname1, fname2 are the two files being compared. Change path accordingly
    '''
    def lcs(seq1 , seq2):
        n1 = len(seq1)                                                               #Length of sequences (n2>=n1)   
        n2= len(seq2)
        L = [[0 for seq1 in range(n2+1)] for iter in range(n1+1)]                    #Create 2D array to store values
        for iter1 in range(n1+1):
            for iter2 in range(n2+1):
                if iter1 == 0 or iter2 == 0 :
                    L[iter1][iter2] = 0
                elif seq1[iter1-1] == seq2[iter2-1]:                                #If elements match
                    L[iter1][iter2] = 1+L[iter1-1][iter2-1]
                else:
                    L[iter1][iter2] = max(L[iter1-1][iter2] , L[iter1][iter2-1])    #If elements do not match
        return L[n1][n2]                                                            #Return length of LCS
    # fname1=r'./original.txt'                              #Path for original file
    # fname2=r'./copy.txt'                                  #Path for file that is being checked for plagiarism (copy)

    def identComparison(fname1, fname2):        
        #Read files
        f1=open(fname1,'r')
        f2=open(fname2,'r')
        #Array containing size of indent for each line 
        space1=[]
        space2=[]

        #Generate indent size sequence for original file
        for line1 in f1:
            ct=0
            index=0
            for char1 in line1:
                if char1==' ':
                    ct+=1
                else:
                    break
            space1.append(ct)
            index+=1

        #Generate indent size sequence for copy file
        for line2 in f2:
            ct=0
            index=0
            for char2 in line2:
                if char2==' ':
                    ct+=1
                else:
                    break
            space2.append(ct)
            index+=1

        #Print sequence of indents for both files
        print(space1)
        print(space2)
        indentmatch=lcs(space1,space2)/len(space1)                                          #Calculate Percentage indent match
        print("Percentage Indent Match = ",100*indentmatch,'%')

    # VARIABLE AND OPERATOR COUNT COMPARISON
    ''' This function is intended to perform variable and opeartor count on both the codefiles in an order to determine their variable and operator
    percentage match '''
    def varAndOperCount(fname1, fname2):
        codefile1=[]
        codefile2=[]

        # Reading the code file and filtering out unnecessary symbols.
        for line in open(fname1,'r'):
            codefile1.append(line.strip(';').strip('\n').strip().strip('{').strip('}').strip('#').strip('').strip('(').strip(')').strip(',').strip("''"))
        for line in open(fname2,'r'):
            codefile2.append(line.strip(';').strip('\n').strip().strip('{').strip('}').strip('#').strip('').strip('(').strip(')').strip(',').strip("''"))

        coderef1=[]
        coderef2=[]
        # Performing split on each of the string for easy comparison
        for word in codefile1:
            coderef1.append(word.split())
        for word_ in codefile2:
            coderef2.append(word.split())

        # All Operators are considered. Just remove whatever you don't want
        count={'int':0,'float':0, 'char':0, 'short':0, 'long':0, 'double':0, '=':0, '+':0, '-':0, '*':0, '%':0, '/':0, '++':0, '--':0, '==':0, '!=':0, '>':0, '<':0, '<=':0, '>=':0, '&&':0, '!':0, '||':0, '&':0, '|':0, '^':0, '~':0, '<<':0, '>>':0, '+=':0, '-=':0, '*=':0, '/=':0, '^=':0, '%=':0, '&=':0}

        # Comparing each items in code file and storing the occurance count in above dictionary.
        count1=count
        count2=count
        countfname1=0
        countfname2=0
        for elements in coderef1:
            for items in elements:
                for key in count1.keys(): 
                    if items == key or items.startswith(key):
                        count1[key] += 1
                        countfname1 += 1
        for elements in coderef2:
            for items in elements:
                for key in count2.keys(): 
                    if items == key or items.startswith(key):
                        count2[key] += 1
                        countfname2 += 1

        similarity=0
        for elem in (count1 and count2):
            similarity +=1

        print("Percentage Variable and Operator Count Match = ",(similarity*100)/len(countfname1),'%')

    ## LAYER 2
    #  EXE COMPARISON
    def exe_comp(fname1, fname2):
        file_o = fname1
        file_t = fname2
        '''
        Compares the compiled exes of the two source codes to check for plagiarism.
        file_o, file_t are names of the files to be compared, without extensions, as strings. o is original, t is the one to be tested.
        Returns true for plagiarised (>80% match), else false.
        file_o must not be considerably larger than file_t, because the excess length of one file is also counted in difference.
        '''
        subprocess.call("rm original.out test.out", shell=True, executable='/bin/bash', stderr = subprocess.PIPE)
        subprocess.call("g++ "+file_o+".cpp -o original.out", shell=True, executable='/bin/bash')
        subprocess.call("g++ "+file_t+".cpp -o test.out", shell=True, executable='/bin/bash')

        comp_process = subprocess.Popen('cmp -l original.out test.out', shell=True, executable='/bin/bash', stdout = subprocess.PIPE)
        result, error = comp_process.communicate()
        differ = re.findall(r'\\n', str(result))
        num_diff = len(differ)
        with open('test.out', 'rb') as f:
            total_t = len(f.read())
        with open('original.out', 'rb') as f:
            total_o = len(f.read())
        perc = (1-num_diff/total_t)*100
        print("Percentage Exe Match = ",perc,'%')
        # if perc>80:
        #     return True
        # else:
        #     return False

    # KEYWORD SEQUENCE COMPARISON 
    def lcs(a, b):
        tbl = [[0 for B in range(len(b) + 1)] for A in range(len(a) + 1)]
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                tbl[i + 1][j + 1] = tbl[i][j] + 1 if x == y else max(
                    tbl[i + 1][j], tbl[i][j + 1])
        res = []
        i, j = len(a), len(b)
        while i and j:
            if tbl[i][j] == tbl[i - 1][j]:
                i -= 1
            elif tbl[i][j] == tbl[i][j - 1]:
                j -= 1
            else:
                res.append(a[i - 1])
                i -= 1
                j -= 1
        return res[::-1]

    C_Keywords = ['auto', 'double', 'int', 'struct', 'break', 'else', 'long', 'switch', 'case', 'enum', 'register', 'typedef', 'char', 'extern', 'return', 'union', 'continue', 'for', 'signed', 'void', 'do', 'if', 'static', 'while', 'default', 'goto', 'sizeof', 'volatile', 'const', 'float', 'short', 'unsigned' ]

    def keywordSeqCom(fname1, fname2):
        code1 = open(fname1, 'r')
        code2 = open(fname2, 'r')

        keyword_sequence1 = []
        keyword_sequence2 = []
        words1 = []
        words2 = []
        lines1 = ''
        lines2 = ''

        for line in code1:
            lines1 += line.strip()
        for line in code2:
            lines2 += line.strip()

        Lines1 = nltk.sent_tokenize(lines1)
        Lines2 = nltk.sent_tokenize(lines2)

        for line in Lines1:
            words1 += nltk.word_tokenize(line)

        for line in Lines2:
            words2 += nltk.word_tokenize(line)

        for word in words1:
            if word in C_Keywords:
                keyword_sequence1.append(word)

        for word in words2:
            if word in C_Keywords:
                keyword_sequence2.append(word)

        LCS_kw = ''
        LCS_kw = lcs(keyword_sequence1,keyword_sequence2)

        a = len(LCS_kw)
        b = max(len(keyword_sequence1),len(keyword_sequence2))

        matching = (a/b)*100
        print("Percentage Keyword Sequence Match = ",matching,'%')