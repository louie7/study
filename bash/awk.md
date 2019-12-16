Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [I. tips](#i-tips)
      * [1. variable usage/assign in awk](#1-variable-usageassign-inawk)
   * [II. instance](#ii-instance)
      * [1. <a href="https://www.gnu.org/software/gawk/manual/html_node/Quoting.html" rel="nofollow">print single quota in awk </a>](#1-print-single-quota-in-awk-)
      * [2.  Generate valgrind mapping files by calling external 'sh' pipe](#2--generate-valgrind-mapping-files-by-calling-external-sh-pipe)
      * [3. regression log file parse](#3-regression-log-file-parse)
      * [4.  redirecting output of print and printf into file (print items &gt; output-file )](#4--redirecting-output-of-print-and-printf-into-file-print-items--output-file-)
      * [5.  replace specified column from other file](#5--replace-specified-column-from-other-file)
      * [6.  find the record didn't exist in 'new.txt' file](#6--find-the-record-didnt-exist-in-newtxt-file)
      * [7.  find the previous line in the pattern](#7--find-the-previous-line-in-the-pattern)
      * [8.  compare file1 1<del>4 char with file2 2</del>5, if they are same, merge file2 2nd column and file1](#8--compare-file1-14-char-with-file2-25-if-they-are-same-merge-file2-2nd-column-and-file1)


# I. tips #
## 1. variable usage/assign in awk 
```bash
## make awk use different var when parsing different files
awk '{ program that depends on s }' s=1 file1 s=0 file2 

awk '{print a, b}' a=111 file1 b=222 file2
##  file1 could NOT use b=222 
##  BEGIN{} block only could use the var from -v assignment

awk -v a='a.*'  '{sub(a,"");print}' xx
awk –v "a=$var1" –v "b=$var2" '{print a,b}' yourfile

## print single quota
awk -v hq="'" '{print $1,$2, hq $3 hq}'

## print external shell variable
awk '{print "'"$LOGNAME"'"}' yourfile
luyi

```
 
 

# II. instance #
## 1. [print single quota in awk ]( https://www.gnu.org/software/gawk/manual/html_node/Quoting.html)
to construct sync cmd for odd filename or directory name to do force sync
```bash
awk -v q="'" '{d=gensub(/(.+\/).+/,"\\1",1,$0); f=gensub(/.+\//,"",1,$0); printf "cd %s%s%s && p4 sync -f %s%s%s \n",q,d,q,q,f,q}' odd_filename.log  > sync.cmd
```


## 2.  Generate valgrind mapping files by calling external 'sh' pipe 
    print items | command
    It is also possible to send output to another program through a pipe instead of into a file.
 ```bash
   awk ’{ print $1 > "names.unsorted"
                       command = "sort -r > names.sorted"
                       print $1 | command }’ BBS-list
 ```
 
 Advanced Notes: Piping into sh
 A particularly powerful way to use redirection is to build command lines and pipe them into the shell, sh. 
 ```bash
 { printf("mv %s %s\n", $0, tolower($0)) | "sh" }
      END { close("sh") }
 ```

```bash
awk -F':' '/golden/{t=gensub(/^ +\(/,"",1,$1); printf ("ls /disk_path/Reg_valgrind_sps_3311633/%s/output/CC*valgrind.log\n", t) | "sh"}END{close ("sh")}' Passed.latest  Failed.latest   > /<disk_path>/val_mapping.txt  
awk '{t=gensub(/.*\/golden\/(.*)\/output.*/,"\\1",1,$0); print $0, t; }'  /<disk_path>/val_mapping.txt > val_mapping.txt
```

## 3. regression log file parse  
```bash
## get the case(s) which is rerun PASS
awk -F':' 'NR==FNR{if ( $0 ~ /EC:/){ i_tc=gensub("[[:space:]]+\\(","",1,$1);  a[i_tc] }} NR>FNR {if ( $0 ~ /, /){tc=gensub("[[:space:]]+\\(","",1,$1); if ((tc in a)){ print tc } }} ' Immrun.txt Passed.latest

##  check failure cases' Errors in the stdout file
awk -F':' '{ if ($0 ~ /golden/ && $NF ~ /FAIL/ ){t=gensub("\\(","",1,$1); print t } } '   Failed.txt | awk -F'/' '{printf "%s/%s.step.stdout\n", $0,$NF}' | xargs grep -Hn  'Error:'

## get failure case which is not in the reference set
gawk -F':'  'BEGIN{ regex="[[:space:]]+\\(nightly\\/" }; NR==FNR{ a[$1]=1 }  NR>FNR{if ($0 ~ regex){f=gensub(regex,"","1", $1); if  (! (f in a) ){print f, $(NF-1), $NF  }  }}'   <ref_path>/Failed.latest   Failed.latest


```

## 4.  redirecting output of print and printf into file (print items > output-file )
```bash
awk -v RS='Error ends' '{printf( " %s \n", $0) > NR"file.txt"  } ' <path_file>
```

## 5.  replace specified column from other file
```bash
    awk 'FILENAME=="a.dat"{a[FNR]=$0} FILENAME=="b.dat"{$3=a[FNR];print}' a.dat b.dat
    awk 'NR==FNR{a[NR]=$1} NR>FNR{if (FNR in a) $3=a[FNR];print}' a.dat b.dat    

```
 
## 6.  find the record didn't exist in 'new.txt' file
```bash
    awk 'FILENAME=="old.txt" {a[$2]=$0} FILENAME=="new.txt" { if (!($2 in a)) print $0 }' old.txt new.txt    
    awk -F';' 'FILENAME=="CaseId.log" {a[$1]=1} FILENAME=="XScaselist.log" { if (($1 in a)) {print $0} }' CaseId.log XScaselist.log
```
   
## 7.  find the previous line in the pattern
```bash
# 某个模式和它的之前的某一行,这里是之前的第3行
awk '/vPattern/&&NR>2{print a[NR%3]"\n"$0}{a[NR%3]=$0}' 
```


## 8.  compare file1 1~4 char with file2 2~5, if they are same, merge file2 2nd column and file1
```bash
awk  'NR==FNR{a[substr($1,2,5)]=$2} NR>FNR&&a[b=substr($1,1,4)]{print $0, a[b]}' file2 file1
```

 
 

