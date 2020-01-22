
---
# I. [bash Manual](https://www.gnu.org/software/bash/manual/bash.html)
## 1.1 pipeline
+ A pipeline is a sequence of one or more commands separated by the character |.  The format for a pipeline is:
```bash
[time [-p]] [ ! ] command [ | command2 ... ]
```
	The standard output of command is connected via a pipe to the standard input of command2.  This connection is performed **before** any redirections specified by the command (see REDIRECTION below). 
	_The return status_ of a pipeline is the exit status of the last command, unless the pipefail option is enabled.  
	If pipefail is enabled, the pipeline's return status is the value of the last (rightmost) command to exit with a non-zero status, or zero if all commands exit successfully.  

	If the reserved word! precedes a pipeline, the exit status of that pipeline is the logical negation of the exit status as described above. The shell waits for all commands in the pipeline to terminate before returning a value.
	If the _time_ reserved word precedes a pipeline, the elapsed as well as user and system time consumed by its execution are reported when the  pipeline  terminates.   
	The  -p  option changes the output format to that specified by POSIX.  
	The TIMEFORMAT variable may be set to a format string that specifies how the timing information should be displayed; see the description of TIMEFORMAT under Shell Variables below. Each command in a pipeline is executed as __a separate process__ (i.e., in a subshell).

## 1.2 Lists
+ A list is a sequence of one or more pipelines separated by one of the operators `;, &, &&, or ||`, and optionally terminated by one of `;, &, or <newline>`.
	If a command is terminated by the control operator `&`, the shell executes the command in the background in a subshell.  The shell __does not wait__ for the command to finish,  and the return status is `0`.  
	Commands separated by a `;` are executed sequentially; the shell __waits__ for each command to terminate in turn. The return status is the exit status of the last command executed.

+ (list) 
	list is executed in a subshell environment (see COMMAND EXECUTION ENVIRONMENT below).  
	Variable assignments and builtin commands that affect the shell's environment __do not__ remain in effect after the command completes.  The return status is the exit status of list.


+ { list; } 
	list is simply executed in the _current_ shell environment.  list __must__ be terminated with a newline or semicolon.  This is known as a group command.
	The return status is the exit status of list.  Note that unlike the metacharacters ( and ), { and } are reserved words and must occur where a reserved word is permitted to be recognized. Since they do not cause a word break, they must be separated from list by whitespace.

+ ((expression))
	The expression is evaluated according to the rules described below under _ARITHMETIC EVALUATION_.  
	If the value of  the  expression  is  non-zero,  the return status is 0; otherwise the return status is 1.  This is exactly equivalent to let "expression".

+ [[ expression ]]
	Return  a status of 0 or 1 depending on the evaluation of the conditional expression expression.  Expressions are composed of the primaries described below under _CONDITIONAL EXPRESSIONS_.  
	Word splitting and pathname expansion are not performed on the words between the [[ and  ]];  tilde  expansion, parameter  and  variable  expansion,  arithmetic expansion, command substitution, process substitution, and quote removal are performed.  Conditional operators such as -f must be unquoted to be recognized as primaries.


## 1.3 Subshell
+ If a command is terminated by the control operator ‘&’, the shell executes the command asynchronously in a subshell. This is known as executing the command in the background. The shell does not wait for the command to finish, and the return status is 0 (true). When job control is not active (see Job Control), the standard input for asynchronous commands, in the absence of any explicit redirections, is redirected from /dev/null.

()
( list )
Placing a list of commands between parentheses causes a subshell environment to be created (see Command Execution Environment), and each of the commands in list to be executed in that subshell. Since the list is executed in a subshell, variable assignments do not remain in effect after the subshell completes.

{}
{ list; }
Placing a list of commands between curly braces causes the list to be executed in the current shell context. No subshell is created. The semicolon (or newline) following list is required.

The shell has an execution environment, which consists of the following:
    •    open files inherited by the shell at invocation, as modified by redirections supplied to the exec builtin
    •    the current working directory as set by cd, pushd, or popd, or inherited by the shell at invocation
    •    the file creation mode mask as set by umask or inherited from the shell’s parent
    •    current traps set by trap
    •    shell parameters that are set by variable assignment or with set or inherited from the shell’s parent in the environment
    •    shell functions defined during execution or inherited from the shell’s parent in the environment
    •    options enabled at invocation (either by default or with command-line arguments) or by set
    •    options enabled by shopt (see The Shopt Builtin)
    •    shell aliases defined with alias (see Aliases)
    •    various process IDs, including those of background jobs (see Lists), the value of $$, and the value of $PPID

When a simple command other than a builtin or shell function is to be executed, it is invoked in a separate execution environment that consists of the following. Unless otherwise noted, the values are inherited from the shell.
    •    `the shell’s open files, plus any modifications and additions specified by redirections to the command`
    •    the current working directory
    •    the file creation mode mask
    •    shell variables and functions marked for export, along with variables exported for the command, passed in the environment (see Environment)
    •    traps caught by the shell are reset to the values inherited from the shell’s parent, and traps ignored by the shell are ignored

A command invoked in this separate environment `cannot affect` the shell’s execution environment.

Command substitution, commands grouped with parentheses, and asynchronous commands are invoked in a subshell environment that is a `duplicate` of the shell environment, except that traps caught by the shell are reset to the values that the shell inherited from its parent at invocation. Builtin commands that are invoked as part of a pipeline are also executed in a subshell environment. Changes made to the subshell environment cannot affect the shell’s execution environment.

Subshells spawned to execute command substitutions inherit the value of the -e option from the parent shell. When not in POSIX mode, Bash clears the -e option in such subshells.

If a command is followed by a ‘&’ and job control is not active, the default standard input for the command is the empty file /dev/null. Otherwise, the invoked command `inherits` the file descriptors of the calling shell as modified by redirections.

## 1.3 Job Control Basics

+ [1] 25647
indicating that this job is job number 1 and that the process ID of the last process in the pipeline associated with this job is 25647. All of the processes in a single pipeline are members of the same job. Bash uses the job abstraction as the basis for job control.#---




---
# II. pitfalls
+ [pitfalls1](http://kodango.com/bash-pitfalls-part-1) 
+ [pitfalls2](http://kodango.com/bash-pitfalls-part-2)
+ [pitfalls3](http://kodango.com/bash-pitfalls-part-3) 
+ [pitfalls4](http://kodango.com/bash-pitfalls-part-4)

### TODO FIXME
## "*.mp3"  vs *.mp3
> for i in $(ls *.mp3)
    ▪ 使用命令展开时不带引号，其执行结果会使用IFS作为分隔符，拆分成参数传递给for循环处理；
    ▪ 不应该让脚本去解析ls命令的结果；

---
### copy if filename contain '-'
文件名中包含短横'-', 第一种方法是在命令和参数之间加上--，这种语法告诉命令不要继续对--之后的内容进行命令行参数/选项解析：
```bash
$cp -- "$file" "$target"
```
另外一种方法是，确保文件名都使用相对或者绝对的路径，以目录开头：
```bash
for i in ./*.mp3; 
    do
    cp "$i" /target
    
    ...
Done
```

---
### comparison in the condition
```bash
 [ $foo = "bar" ]
```
这个例子在以下情况下会出错：
    ▪ 如果[中的变量不存在，或者为空，这个时候上面的例子最终解析结果是：
    [ = "bar" ] # 错误!
    并且执行会出错：unary operator expected，因为=是二元操作符，它需要左右各一个操作数。
    ▪ 如果变量值包含空格，它首先在执行之前进行单词拆分，因此[命令看到的样子可能是这样的：
    [ multiple words here = "bar" ];

POSIX way:
```bash
[ "$foo" = bar ]
```

```bash
[ "$foo" = bar && "$bar" = foo ]
```
    不要在test命令内部使用&&，Bash解析器会把你的命令分隔成两个命令，在&&之前和之后。你应该使用下面的写法：
```bash
    [ bar = "$foo" ] && [ foo = "$bar" ] # POSIX
    [[ $foo = bar && $bar = foo ]]       # Bash / Ksh
```

---
```bash
grep foo bar | while read -r; do ((count++)); done
```
这种写法初看没有问题，但是你会发现当执行完后，count变量并没有变化。原因是管道后面的命令是在一个子Shell中执行的。

---
### do not read and write file at the same pipe
```bash
cat file | sed s/foo/bar/ > file
```
你不应该在一个管道中，从一个文件读的同时，再往相同的文件里面写，这样的后果是未知的。你可以为此创建一个临时文件，这种做法比较安全可靠：
```bash
sed 's/foo/bar/g' file > tmpfile && mv tmpfile file
```

---
### check *cd* if it's successful
```bash
cd /foo; bar
```
如果你不检查 cd 命令执行是否成功，你可以会在错误的目录下执行 bar 命令，这有可能会带来灾难，比如 bar 命令是 rm -rf *。
如果你想要在标准输出同时输出自定义的错误提示，可以使用复合命令（command grouping）:
```bash
    cd /net || { echo "Can't read /net. Make sure you've logged in to the Samba network, and try again."; exit 1; }

    do_stuff

    more_stuff
```

下面的写法，在循环中 `fork 了一个子 shell 进程`，子 shell 进程中的 cd 命令仅会影响当前 shell的环境变量，所以父进程中的环境命令不会被改变；当执行到下一次循环时，无论之前的 cd命令有没有执行成功，我们会回到相同的当前目录。这种写法相较前面的用法，代码更加干净。
```bash
    ## http://mywiki.wooledge.org/BashGuide/CompoundCommands
    
    find ... -type d -print0 | while IFS= read -r -d '' subdir; 
    do
   
        (cd "$subdir" || exit; whatever; ...)

    done
```

---
### double quota for parameter
```bash
for arg in $*
    ## 正确的写法：
for x in "$@"; 
do
    echo "parameter: '$x'"
Done
```

---
### function defination format
```bash
function foo()
## 这种写法不一定能够兼容所有 shell，兼容的写法是：
foo() 
{
    ...

}
```
    
---
### printf format
```bash
printf "$foo"
### 如果$foo 变量的值中包括\或者%符号，上面命令的执行结果可能会出乎你的意料之外。
下面是正确的写法：
printf %s "$foo"

printf '%s\n' "$foo"
```

---
## 2. semantic
### for loop style
``` bash
for arg in [list] 
do 
 command(s)… 
done 
  
for file in "$( find $directory -type l )"
do 
  echo "$file" 
done | sort                  # Otherwise file list is unsorted. 
  
c-style syntax 
  
# oneline 
for ((i=1; i <=6885; i++)); do n=$(printf '%04d' $i); f="swe-vm-kcr-cats024190m2_$n"; [[ -e $f ]] || echo "$f no there"; done
```


# II. FAQ & Context
## 2.1 What startup files are read by the shell? (shell configuration)
[Unix Faq](http://hayne.net/MacDev/Notes/unixFAQ.html#shellStartup)

You can customize the behaviour of the shells you use by editing the "startup files" that are read when a shell starts up. 
These files are often called "dot files" since their names usually start with a dot (.)Note that the per-user "dot files" are looked for in your home folder (designated by ~) and that they don't usually exist by default 
The following settings are often put in shell startup files:
+ shell execution PATH (determines where the shell will look for executables)
+ MANPATH (determines where the 'man' program will look for man pages)
+ shell aliases and functions (used to save you typing)
+ shell prompts- other environment variables

Which startup files are read __depends on__ which shell you are using (e.g. bash or tcsh) and whether it is a "login shell" or a "non-login shell". 
Note however, that sub-shells inherit the environment variables of the parent shell. The following is a summary of the usual startup files read by "interactive" shells. 
Bash Startup Files
+ When a "login shell" starts up, it reads the file 
_"/etc/profile"_ ==> *"~/.bash_profile"* or *"~/.bash_login"* or _"~/.profile"_ (whichever one exists - it only reads one of these, checking for them in the order mentioned).

+ When a "non-login shell" starts up, it reads the file
_"/etc/bashrc"_ ==>  _"~/.bashrc"_.

Note that when bash is invoked with the name "sh", it tries to mimic the startup sequence of the Bourne shell ("sh"). In particular, a non-login shell invoked as "sh" does not read any dot files by default. See the bash man page for details.

Tcsh Startup Files
When a "login shell" starts up, it reads the files _"/etc/csh.cshrc"_ and _"/etc/csh.login"_ (in that order) and then _"~/.tcshrc"_ or _"~/.cshrc"_ (whichever one exists - it only reads one of these, checking for them in the order mentioned) and then ~/.login.

When a "non-login shell" starts up, it reads the file _"/etc/csh.cshrc"_ and then _"~/.tcshrc"_ or _"~/.cshrc"_ (whichever one exists - it only reads one of these).
