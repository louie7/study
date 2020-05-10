Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [I. tips](#i-tips)
      * [1.1 variable usage/assign in awk](#11-variable-usageassign-inawk)
      * [1.2 [arrays in awk] (<a href="http://bbs.chinaunix.net/thread-2312439-1-1.html" rel="nofollow">http://bbs.chinaunix.net/thread-2312439-1-1.html</a>)](#12-arrays-in-awk-httpbbschinaunixnetthread-2312439-1-1html)
      * [1.3 [Awk tips, tricks, pitfalls in awk] (<a href="https://catonmat.net/ten-awk-tips-tricks-and-pitfalls#awk_shorten_pipes" rel="nofollow">https://catonmat.net/ten-awk-tips-tricks-and-pitfalls#awk_shorten_pipes</a>)](#13-awk-tips-tricks-pitfalls-inawk-httpscatonmatnetten-awk-tips-tricks-and-pitfallsawk_shorten_pipes)
         * [1.3.1 Here are some examples of typical awk idioms, using only conditions: ](#131-here-are-some-examples-of-typical-awk-idioms-using-only-conditions)
   * [II. instance](#ii-instance)
      * [2.1 <a href="https://www.gnu.org/software/gawk/manual/html_node/Quoting.html" rel="nofollow">print single quota in awk </a>](#21-print-single-quota-in-awk-)
      * [2.2  Generate valgrind mapping files by calling external 'sh' pipe](#22--generate-valgrind-mapping-files-by-calling-external-sh-pipe)
      * [2.3 regression log file parse](#23-regression-log-file-parse)
      * [2.4  redirecting output of print and printf into file (print items &gt; output-file )](#24--redirecting-output-of-print-and-printf-into-file-print-items--output-file-)
      * [2.5  replace specified column from other file](#25--replace-specified-column-from-other-file)
      * [2.6  find the record didn't exist in 'new.txt' file](#26--find-the-record-didnt-exist-in-newtxt-file)
      * [2.7  find the previous line in the pattern](#27--find-the-previous-line-in-the-pattern)
      * [2.8  compare file1 1 to 4 char with file2 2 to 5, if they are same, merge file2 2nd column and file1](#28--compare-file1-1-to-4-char-with-file2-2-to-5-if-they-are-same-merge-file2-2nd-column-and-file1)
      * [2.9  call external bash command to get same duplicate file size based on md5sum](#29--call-external-bash-command-to-get-same-duplicate-file-size-based-on-md5sum)



# I. tips #
## 1.1 variable usage/assign in awk 
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

## 1.2 [arrays in awk] (http://bbs.chinaunix.net/thread-2312439-1-1.html)

## 1.3 [Awk tips, tricks, pitfalls in awk] (https://catonmat.net/ten-awk-tips-tricks-and-pitfalls#awk_shorten_pipes)
### 1.3.1 Here are some examples of typical awk idioms, using only conditions: 
```bash
awk 'NR % 6'            # prints all lines except those divisible by 6
awk 'NR > 5'            # prints from line 6 onwards (like tail -n +6, or sed '1,5d')
awk '$2 == "foo"'       # prints lines where the second field is "foo"
awk 'NF >= 6'           # prints lines with 6 or more fields
awk '/foo/ && /bar/'    # prints lines that match /foo/ and /bar/, in any order
awk '/foo/ && !/bar/'   # prints lines that match /foo/ but not /bar/
awk '/foo/ || /bar/'    # prints lines that match /foo/ or /bar/ (like grep -e 'foo' -e 'bar')
awk '/foo/,/bar/'       # prints from line matching /foo/ to line matching /bar/, inclusive
awk 'NF'                # prints only nonempty lines (or: removes empty lines, where NF==0)
awk 'NF--'              # removes last field and prints the line
awk '$0 = NR" "$0'      # prepends line numbers (assignments are valid in conditions)
```

```bash
## template
awk 'NR==FNR { # some actions; next} # other condition {# other actions}' file1 file2

## prints lines that are both in file1 and file2 (intersection)
## The "next" at the end of the first action block is needed to prevent the condition in "# other condition" from being evaluated, and the actions in "# other actions" from being executed while awk is reading the first file.
awk 'NR==FNR{a[$0];next} $0 in a' file1 file2

# use information from a map file to modify a data file
awk 'NR==FNR{a[$1]=$2;next} {$3=a[$3]}1' mapfile datafile

## TODO


```


# II. instance #
## 2.1 [print single quota in awk ]( https://www.gnu.org/software/gawk/manual/html_node/Quoting.html)
to construct sync cmd for odd filename or directory name to do force sync
```bash
awk -v q="'" '{d=gensub(/(.+\/).+/,"\\1",1,$0); f=gensub(/.+\//,"",1,$0); printf "cd %s%s%s && p4 sync -f %s%s%s \n",q,d,q,q,f,q}' odd_filename.log  > sync.cmd
```


## 2.2  Generate valgrind mapping files by calling external 'sh' pipe 
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

## 2.3 regression log file parse  
```bash
## get the case(s) which is rerun PASS
awk -F':' 'NR==FNR{if ( $0 ~ /EC:/){ i_tc=gensub("[[:space:]]+\\(","",1,$1);  a[i_tc] }} NR>FNR {if ( $0 ~ /, /){tc=gensub("[[:space:]]+\\(","",1,$1); if ((tc in a)){ print tc } }} ' Immrun.txt Passed.latest

##  check failure cases' Errors in the stdout file
awk -F':' '{ if ($0 ~ /golden/ && $NF ~ /FAIL/ ){t=gensub("\\(","",1,$1); print t } } '   Failed.txt | awk -F'/' '{printf "%s/%s.step.stdout\n", $0,$NF}' | xargs grep -Hn  'Error:'

## get failure case which is not in the reference set
gawk -F':'  'BEGIN{ regex="[[:space:]]+\\(nightly\\/" }; NR==FNR{ a[$1]=1 }  NR>FNR{if ($0 ~ regex){f=gensub(regex,"","1", $1); if  (! (f in a) ){print f, $(NF-1), $NF  }  }}'   <ref_path>/Failed.latest   Failed.latest

```

## 2.4  redirecting output of print and printf into file (print items > output-file )
```bash
awk -v RS='Error ends' '{printf( " %s \n", $0) > NR"file.txt"  } ' <path_file>
```

## 2.5  replace specified column from other file
```bash
    awk 'FILENAME=="a.dat"{a[FNR]=$0} FILENAME=="b.dat"{$3=a[FNR];print}' a.dat b.dat
    awk 'NR==FNR{a[NR]=$1} NR>FNR{if (FNR in a) $3=a[FNR];print}' a.dat b.dat    

```
 
## 2.6  find the record didn't exist in 'new.txt' file
```bash
    awk 'FILENAME=="old.txt" {a[$2]=$0} FILENAME=="new.txt" { if (!($2 in a)) print $0 }' old.txt new.txt    
    awk -F';' 'FILENAME=="CaseId.log" {a[$1]=1} FILENAME=="XScaselist.log" { if (($1 in a)) {print $0} }' CaseId.log XScaselist.log
```
   
## 2.7  find the previous line in the pattern
```bash
# 某个模式和它的之前的某一行,这里是之前的第3行
awk '/vPattern/&&NR>2{print a[NR%3]"\n"$0}{a[NR%3]=$0}' 
```


## 2.8  compare file1 1 to 4 char with file2 2 to 5, if they are same, merge file2 2nd column and file1
```bash
awk  'NR==FNR{a[substr($1,2,5)]=$2} NR>FNR&&a[b=substr($1,1,4)]{print $0, a[b]}' file2 file1
```


## 2.9  call external bash command to get same duplicate file size based on md5sum 
```bash
find dir/ -name '*' -type f -print0 | xargs -0 -n2 -P2 -I{} /usr/bin/md5sum "{}" > file_md5.txt
awk '{
        if ($1 in a) { a[$1] = sprint("%s\t%s\t", a[$1], $2); d[$1]=a[$1]; 
            if (c[$1] = 1){ cmd=sprintf("%s \"%s\" ", "du", $2); cmd | getline sizeinf; close(cmd);
                size=gensub(/(.*)\s+.+/, "\\1", 1, sizeinfo); };
                s[$1] = size;
                c[$1] += 1;
        } else {
            a[$1] = $2; c[$1] += 1;
        }
    }
    END{
        printf "Count\tWaste\tMD5\tTests\n";
        for (m in d){
            printf "%d\t%d\t%s\t%s\n", c[m], s[m]*c[m], m, d[m]
            }
    }
    ' file_md5.txt
```

 
 

