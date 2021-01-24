Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [I. <a href="https://www.gnu.org/software/bash/manual/bash.html" rel="nofollow">bash Manual</a>](#i-bash-manual)
      * [1.1 pipeline](#11-pipeline)
      * [1.2 Lists](#12-lists)
      * [1.3 Subshell](#13-subshell)
      * [1.4 Job Control Basics](#14-job-control-basics)
      * [1.5 Coding Skill](#15-Coding-Skill)
   * [II. pitfalls](#ii-pitfalls)
      * [2.1 passing args](#21-passing-args)
      * [2.2 function def (portable)](#22-function-def-portable)
      * [2.3 string compare to avoid pattern match without quote](#23-string-compare-to-avoid-pattern-match-without-quote)
   * [III. FAQ &amp; Context](#iii-faq--context)
      * [3.1 What startup files are read by the shell? (shell configuration)](#31-what-startup-files-are-read-by-the-shell-shell-configuration)


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

## 1.4 Job Control Basics

+ [1] 25647
indicating that this job is job number 1 and that the process ID of the last process in the pipeline associated with this job is 25647. All of the processes in a single pipeline are members of the same job. Bash uses the job abstraction as the basis for job control.#---

## 1.5 Coding Skill
### 1.5.1 after shebang, insert below line
```bash
set -xeuo pipefail
## or run bash commands in terminal with the settings
( set -xeuo pipefail; for i in $(ls -d test_dir{2..2}); do echo "tar cfz $i.tar.gz $i && rm -rf $i"; done)
```

### 1.5.2 flock to avoid same script to run several times
```bash
flock --wait 5 -e "lock_myscript" -c "bash myscript.sh"
```

### 1.5.3 kill all child process if there is when the script is accidently exit 
```bash
# put below line at the beginning block
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT
```

### 1.5.4 timeout the command excuting time
```bash
timeout 600s <script|command> arg1 arg2
```

### 1.5.5 loop with number range
```bash
for i in $(seq -w 01 07); do echo -e  "\n vm-kcr$i ";  ssh  "vm-kcr$i"  "df -h /SCRATCH/ ; df -h /tmp/"; done;
for i in {1..10}; do echo $i; done;
```

### 1.5.6 get case TAT over 360 secs from txt files of dirs
```bash
for d in $(ls -1d D202011*); do awk -F',' '/   \(/{tct=gensub(")","",1,$NF) + 0; if (tct >= 450){ print FILENAME, $1, tct}}' ${d}/Passed.txt ;  awk -F',' '/   \(/{tct=$2 + 0; if (tct >= 450){ print FILENAME, $1, tct}}' ${d}/Failed.txt; done
```

---
# II. pitfalls
[bash pitfalls](http://mywiki.wooledge.org/BashPitfalls)
### 2.1 passing args
```bash
for x in "$@"; do
    ## "$@" equal to "$1" "$2" "$3" ...
    echo "parameter: '$x'"
done
```

### 2.2 function def (portable)
```bash
foo() {
    ...
}
```

### 2.3 string compare to avoid pattern match without quote
```bash
if [[ $foo == "$bar" ]]; then
fi
```


# III. FAQ & Context
[BASH Frequently Asked Questions](http://mywiki.wooledge.org/BashFAQ)

## 3.1 What startup files are read by the shell? (shell configuration)
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
