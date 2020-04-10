Table of Contents
=================
* [I. Tutorial](#i-tutorial)
   * [1.1 Perldoc](#11-perldoc)
      * [options](#options)
   * [1.2 <a href="https://metacpan.org/pod/distribution/perl/pod/perldata.pod" rel="nofollow">perldata</a>](#12-perldata)
   * [1.2.1 Context](#121-context)
      * [1.2.2 scalar values](#122-scalar-values)
      * [1.2.2 List value constructors](#122-list-value-constructors)
      * [1.2.4 slice](#124-slice)
         * [1.2.5 Key/Value Hash Slices](#125-keyvalue-hash-slices)
      * [Typeglobs and Filehandles](#typeglobs-and-filehandles)
   * [perlsyn](#perlsyn)
   * [perlop](#perlop)
   * [perlre](#perlre)
   * [perlvar](#perlvar)
   * [perlsub](#perlsub)
   * [perlfunc](#perlfunc)
   * [perlmod](#perlmod)
   * [perlref](#perlref)
   * [perlobj](#perlobj)
   * [perlipc](#perlipc)
   * [perlrun](#perlrun)
   * [perldebug](#perldebug)
   * [perldiag](#perldiag)
   * [perlfaq](#perlfaq)
      * [perlfaq1](#perlfaq1)
      * [<a href="https://metacpan.org/pod/distribution/perlfaq/lib/perlfaq5.pod" rel="nofollow">perlfaq5 - Files and Formats</a>](#perlfaq5---files-and-formats)
* [II. Modules:](#ii-modules)
   * [2.1 File::Copy](#21-filecopy)
   * [2.2 perl common modules simple usage sample](#22-perl-common-modules-simple-usage-sample)
* [III. Doc:](#iii-doc)
   * [3.1 Truth and Falsehood](#31-truth-and-falsehood)
   * [3.2 -&gt; 用法](#32---用法)
   * [3.3 <a href="http://stackoverflow.com/questions/7083453/copying-a-hashref-in-perl" rel="nofollow">copy hash</a>](#33-copy-hash)


# I. Tutorial #
## 1.1 Perldoc
### options
<blockquote>
-q perlfaq-search-regexp <br>
The -q option takes a regular expression as an argument.  It will search the question headings in perlfaq[1-9] and print the entries matching the regular expression.
</blockquote>

<blockquote>
-v perlvar
    The -v option followed by the name of a Perl predefined variable will extract the documentation of this variable from perlvar.
</blockquote>
```perl
    perldoc -v '$"'
    perldoc -v '$#'
```

<blockquote>
PageName|ModuleName|ProgramName|URL <br>
The item you want to look up.  Nested modules (such as "File::Basename") are specified either as "File::Basename" or "File/Basename".
</blockquote>

<blockquote>
-m module
    Display the entire module: both code and unformatted pod documentation.  This may be useful if the docs don't explain a function in the detail you need, and you'd like to inspect the code directly; perldoc will find the file for you and simply hand it off for display.
</blockquote>

## 1.2 [perldata](https://metacpan.org/pod/distribution/perl/pod/perldata.pod)

> Perl has three built-in data types: scalars, arrays of scalars, and associative arrays of scalars, known as "hashes".
 - A scalar is a single string (of any size, limited only by the available memory), number, or a reference to something (which will be discussed in perlref).
 - Normal arrays are ordered lists of scalars indexed by number, starting with 0.
 - Hashes are unordered collections of scalar values indexed by their associated string key.

> Values are usually referred to by name, or through a named reference. The first character of the name tells you to what sort of data structure it refers. The rest of the name tells you the particular value to which it refers.

scalar values are named with '$', even when referring to a scalar that is part of an array or a has. (like the English word "the") indicates a single value is expected.

```perl
$days
$days[28]
$days{'Feb'}
$#days            #the last index of array @days
```

Entire arrays are denoted by '@' (like the "these" or "those" does in English)
```perl
@days[3,4,5] # same as($days[3],$days[4],$days[5])
@days{'a','c'}   # same as ($days{'a'},$days{'c'})
```

Entire hashes are denoted by '%'

## 1.2.1 Context
The interpretation of operations and values in Perl sometimes depends on the requirements of the context around the operation or value. There are two major contexts: list and scalar.

### 1.2.2 scalar values
All data in Perl is a scalar, an array of scalars, or a hash of scalars.
A scalar may contain one single value in any of three different flavors: a number, a string, or a reference.
Although a scalar may not directly hold multiple values, it may contain a reference to an array or hash which in turn contains multiple values.

> A scalar value is interpreted as FALSE in the Boolean sense if it is undefined, the null string or the number 0 (or its string equivalent, "0"), and TRUE if it is anything else.

truncate an array to nothing:
```perl
@wahtever = ();
$#whatever = -1;
```

If you evaluate an array in scalar context, it returns the length of the array.
```perl
$element_count = scalar(@wahtever);
```

### 1.2.2 List value constructors
LISTs do automatic interpolation of sublists. That is, when a LIST is evaluated, each element of the list is evaluated in list context, and the resulting list value is interpolated into LIST just as if each individual element were a member of LIST.
```perl
(@foo, &SomeSub, %glarch)
```

A list value may also be subscripted like a normal array.
```perl
$time = (stat($file))[8];
```

An exception to this is that you may assign to undef in a list. This is useful for throwing away some of the return values of a function:
```perl
($dev, $ino, undef, undef, $uid, $gid) = stat($file);
```

The final element of a list assignment may be an array or a hash:
```perl
($a, $b, @rest) = split;
my ($a, $b, %rest) = @_;
```

It is often more readable to use the => operator between key/value pairs.
```perl
%map = (
    red => 0x00f,
    blue => 0x0f0,
    );
```

initializing hash referencese:
```perl
    $rec = {
        date => '10/31',
        cat => 'moew',
    };
```

### 1.2.4 slice
```perl
($who, $home)  = @ENV{"USER", "HOME"};      # hash slice
@them          = @folks[0 .. 3];            # array slice
```

#### 1.2.4.1 Key/Value Hash Slices
Starting from Perl 5.20 support
```perl
%h = (blonk => 2, foo => 3, squink => 5, bar => 8);
%subset = %h{'foo', 'bar'}; # key/value hash slice
## %subset is now (foo => 3, bar => 8)
```

### 1.2.5 Typeglobs and Filehandles
Perl uses an internal type called a typeglob to hold an entire symbol table entry. 
The type prefix of a typeglob is a `*` , because it represents all types.
```perl
local *Here::blue = \$There::green;
```
> temporarily makes `$Here::blue` an alias for `$There::green`, but doesn't make @Here::blue an alias for @There::green, or %Here::blue an alias for %There::green, etc.


## 1.3 [perlop](https://metacpan.org/pod/release/XSAWYERX/perl-5.30.0/pod/perlop.pod)

## 1.4 [perlre](https://metacpan.org/pod/release/XSAWYERX/perl-5.30.0/pod/perlre.pod)
```perl
regex for perl
    1. \E          end case modification (think vi)
    2. \Q          quote (disable) pattern metacharacters till \E
    ## For all their power and expressivity, patterns in Perl recognize the same 12 traditional metacharacters (the Dirty Dozen, as it were) found in many other regular expression packages:
    \ | ( ) [ { ^ $ * + ? .
```


## 1.5 perlvar

## 1.6 perlsub

## 1.7 perlfunc

## 1.8 perlmod

## 1.9 perlref

## 1.10 perlobj

## 1.11 perlipc

## 1.12 perlrun

## 1.13 perldebug

## 1.14 perldiag

## 1.15 perlfaq
### 1.15.1 perlfaq1

### 1.15.2 [perlfaq5 - Files and Formats](https://metacpan.org/pod/distribution/perlfaq/lib/perlfaq5.pod)


---
~~~
# II. Modules: #
## 2.1 File::Copy 
>'cp' and 'mv' would keep permission comparing to the 'copy' and 'move'
https://metacpan.org/source/SHAY/perl-5.22.1/lib/File/Copy.pm

## 2.2 perl common modules simple usage sample
http://bbs.chinaunix.net/thread-85748-5-1.html

## 2.3 [Exporter](https://perldoc.perl.org/Exporter.html)

## 2.4 FindBin
```perl 
use FindBin
$Bin           - path to bin directory from where script was invoked
$Script        - basename of script from which perl was invoked
$RealBin       - $Bin with all links resolved
$RealScript    - $Script with all links resolved
```

---
~~~
# III. Doc: #
## 3.1 Truth and Falsehood
> The number 0, the strings '0' and "", the empty list "()", and "undef"
are all false in a boolean context.  All other values are true.
Negation of a true value by "!" or "not" returns a special false value.
When evaluated as a string it is treated as "", but as a number, it is
treated as 0.  Most Perl operators that return true or false behave
this way.

## 3.2 -> 用法
-> 有两种用法，都和解引用有关。

- 1. List item
 第一种用法，就是解引用。
 根据 -> 后面跟的符号的不同，解不同类型的引用，
 ->[] 表示解数组引用，->{} 表示解散列引用 ，->() 表示解子例程引用。
 例子：
```perl
$arr_ref = \@array;
$arr_ref->[0] 访问数组 @array 的第一个元素。
$hash_ref = \%hash;
$hash_ref->{foo} 访问 %hash 的 foo 分量
$sub_ref = \&test;
$sub_ref->(1, 2, 3) 使用参数列表 (1,2,3) 来调用 &test 这个子程序。
```

- 2. 第二种用法，就是调用类或者对象的方法(_method_)。
格式：
> $obj->method();
或者
> ClassName->method();

例如：
```perl
$pop3->login( $username, $password );
my $ftp = Net::FTP->new("some.host.name", Debug => 0);
```
这两种用法略有不同，
但是总的来说，符合以下规则：
>假设 -> 的左操作数（就是左边那个值，如 $pop3 和 Net::FTP）是 $left，右操作数（就是右边那个值，如 login 和 new）是 $right，那么 -> 的运算规则就是：
```perl
 if ( ref $left 有效 ){    # 也就是说 $left 是个引用，而不是个裸字
         $ClassName = ref $left;   # 取引用的类型，当作类名称
 } else{
         $ClassName = $left;       # 直接把裸字当作类名称
 }
```
 然后调用：

```perl
 &{$ClassName::$right}($left, 原参数列表) 
```
 也就是说把类名称和右操作数拼在一起，当作子程序名称（注），并把左操作数当作第一个参数。

注：Perl 解释器要做的工作其实要比这复杂，它还要考虑到继承的问题。

## 3.3 [copy hash](http://stackoverflow.com/questions/7083453/copying-a-hashref-in-perl)
You can create a shallow copy of a hash easily:
```perl
my $copy = { %$source };
```
The %$source bit in list context will expand to the list of key value pairs. The curly braces (the anonymous hash constructor) then takes that list an creates a new hashref out of it. A shallow copy is fine if your structure is 1-dimensional, or if you do not need to clone any of the contained data structures.

To do a __full deep__ copy, you can use the core module Storable.
```perl
use Storable 'dclone';
my $deep_copy = dclone $source;
```

## 3.4 [How Hashes Really Work](https://www.perl.com/pub/2002/10/01/hashes.html/)
A hash is an unordered collection of values, each of which is identified by a unique key.

## 3.5 [STDIN, STDOUT, STDERR](https://rt.perl.org/Public/Bug/Display.html?id=23838)
The next open will _reuse_ the lowest file descriptor available, which will be the one of stdin (0).
The warning just warns you that you're using fd #0 for output, which is uncommon.
UNIX assigns to it the _lowest unused_ file descriptor.

## 3.5 管道
### 3.5.1 父进程写往子进程的管道
看看如下几句：

open(FOO, "|tr '[a-z]' '[A-Z]'");
open(FOO, '|-', "tr '[a-z]' '[A-Z]'");
open(FOO, '|-') || exec 'tr', '[a-z]', '[A-Z]';
它们是一样的吗？答案是：当然一样。
为什么？为什么？
让我们看看第一个：

open(FOO, "|tr '[a-z]' '[A-Z]'");
tr是什么？它是个unix的shell命令。它在管道右边，意味着什么？笨啊，当然意味着从管道左边接受输入啦。
如果你还不清楚，那么在shell里运行:
echo 'abcd' |tr '[a-z]' '[A-Z]'
ABCD

看到没有，你输入的abcd通过管道传给tr后，就处理成ABCD了。
那么，perl里也一样呀。open(FOO, "|tr '[a-z]' '[A-Z]'");它打开一个管道，并将数据通过句柄FOO传递给tr命令。
这里有点巧妙，实际上发生了1个fork过程。__tr命令实际上是在子进程里完成的啦。__
对了，有人问了，这个子进程与fork出来的有何不同？
主要的不同就在于子进程的STDIN被重定向到管道了，也就是说它从FOO句柄接受输入，然后它将结果输出到STDOUT，这样你在屏幕上就可见到ABCD啦。

明白了吗？很简单吧，:p 那接着看第2个：
open(FOO, '|-', "tr '[a-z]' '[A-Z]'");

这个与第1个其实一样的，只是写法不同啦！不过很多人被这个|-迷惑住了，以后再见到，就不要怕怕了哦，简单的把这个'-'想象成后面的shell命令就可以了呀。
好了，再看看第3个：

open(FOO, '|-') || exec 'tr', '[a-z]', '[A-Z]';
晕，这是什么意思啊？别着急，听偶慢慢道来。
已经说了哦，open过程中实际会发生一个fork过程，这个fork对父进程返回子进程的pid，通常是个正整数；对子进程返回0。所以：
my $pid=open(FOO,'|-');
若$pid > 0那就表示位于父进程里啦。||是什么意思呀？||是个or运算符，它后面的条件与前面的条件相反，前面的是$pid >;0，那后面的就是$pid==0啦，这样你就明白了吧，偶已经位于子进程里了。
那exec呢？exec与system意思差不多，__不同的是exec执行的命令完全替代了fork出来的子进程，__除了进程号一样外，其他的代码段，堆栈段什么的都替换掉了。
如果你不明白，那么翻翻仙子以前的关于exec的解释啦；什么？还不明白？那就把它想象成system()好啦。

所以这里你应该明白啦：
open(FOO, '|-') || exec 'tr', '[a-z]', '[A-Z]';
exec从管道接受数据，也就是说在子进程里，从FOO句柄接受数据，转换后再将结果写往标准输出，跟前面2个例子一样呀。

不过仙子提醒大家，上述3种情况下，你应该记住：
1）在父进程里，对FOO句柄操作的行为与正常的一致，例如，你这样将数据写入FOO句柄：
print FOO $str;
2）__在子进程里，STDIN被重定向了哦__。它默认从管道接受数据了。但STDOUT不变。不要混淆了哦，:-)


### 3.5.2 子进程写往父进程的管道


同样的，看看如下代码：
open(FOO, "cat -n '$file'|");
open(FOO, '-|', "cat -n '$file'");
open(FOO, '-|') || exec 'cat', '-n', $file;


这把大家都聪明了，它们肯定是一样的呀。
让我们先看看第1句，它简单点哦。

open(FOO, "cat -n '$file'|");
它的意思其实与前面的差不多哦，cat执行了外部shell命令，等于是fork了一个子进程，它将输出通过管道发送给父进程。如果你还不是很理解，那么看下这个shell命令:
cat -n $file | more

明白了吗？cat的结果通过管道发送给more了。
那么这里也一样呀，cat -n '$file'的结果写往了FOO句柄，父进程正常的读取这个句柄，就可以获取到cat的输出啦。父进程里这样写就可以啦：

print my $line=<FOO>;;

好，接着看第2句：
open(FOO, '-|', "cat -n '$file'");


又是'-|'，开始晕了吧？不要晕，它与第1句一样呀，写法不同罢了。记着：把'-'想象成后面的shell命令。


再看第3句哦：
open(FOO, '-|') || exec 'cat', '-n', $file;

这里与前面的一样哦，如果你理解了fork，理解了||，理解了exec，那么看它就清清楚楚啦。作用还是一样的哦，||后面的子进程将结果写往FOO句柄，父进程就从FOO句柄接受数据了。

仙子再次提醒大家，在上述3种情况下要注意：
1）父进程对FOO句柄的操作还是与正常的一致，例如，它这样接受FOO句柄的数据：
my $line=<FOO>;;

2）__子进程的STDOUT被重定向了__，也就是说，子进程的任何输出都会写往管道了。
好了，到这里你应该大概清楚open pipe的方式了吧？还不太明白？那么去看看perldoc的相关手册吧。
哦，还有个问题，能不能把子进程的STDIN和STDOUT同时定向到FOO句柄呀？晕，那就是双向管道了哦，仙子不太明白这方面的应用，看看IPC的相关文档吧。

---
~~~

