# I. Lessons #
---
## 1.1 load lib by _do_, _require_ or _use_
[do, require and use definition](https://stackoverflow.com/questions/2180554/in-perl-is-it-better-to-use-a-module-than-to-require-a-file)
Standard practice is to use the most of the time, require occasionally, and do rarely.
A library is just a collection of subroutines; a module provides a namespace, making it far more suitable for reuse.

- do 'file' will execute file as a Perl script. It's almost like calling eval on the contents of the file; if you do the same file multiple times (e.g. in a loop) it will be parsed and evaluated each time which is unlikely to be what you want. The difference between do and eval is that do can't see lexical variables in the enclosing scope, which makes it _safer_. do is occasionally useful for simple tasks like processing a configuration file that's written in the form of Perl code.

- require 'file' is like do 'file' except that it will only parse any particular file __one time__ and will raise an exception if something goes wrong. (e.g. the file can't be found, it contains a syntax error, etc.) The automatic error checking makes it a good replacement for do 'file' but it's still only suited for the same simple uses.

- use Module is the normal way of using code from a module. Note that Module is the package name as a bareword and not a quoted string containing a file name. Perl handles the translation from a package name to a file name for you. use statements happen __at compile time__ and throw an exception if they fail. This means that if a module your code depends on isn't available or fails to load the error will be apparent immediately. Additionally, use automatically calls the import() method of the module if it has one which can save you a little typing.

require Module is like use Module except that it happens at __runtime__ and does __not__ automatically call the module's import() method. Normally you want to use use to fail early and predictably, but sometimes require is better. For example, require can be used to delay the loading of large modules which are only occasionally required or to make a module optional. (i.e. use the module if it's available but fall back on something else or reduce functionality if it isn't.)

Strictly speaking, the only difference between require Module and require 'file' is that the first form triggers the automatic translation from a package name like Foo::Bar to a file name like Foo/Bar.pm while the latter form expects a filename to start with. By convention, though, the first form is used for loading modules while the second form is used for loading libraries.

## 1.2 delay interpolation in a regex to the point of use
http://stackoverflow.com/questions/21759993/how-can-i-delay-variable-interpolation-in-a-regex-to-the-point-of-use

---
~~~

# II. Snippet #
## 2.1 Json encode and decode
```perl
perl  -I lib/perl5/  -MJSON::PP -MData::Dumper -e 'use JSON::PP; $a={a=>1,b=>2,c,asdf,{asdf,2}}; $g=JSON::PP->new->allow_singlequote->allow_barekey->space_after->relaxed->latin1->allow_blessed->convert_blessed; $b=$g->encode($a); print Dumper ($g->decode($b));  '
```

## 2.2 encode to JSON on command line
```perl
perl -MJSON::backportPP  -e  'BEGIN{push @INC, "/u/yilu/SWE_yilu/step/dev/lib/perl5";  while( ($k,$v) = each  %INC){print "$k => $v \n";} exit;}; my $g_json_pp = JSON::PP->new->latin1->space_after->relaxed->allow_singlequote->allow_barekey->indent->allow_blessed(1)->convert_blessed(0); $a={ bbb => 1234 } ;   print $g_json_pp->encode($a);'
```

## 2.3 opendir and readdir in a directory
```perl
## print the items in the dirs by filter some regex pattern
perl -e 'opendir(DH, "/dir2open/XXX"); @f = grep { $_ !~ m/bin*|~$|\.{1,2}$/ } readdir(DH); print "@f";'
```

## 2.4 perl reference/alias usage example 
```perl
## print ENV key value pairs
perl -e '$hashref = *ENV{HASH};  for $k (keys( %{$hashref} )) {print $k,"==>", $$hashref{$k},"\n";}'

## add the key value pairs
perl -e '%$hashref = (KET => "king", BIRD=> "sing"); @$hashref{"KEY1", "KEY2"} = ('AAA', 'BBB'); for $k (keys(%{$hashref})){print $k,"==>",$$hashref{$k},"\n" } ; '
```
## 2.5 Try best to get the absolutely path with readlink way even if there is dead link or inconsistent path
```perl
perl -MCwd=abs_path -MFile::Basename -e '$p = $org = "<path>/D20151234_"; while ( ! -d $r )  { $r=abs_path("$p");   $r=dirname("$p"); $p=$r; }; print $org,"\n"; $real=abs_path($r); ($new=$org) =~ s,$p,$real,; print "New path:", $new  '
```
## 2.6 get env setting from %ENV
```bash
perl -e 'foreach $k (keys %ENV) {print "$k -->  $ENV{$k} \n "}'
```

## 2.7 list all used modules (without condition ones)
```perl
## %INC contains all modules that Perl load by do, require or use
perl -MFile::Path -e ' while( ($k,$v) = each( %INC )){ print $k, $v, "\n";}'
```

## 2.8 grep implement grep as in bash by perl
```perl
#!/usr/bin/perl
use strict;
use warnings;

my $pattern = qr/$ARGV[0]/;
my $file= $ARGV[1];
print "pattern=$pattern\n";

my @lines;
open my $fh, '<', $file or die "unable to open file '$file' for reading : $!";
while(my $line=<$fh>) {
    push @lines, $line if ($line =~ $pattern);
}
close($fh);
print @lines;
```

## 2.9 mapping char to num, use map to construct mapping table
```perl
    perl -e '%h; $n=1; for $i ((a..z)){$h{$i}=$n;$n++}; $s="ab"; @a=reverse split("", $s); $x = 0; $sum=0; for $i (@a){$tmp = $h{$i} * 26 ** $x; print $tmp,"EE"; $sum += $tmp; $x++;}; print $sum;'

    perl -MData::Dumper -e '$n=0;  %h = map {;$n++;  $_ => $n;} (a..z); print Dumper(\%h);   $s="ab";  @a=reverse split("", $s);  $x = 0; $sum=0; for $i (@a){$tmp = $h{$i} * 26 ** $x; $sum += $tmp; $x++;}; print "${s}: is $sum";'
```

---
~~~
# III. Sugar #
## 3.1 one command line prefix with some new feature(experiment)/module
```perl
perl -Mfeature=postderef,say,state -Mstrict -Mwarnings -MData::Dumper -e "print $a;"
```

## 3.2 list core module(s) with naming pattern by Module::CoreList
```perl
perl -MModule::CoreList  -e 'use Module::CoreList; print join "\n", Module::CoreList->find_modules(qr/File/) '
```

## 3.3 chmop safer 'chop'
chomp VARIABLE
chomp( LIST )
chomp:   This safer version of "chop" removes any trailing string that
         corresponds to the current value of `$/` (also known as $INPUT_RECORD_SEPARATOR in the "English" module).
                                                     

## 3.4 call system command with /bin/sh
```perl
## qx/STRING/
## ``
perl -MData::Dumper -e '$o=qx{ls -l }; @a=split(/\n/,$o); print Dumper(\@a); for $i (@a){@b=split(/[ \t]+/, $i); print " $b[-1]";}'
```

> A string which is (possibly) interpolated and then executed as a system command with _/bin/sh_ or its equivalent. 
_Shell wildcards, pipes, and redirections will be honored._ 
The collected standard output of the command is returned; standard error is unaffected. In scalar context, it comes back as a single (potentially multi-line) string, or undef if the command failed. 
_In list context_, returns a list of lines (however you've defined lines with `$/` or $INPUT_RECORD_SEPARATOR ), or an empty list if the command failed.
Because backticks do not affect standard error, use shell file descriptor syntax (assuming the shell supports this) if you care to address this. To capture a command's STDERR and STDOUT together:
```perl
$output = `cmd 2>&1`;
```

## 3.5 concatenate strings efficiently with join
> For concatenating multiple strings all at once, use join. Join is (according to the Camel book) the most efficient way to concatenate many strings together. Join can be used with a delimiter, or with a null string as the delimiter, so that nothing is inserted between the strings that are joined (concatenated) together.
```perl
## join EXPR,LIST
$rec = join(':', $login,$passwd,$uid,$gid,$gcos,$home,$shell);
```

## 3.7 Adjust the time format
```perl
perl  -MPOSIX -e '$file="aa";$sec=(stat($file))[9]; printf "file %s updated at %s\n", $file,  strftime( "%H:%M:%S_%Y/%m/%d", localtime($sec));'
## file aa updated at 08:00:00_1970/01/01 
```

## 3.8 check if the hash is empty
If you evaluate a hash in _scalar_ context, it returns false if the hash is empty.
If there are any key/value pairs, it returns true; more precisely, the value returned is a string consisting of the number of used buckets and the number of allocated buckets, separated by a slash.
This is pretty much useful only to find out whether Perl's internal hashing algorithm is performing poorly on your data set.

## 3.8 get index but when there is duplicated cell, it count the later one
```perl
@teams = qw(Miami Oregon Florida Tennessee Texas Oklahoma Nebraska LSU Colorado Maryland);
%rank = map { $teams[$_] => $_ + 1 } 0 .. $#teams;
```

## 3.9 filter out cells in the array with grep
```perl
## remove duplicated cells in the array with grep
perl -e '@a=('a','b','a','c','d'); @b=sort( @a ); @u=grep {!$_{$_}++} @b; print "@u \n"'

## get duplicated cells in the array with grep
perl -e '@a=("A","B","CC","D","CC"); @d=grep {$h{$_}++} @a; ‘
```

```bash
## remove duplicated cells in path by awk
PATH=`echo -n $PATH | awk -v RS=: '{ if (!arr[$0]++) {printf("%s%s",!ln++?"":":",$0)}}’`

PATH=$(echo "$PATH" | awk -v RS=':' -v ORS=":" '!a[$1]++{if (NR > 1) printf ORS; printf $a[$1]}’) 
```

## 3.10 Get a modified copy of a string without changing the original one
(my $new = $original) =~ s/foo/bar/;

## 3.11 sort the value of the hash by value comparation
In list context, this sorts the LIST and returns the sorted list value.
In scalar context, the behaviour of sort() is undefined.
```perl
foreach my $case ( sort { $tcStatus{$::b} <=> $tcStatus{$::a}}  keys %tcStatus ) {
       printf "CPU Time:%7d  Case:%s \n", $tcStatus{$case},$case;
}
```

We almost always want to sort the keys of the hash. 
```perl
## sort the keys by its associated value. Then get the values (e.g. by using a hash slice).
my @keys = sort { $h{$a} <=> $h{$b} } keys(%h);
my @vals = @h{@keys};
## Or if you have a hash reference.
my @keys = sort { $h->{$a} <=> $h->{$b} } keys(%$h);
my @vals = @{$h}{@keys};
```

In some cases this is OK, in other cases we will want to make sure keys that have the same value will be sorted according the ASCII table. For that case we have the following code:
```perl
foreach my $name (sort { $planets{$a} <=> $planets{$b} or $a cmp $b } keys %planets) {
        printf "%-8s %s\n", $name, $planets{$name};
}

key, ASCII:       foreach my $key (sort                             keys %hash)  { }
key, ASCII:       foreach my $key (sort {       $a  cmp  $b       } keys %hash)  { }
key, numeric:     foreach my $key (sort {       $a  <=>  $b       } keys %hash)  { }
value, ASCII:     foreach my $key (sort { $hash{$a} cmp $hash{$b} } keys %hash)  { }
value, numeric:   foreach my $key (sort { $hash{$a} <=> $hash{$b} } keys %hash)  { }
```

---
~~~






Grep
（一） Grep函数

grep有2种表达方式：

grep BLOCK LIST

grep EXPR, LIST

BLOCK表示一个code 块，通常用{}表示；EXPR表示一个表达式，通常是正则表达式。原文说EXPR可是任何东西，包括一个或多个变量，操作符，文字，函数，或子函数调用。

LIST是要匹配的列表。

grep对列表里的每个元素进行BLOCK或EXPR匹配，它遍历列表，并临时设置元素为$_。
在列表上下文里，grep返回匹配命中的所有元素，结果也是个列表。
在标量上下文里，grep返回匹配命中的元素个数。


（二） Grep vs. loops

open FILE "<myfile" or die "Can't open myfile: $!";

print grep /terrorism|nuclear/i, <FILE>;;

这里打开一个文件myfile，然后查找包含terrorism或nuclear的行。<FILE>;返回一个列表，它包含了文件的完整内容。

可能你已发现，如果文件很大的话，这种方式很消耗内存，因为文件的所有内容都拷贝到内存里了。

代替的方式是使用loop（循环）来完成：

while ($line = <FILE>;) {

        if ($line =~ /terrorism|nuclear/i) { print $line }

}

上述code显示，loop可以完成grep能做的任何事情。那为什么还要用grep呢？答案是grep更具perl风格，而loop是C风格的。

更好的解释是：（1）grep让读者更显然的知道，你在从列表里选择某元素；（2）grep比loop简洁。

一点建议：如果你是perl新手，那就规矩的使用loop比较好；等你熟悉perl了，就可使用grep这个有力的工具。


（三） 几个grep的示例

1. 统计匹配表达式的列表元素个数


$num_apple = grep /^apple$/i, @fruits;

在标量上下文里，grep返回匹配中的元素个数；在列表上下文里，grep返回匹配中的元素的一个列表。

所以，上述code返回apple单词在@fruits数组中存在的个数。因为$num_apple是个标量，它强迫grep结果位于标量上下文里。


2. 从列表里抽取唯一元素

@unique = grep { ++$count{$_} < 2 } qw(a b a c d d e f g f h h);
@unique = grep { ++$count{$_} < 2 } qw(a b a c d d e f g f h h);
print "@unique\n";

上述code运行后会返回：a b c d e f g h
即qw(a b a c d d e f g f h h)这个列表里的唯一元素被返回了。为什么会这样呀？让我们看看：

%count是个hash结构，它的key是遍历qw()列表时，逐个抽取的列表元素。++$count{$_}表示$_对应的hash值自增。在这个比较上下文里，++$count{$_}与$count{$_}++的意义是不一样的哦，
前者表示在比较之前，就将自身值自增1；后者表示在比较之后，才将自身值自增1。
所以，++$count{$_} < 2 表示将$count{$_}加1，然后与2进行比较。$count{$_}值默认是undef或0。
所以当某个元素a第一次被当作hash的关键字时，它自增后对应的hash值就是1，当它第二次当作hash关键字时，对应的hash值就变成2了。变成2后，就不满足比较条件了，所以a不会第2次出现。

所以上述code就能从列表里唯一1次的抽取元素了。


2. 抽取列表里精确出现2次的元素


@crops = qw(wheat corn barley rice corn soybean hay alfalfa rice hay beets corn hay);

@duplicates = grep { $count{$_} == 2 } grep { ++$count{$_} > 1 } @crops;

print "@duplicates\n";


运行结果是：rice


这里grep了2次哦，顺序是从右至左。首先grep { ++$count{$_} >; 1 } @crops;返回一个列表，列表的结果是@crops里出现次数大于1的元素。

然后再对产生的临时列表进行grep { $count{$_} == 2 }计算，这里的意思你也该明白了，就是临时列表里，元素出现次数等于2的被返回。

所以上述code就返回rice了，rice出现次数大于1，并且精确等于2，明白了吧？ :-)


3. 在当前目录里列出文本文件

@files = grep { -f and -T } glob '* .*';
print "@files\n";


这个就很容易理解哦。glob返回一个列表，它的内容是当前目录里的任何文件，除了以'.'开头的。{}是个code块，它包含了匹配它后面的列表的条件。这只是grep的另一种用法，其实与 grep EXPR,LIST 这种用法差不多了。-f and -T 匹配列表里的元素，首先它必须是个普通文件，接着它必须是个文本文件。据说这样写效率高点哦，因为-T开销更大，所以在判断-T前，先判断-f了。


4. 选择数组元素并消除重复

@array = qw(To be or not to be that is the question);

@found_words =
     grep { $_ =~ /b|o/ and ++$counts{$_} < 2; } @array;

     print "@found_words\n";

     运行结果是：To be or not to question

     {}里的意思就是，对@array里的每个元素，先匹配它是否包含b或o字符（不分大小写），然后每个元素出现的次数，必须小于2（也就是1次啦）。

     grep返回一个列表，包含了@array里满足上述2个条件的元素。


     5. 从二维数组里选择元素，并且x<y

# An array of references to anonymous arrays

@data_points = ( [ 5, 12 ], [ 20, -3 ],

                 [ 2, 2 ], [ 13, 20 ] );

@y_gt_x = grep { $_->;[0] < $_->;[1] } @data_points;

foreach $xy (@y_gt_x) { print "$xy->;[0], $xy->;[1]\n" }


运行结果是：

5, 12

13, 20


这里，你应该理解匿名数组哦，[]是个匿名数组，它实际上是个数组的引用（类似于C里面的指针）。


@data_points的元素就是匿名数组。例如：


foreach (@data_points){

        print $_->;[0];}


        这样访问到匿名数组里的第1个元素，把0替换成1就是第2个元素了。


        所以{ $_->;[0] < $_->;[1] }就很明白了哦，它表示每个匿名数组的第一个元素的值，小于第二个元素的值。

        而grep { $_->;[0] < $_->;[1] } @data_points; 就会返回满足上述条件的匿名数组列表。


        所以，就得到你要的结果啦！


        6. 简单数据库查询

        grep的{}复杂程度如何，取决于program可用虚拟内存的数量。如下是个复杂的{}示例，它模拟了一个数据库查询：

# @database is array of references to anonymous hashes

@database = (

    { name      =>; "Wild Ginger",

          city      =>; "Seattle",

                cuisine   =>; "Asian Thai Chinese Korean Japanese",

                      expense   =>; 4,

                            music     =>; "\0",

                                  meals     =>; "lunch dinner",

                                        view      =>; "\0",

                                              smoking   =>; "\0",

                                                    parking   =>; "validated",

                                                          rating    =>; 4,

                                                                payment   =>; "MC VISA AMEX",

                                                                    },

## { ... },  etc.

);


sub findRestaurants {

        my ($database, $query) = @_;

            return grep {

                        $query->;{city} ?

                                    lc($query->;{city}) eq lc($_->;{city}) : 1

                                            and $query->;{cuisine} ?

                                                        $_->;{cuisine} =~ /$query->;{cuisine}/i : 1

                                                                and $query->;{min_expense} ?

                                                                           $_->;{expense} >;= $query->;{min_expense} : 1

                                                                                   and $query->;{max_expense} ?

                                                                                              $_->;{expense} <= $query->;{max_expense} : 1

                                                                                                      and $query->;{music} ? $_->;{music} : 1

                                                                                                              and $query->;{music_type} ?

                                                                                                                         $_->;{music} =~ /$query->;{music_type}/i : 1

                                                                                                                                 and $query->;{meals} ?

                                                                                                                                            $_->;{meals} =~ /$query->;{meals}/i : 1

                                                                                                                                                    and $query->;{view} ? $_->;{view} : 1

                                                                                                                                                            and $query->;{smoking} ? $_->;{smoking} : 1

                                                                                                                                                                    and $query->;{parking} ? $_->;{parking} : 1

                                                                                                                                                                            and $query->;{min_rating} ?

                                                                                                                                                                                       $_->;{rating} >;= $query->;{min_rating} : 1

                                                                                                                                                                                               and $query->;{max_rating} ?

                                                                                                                                                                                                          $_->;{rating} <= $query->;{max_rating} : 1

                                                                                                                                                                                                                  and $query->;{payment} ?

                                                                                                                                                                                                                             $_->;{payment} =~ /$query->;{payment}/i : 1

                                                                                                                                                                                                                                 } @$database;

}

%query = ( city =>; 'Seattle', cuisine =>; 'Asian|Thai' );

@restaurants = findRestaurants(\@database, \%query);

print "$restaurants[0]->;{name}\n";

运行结果是：Wild Ginger

上述code不难看懂，但仙子不推荐使用这样的code，一是消耗内存，二是难于维护了。


简简单单讲map
（一）map函数

map BLOCK LIST
map EXPR, LIST

map函数对LIST里的每个元素按BLOCK或EXPR进行计算，遍历LIST时，临时将LIST里的每个元素赋值给$_变量。
map对每次的计算返回一个结果列表，它在列表上下文里计算BLOCK或EXPR。每个LIST元素可能在输出列表里产生0个，1个，或多个元素。

（仙子注：上文是说遍历每个LIST元素时产生一个结果列表，而不是说总的map结果是个列表，不要搞混了哦。）

在标量上下文里，map返回结果列表的元素数量。在HASH上下文里，输出列表(a,b,c,d...)会变成这样的形式： ( a =>; b, c =>; d, ... )。
假如输出列表的元素数量非对称，那么最后的hash元素的值就是undef了。

避免在BLOCK或EXPR里修改$_，因为这会修改LIST里的元素。另外，避免使用map返回的的列表作为左值，因为这也会修改LIST里的元素。（所谓左值，就是在某个表达式左边的变量。）

（二）Map vs. grep vs. foreach

map跟grep一样，从数组里选择元素。下列2句是一样的：

@selected = grep EXPR, @input;
@selected = map { if (EXPR) { $_ } } @input;

另外，map也是foreach陈述的特殊形式。假如@transformed数组当前未定义或为空，那么下列2句亦相等：

foreach (@input) { push @transformed, EXPR; }
@transformed = map EXPR, @input;

通常，用grep从数组里选择元素，用grep来从数组里选择元素，避用map从数组里转换元素。
当然，数组处理也能使用标准的循环语句来完成(foreach, for, while, until, do while, do until, redo)。

（三）map用法示例

1. 转换文件名为文件大小

@sizes = map { -s $_ } @file_names;

-s是个文件测试操作符，它返回某个文件的size。所以上面这句就返回@file_names数组里每个文件的大小，结果也是个数组。

2. 转换数组到hash：找到某个数组值的索引

代替重复的搜索数组，我们可以用map来转换数组到hash，并通过hash关键字来进行直接查找。如下的map用法相对于重复的数组搜索，更简单高效。

@teams = qw(Miami Oregon Florida Tennessee Texas
            Oklahoma Nebraska LSU Colorado Maryland);
%rank = map { $teams[$_], $_ + 1 } 0 .. $#teams; 
print "Colorado: $rank{Colorado}\n";
print "Texas: $rank{Texas} (hook 'em, Horns!)\n";

打印结果是：
Colorado: 9
Texas: 5 (hook 'em, Horns!)

上述code容易理解哦，0 ..$#teams 是个列表，$#teams代表@teams最后一个元素的下标值（这里是9），所以这个列表就是0-9这几个数了。
map遍历上述列表，将每个列表元素临时设置为$_，并对$_在中间的{}里进行计算；{ $teams[$_], $_ + 1 }，这里每次计算后返回一个2元素的列表，列表结果是某个数组值和对应的数组下标加1，明白了呀？

由于对每个LIST元素进行计算时，都产生一个2元素的列表，所以总的map结果就可看作一个hash了。hash关键字就是数组元素，hash值是对应的数组下标加1。

3. 转换数组到hash：查找拼错单词

转换数组到hash是map最普遍的用法。在本示例里，hash的值是无关紧要的，我们仅检查hash关键字是否存在。

%dictionary = map { $_, 1 } qw(cat dog man woman hat glove);
@words = qw(dog kat wimen hat man gloove);
foreach $word (@words) {
        if (not $dictionary{$word}) {
                    print "Possible misspelled word: $word\n";
                        }
}

打印结果是：
Possible misspelled word: kat
Possible misspelled word: wimen
Possible misspelled word: gloove

看看第1句的map用法，它跟前面示例里的差不多哦。qw()这里是个列表，map对这个列表里的每个元素进行{ $_, 1 }计算，每次计算的结果返回一个2元素的列表，
换句话说，就是%dictionary的key和value呀。所以map最终的结果就是一个hash了，关键字是qw()里的元素，值总是1，无关紧要的。

然后下面的foreach语句就容易了哦，如果@words里的元素不构成%dictionary的关键字的话，就打印一条出错消息。
如果把%dictionary看成标准字典的话，那么就可用它来检验你自己的@words字库里是否有错字了呀。

4. 转换数组到hash：存储选中的CGI参数

hash通常是存储传递给程序或子函数的参数的最便利的方法，而map通常是创建这个hash的最便利的方法。

use CGI qw(param);
%params = map { $_, ( param($_) )[0] }
              grep { lc($_) ne 'submit' } param();
              %params = map { $_, ( param($_) )[0] } grep { lc($_) ne 'submit' } param();
              这里你可能要了解一下CGI模块的基本知识哦。param()调用返回CGI参数名的列表；param($_)调用返回指定的CGI参数名的值。
              假如param($_)返回某个CGI参数的多个值，那么( param($_) )[0]只取第一个值，以便hash仍被良好定义。

              上述code的意思是，将param()的结果作为输入列表，它的元素是多个CGI参数名，然后从这些参数名里grep出参数名不等于'submit'的，结果是一个临时列表，
              map的{ $_, ( param($_) )[0] }语句再次遍历这个临时列表，并获取到参数名，和对应的参数值，将结果赋给%params。
              所以%params里就存储了页面提交过来的，除了submit外的其他CGI参数名和参数值（只取第1个）。

              很巧妙的用法，是不是？它结合用了map和grep，使code显得很简洁。

              （话外一句：偶在Cornell读书时，偶的师兄们很喜欢这种用法，他们往往在中间多次使用map,grep,sort进行堆叠，结果产生的code也许高效，但不容易看懂。读这样的code时，你要从右往左读，因为右边表达式产生的临时列表，是左边表达式的输入条件。）

              5. 产生随机密码

              @a = (0 .. 9, 'a' .. 'z');
              $password = join '', map { $a[int rand @a] } 0 .. 7;
              print "$password\n";

              每次运行它会得到不同的结果，但长度总是8位，由0 .. 7这个决定。如下是可能的输出：

              y2ti3dal

              它是个随机值，也许你能用它来做密码。

              这里，需要先明白几个函数，rand产生一个随机值，它后面的@a其实是个标量哦，表示@a数组的长度，rand @a的结果可能是个小数，所以再用int函数来取整。int rand @a的结果是个整数，它>;=0但小于@a的长度。
              所以$a[int rand @a]就表示从@a数组里随机取出一个字符了。0..7表示总共取8次，返回的结果再用join连接起来，就构成一个8位随机密码了呀。

              当然，(0 .. 9, 'a' .. 'z')数组元素太少了，你可以修改它，使其包含大小写字符，数字和标点符号，这样密码强度就高些。

              6. 从数组元素里剥离数字

              已经说了哦，不要在EXPR里修改LIST值。如下做法是不好的：

              @digitless = map { tr/0-9//d; $_ } @array;

              它虽然从数组元素里剥离了数字，但同样破坏了该数组，:(

              如下做法是good:

              @digitless = map { ($x = $_) =~ tr/0-9//d;
                                 $x;
                                                  } @array;

                                                  它将tr的结果赋给临时变量$x，并返回$x的值，这样就保护数组了呀。

                                                  7. 打印"just another perl hacker"，让你晕到家

                                                  print map( { chr }
                                                             ('10611711511603209711011111610410111' . 
                                                                        '4032112101114108032104097099107101114')
                                                                        =~ /.../g
                                                                                 ), "\n";

                                                                                 打印的结果是：
                                                                                 just another perl hacker

                                                                                 chr函数将单个数字转换到相应的ASCII字符。()=~/.../g语法以3个数字长度为单位，分割数字串到新的串列表。

                                                                                 比较无聊的用法，还不如用pack()和unpack()，:P

                                                                                 8. 转置矩阵

                                                                                 @matrix = ( [1, 2, 3], [4, 5, 6], [7, 8, 9] );
                                                                                 foreach $xyz (@matrix) {
                                                                                         print "$xyz->;[0]  $xyz->;[1]  $xyz->;[2]\n";
                                                                                 }
                                                                                 @transposed =
                                                                                     map { $x = $_;
                                                                                               [ map { $matrix[$_][$x] } 0 .. $#matrix ];
                                                                                                       } 0 .. $#{$matrix[0]};
                                                                                                       print "\n";
                                                                                                       foreach $xyz (@transposed) {
                                                                                                               print "$xyz->[0];  $xyz->[1];  $xyz->[2];\n";

                                                                                                               打印结果是：

                                                                                                               1  2  3
                                                                                                               4  5  6
                                                                                                               7  8  9

                                                                                                               1  4  7
                                                                                                               2  5  8
                                                                                                               3  6  9

                                                                                                               这里稍微有点复杂哦，让我们分2步看看。

                                                                                                               @matrix = ( [1, 2, 3], [4, 5, 6], [7, 8, 9] );
                                                                                                               foreach $xyz (@matrix) {
                                                                                                                       print "$xyz->;[0]  $xyz->;[1]  $xyz->;[2]\n";
                                                                                                               }

                                                                                                               这里不难明白，( [1, 2, 3], [4, 5, 6], [7, 8, 9] ) 是个数组，它的每个元素又是个匿名数组，这样在$xyz遍历数组时，$xyz->;[0],$xyz->;[1],$xyz->;[2]就可以访问到匿名数组里的元素了。所以会打印出：

                                                                                                               1  2  3
                                                                                                               4  5  6
                                                                                                               7  8  9

                                                                                                               @transposed =
                                                                                                                   map { $x = $_;
                                                                                                                             [ map { $matrix[$_][$x] } 0 .. $#matrix ];
                                                                                                                                     } 0 .. $#{$matrix[0]};

                                                                                                                                     这里复杂点，0 .. $#{$matrix[0]}是个列表，$#{$matrix[0]}表示$matrix[0]这个匿名数组的最大下标值，0 .. $#{$matrix[0]}表示矩阵的横向。
                                                                                                                                     $x = $_;这里将$_的值赋给$x，为什么呢？因为它后面又有个map嘛，$_的值会改变，所以要先存储起来。
                                                                                                                                     外围的map返回的值是[]里的map计算出来的一个列表，以[]匿名数组形式返回。
                                                                                                                                     []里面的map是这样的，它的输入LIST是0 .. $#matrix， 表示矩阵的纵向了。$matrix[$_][$x]这里先纵再横，就把矩阵值置换了一下。所以返回的结果列表@transposed就包含置换后的矩阵了哦。

                                                                                                                                     是否有点糊涂？那举例看看。这样看可能好点：

                                                                                                                                     [1, 2, 3],
                                                                                                                                     [4, 5, 6],
                                                                                                                                     [7, 8, 9]

                                                                                                                                     外围的map遍历时，先是横向下标遍历，停留在横向0位。
                                                                                                                                     然后第二个map，就是纵向下标遍历了，它要遍历所有纵向下标，这样在横向0位，就先返回[1,4,7]的列表了，然后在横向1位，又返回[2,5,8]的列表，最后在横向2位，返回[3,6,9]的列表。

                                                                                                                                     还不明白呀？那偶也讲不清了，自己多想想，:P

                                                                                                                                     9. 查找质数：警示用法

                                                                                                                                     foreach $num (1 .. 1000) {
                                                                                                                                             @expr = map { '$_ % ' . $_ . ' &&' } 2 .. int sqrt $num;
                                                                                                                                                 if (eval "grep { @expr 1 } $num") { print "$num " }
                                                                                                                                     }

                                                                                                                                     打印结果是：
                                                                                                                                     1 2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 ...

                                                                                                                                     该code能工作，但它如此麻烦，违背了程序最基本的明晰法则。用如下直观的code代替它就可以了呀：

                                                                                                                                     CANDIDATE: foreach $num (1 .. 1000) {
                                                                                                                                             foreach $factor (2 .. int sqrt $num) {
                                                                                                                                                         unless ($num % $factor) { next CANDIDATE }
                                                                                                                                                             }
                                                                                                                                                                 print "$num ";
                                                                                                                                     }

                                                                                                                                     记住，让你的Code简洁哦~~

                                                                                                                                     ---



pipe
http://blog.csdn.net/fireroll/article/details/12262513
步骤是先使用pipe()函 数建立管道对，再使用fork()创建新进程，在不同的进程关闭不同的管道，这样就可以达到管道间通信的目的了
The pipe function creates two connected filehandles, a reader and writer, whereby anything writtern to the writer can be read from the reader.
http://perldoc.perl.org/perlipc.html#Bidirectional-Communication-with-Yourself


while each cause endless loop

    As a side effect, calling keys() resets the HASH's internal iterator (see "each"). 
    In particular, calling keys() in void context resets the iterator with no other overhead.

    After each has returned all entries from the hash or array, the next call to each returns the empty list in list context and undef in scalar context;
    the next call following that one restarts iteration. Each hash or array has its own internal iterator, accessed by each, keys, and values.
    The iterator is implicitly reset when each has reached the end as just described; it can be explicitly reset by calling keys or values on the hash or array.

    Getting the hash's content by evaluating it in list context uses the same iterator as each/keys/values, causing it to be reset.
#7#　Cause endless loop with:
    perl -e ' $h{a}=4; $h{b}=6; while ( my ($k, $v) = each(%h) ) { print "aaa",  %h;  }' 
    perl -e ' $h{a}=4; $h{b}=6; while ( my ($k, $v) = each(%h) ) { print "aaa"; keys %h;  }' 
