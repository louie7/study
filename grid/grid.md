Table of Contents (UGE/SGE)
=================

   * [Table of Contents (UGE/SGE)](#table-of-contents-ugesge)
      * [I. Complex setting](#i-complex-setting)
         * [1. qconf](#1-qconf)
         * [2. qquota setting:](#2-qquota-setting)
         * [3. -sprjl: ](#3--sprjl-)
      * [II. Job priorities](#ii-job-priorities)
      * [III. Commands](#iii-commands)
         * [1. qaccess](#1-qaccess)
         * [2. qacct](#2-qacct)
         * [3. qsub](#3-qsub)
         * [4. qstat](#4-qstat)
         * [5. qhost](#5-qhost)
         * [6. qalter](#6-qalter)
         * [7. qdel - delete batch jobs](#7-qdel---delete-batch-jobs)
         * [8. quser](#8-quser)
         * [9. Job suspension:](#9-job-suspension)
      * [IV. FAQ](#iv-faq)
         * [1. General errors](#1-general-errors)
      * [Quota reached](#quota-reached)
         * [2. Running Jobs](#2-running-jobs)
            * [1. "Error: No suitable queues"](#1-error-no-suitable-queues)
            * [2. No output or truncated output](#2-no-output-or-truncated-output)
            * [3. Eqw: Job waiting in error state](#3-eqw-job-waiting-in-error-state)
            * [4. My job is stuck in the 'dr' state](#4-my-job-is-stuck-in-the-dr-state)
            * [5. Job won't start](#5-job-wont-start)
            * [6. Rr: Job re-started](#6-rr-job-re-started)
            * [7. Why doesn't my job start right away?](#7-why-doesnt-my-job-start-right-away)
            * [8. How to merge output files](#8-how-to-merge-output-files)
            * [9. Warning: No xauth data; using fake authentication data for X11 forwarding](#9-warning-no-xauth-data-using-fake-authentication-data-for-x11-forwarding)
            * [10. I need to extend the run-time limit for a running job](#10-i-need-to-extend-the-run-time-limit-for-a-running-job)
      * [V. Others](#v-others)
         * [1. man sge_conf](#1-man-sge_conf)
         * [2. man sge_flags](#2-man-sge_flags)


---
## I. Complex setting
man complex
NAME
       complex - Univa Grid Engine complexes configuration file format


UGE would product ENV for some command like qsub
Job parameters and Environment variables: [Grid Engine Context](https://www.ace-net.ca/wiki/Grid_Engine)

### 1. qconf
```bash
## see complex configuration setting
qconf -sc

## shows the list of all currently defined users.
qconf -suserl <show users>

## list all submit hosts
qconf -ss

## list all execution hosts
qconf -sel

## see host complex setting, qsub and qhost about h=XXX setting
qconf -sconf <host>

## displays the definition of the specified execution host.
## to check the host status, and get the detail resource setting of the specified cell
qconf -se <host>

qconf -s

## Get the detail notify time to post action like tar back after the job is killed
qconf -sq q1 | grep notify
   notify                00:05:00

```

### 2. qquota setting:
<root>/spool/qmaster/resource_quotas/

### 3. -sprjl: <show project list>
Shows the list of all currently defined projects.  show specific Project priority:
``` bash
(s_linux_sge; qconf -sprj prj_nightly_reg  )
name prj_nightly_reg
oticket 0
fshare `27`  ## the bigger the high priority
acl NONE
xacl ig-share
```

---
## II. Job priorities
[sge priority](http://gridscheduler.sourceforge.net/htmlman/htmlman5/sge_priority.html)

SGE provide means for controlling job dispatch and run-time priorities.

- dispatch priority: indicates the importance of pending jobs compated with others
- run-time priority: determines CPU allocation

A job's dispatch priority is affected by factors:
     o  the identity of the submitting user

     o  the project under which the job is submitted (or alternatively, the default project of the submitting user)

     o  any resources requested by the job

     o  the job's submit time

     o  the job's initiation deadline time (if specified)

     o  the -p priority specified for the job (also known as  the
        POSIX priority "pprio")


Each of these is configured through the sched_conf(5) parameters weight_priority, weight_ticket and weight_urgency.
Normalization maps each raw urgency/ticket/priority value into a range between 0 and 1.

        npprior = normalized(ppri)
        nurg    = normalized(urg)
        ntckts  = normalized(tckts)

        prio    = weight_priority * pprio +
                  weight_urgency  * nurg  +
                  weight_ticket   * ntckts

The higher a job's priority value, the earlier it gets dispatched.

The *urgency* policy defines an urgency value  for  each  job. The urgency value:

        urg     =  rrcontr + wtcontr + dlcontr

consists of the resource requirement contribution ("rrcontr"),  the waiting time contribution ("wtcontr") and the deadline contribution ("dlcontr").

The ticket policy unites functional, override and share tree policies in the ticket value ("tckts"), as is defined as the sum of the specific ticket values  ("ftckt"/"otckt"/"stckt") for each sub-policy (functional, override, share):

         tckts = ftckt + otckt + stckt


---
## III. Commands

### 1. qaccess
qaccess - Show overall access status for Grid Engine queues
    Usage: qaccess [-help] [-h] Hostname [-u] Username [-ul] Userlist [-P] all|Project
        -h              Print access status on the specified machine
        -u              Print SGE queues that the user has access to
        -ul             Print SGE queues that the userlist has access to
        -P              Print SGE queues that belong to the project

```bash
qaccess -P <project>
```

### 2. qacct
check finished job status with accounting file
```bash
qacct --help
[[-f] acctfile]                   use alternate accounting file
[-j [job_id|job_name|pattern]]    list all [matching] jobs

qacct -f <account_file_path>/accounting.1 -j [jobid|jobname]
```

### 3. qsub
qsub   -  submit a batch job to Univa Grid Engine.
* - The -P (`priority`) option allows users to designate the relative priority of a batch job for selection from a queue.
* -A  account_string
    Define the account to which the resource consumption of the batch job should be charged.
* -b y[es]|n[o]
    Gives the user the possibility to indicate explicitly whether command should be treated as binary or script. If the value of -b is 'y', then command  may be a binary or script.
* -e  path_name
    Define the path to be used for the standard error stream of the batch job.
* -j y|n
    Specifies whether or not the standard error stream of the job is merged into the standard output stream. If both the -j y and the -e options are present, Univa Grid Engine sets but ignores the error-path attribute.
* -shell y[es]|n[o]
    -shell n causes qsub to execute the command line directly, as if by exec(2).  No command shell will be executed for the job.  This option only applies when -b y is also used.  Without -b y, -shell n has no effect.
    This option can be used to speed up execution as some overhead, like the shell startup and sourcing the shell resource files is avoided.
* -v  variable_list
    Add to the list of variables that are *exported* to the session leader of the batch job.
* -V  Specify that all of the environment variables of the process are exported to the context of the batch job.
* -N option allows users to associate a name with the batch job.
The -o option allows users to redirect the standard output stream.

Multithreaded job submission use `-pe mt <n>` option
Distributed job submission use `-pe dp <n>` option

```bash
Batch Jobs (examples)
#  Submit to bnormal project, and choose a Linux machine
qsub -P bnormal -l arch=glinux $PATH/script.sh

# Submit to bnormal project and stay in the current working directory, and choose a AMD 64 type CPU
qsub -P bnormal -cwd -l cputype=amd64 script.sh

# Submit to bhigh project, and choose a Solaris 64 bit machine which has at least 10GB of virtual memory free
qsub -P bhigh -l arch=solari64,mem_free=10g script.sh

#  Submit to bhigh and choose a Linux machine which has the BibMem kernel installed (capable of accessing upto 3.6GB memory)
qsub -P bhigh -l model=PC2800 script.sh

#  specify the job option in the job script with "\#\$" like:
\#\$ -cwd
\#\$ -N jobName
```


### 4. qstat
qstat - show the status of Univa Grid Engine jobs and queues

    -s {p|r|s|z|hu|ho|hs|hd|hj|ha|h|a}[+]
      Prints only jobs in the specified state, any combination of states is possible.

```bash
# Job Status: (Examples)
qstat -u <user_id>
qstat -j <job_id>

# list all running jobs for the given user-name
qstat -ext -u <user_id> -s r

# list all pending jobs for the given user-name
qstat -ext -u <user_id> -s p

# Get runing job status for specific resource
(source <source_path>/settings.sh; qstat -u '*'  -F  os_version=WS7.0,os_minor=6.6\|6.7,os_bit=64 -s r ) | awk -v RS='----------------*' '{if ($0 ~ /qsc=m/ ){print $0} }'
```

### 5. qhost
 qhost - show the status of Univa Grid Engine hosts, queues, jobs

* -j   Prints all jobs `running` on the  queues  hosted  by  the shown hosts. This switch calls _-q_ implicitly. _-q_ Show information about the queues  instances hosted by the displayed hosts.
* -h display only selected hosts
* -l [resource request]
      Defines the resources to be granted by the hosts which should be included in the host list output.
* **-F** [ resource_name,... ]
    qhost will present a detailed listing of the current **resource availability** per host *with respect to* all resources (if the option argument is omitted) or with respect to those resources contained in the resource_name list. Please refer to the description of the Full Format in section OUTPUT FORMATS below  for  further detail.

```bash
# list running jobs on the queues hosts
   qhost -j
   job-ID     prior   name       user         state submit/start at     queue      master ja-task-ID
   -------------------------------------------------------------------------------------------------
   ...
   ...

# get list of the resource 'project' availablility defination from *'qconf -sc'*:
(s_linux_sge; qhost -F project | fgrep 'project='  | sort -u  )

# get available os flag resouce  setting
(s_linux_sge ; qhost  -F os | fgrep ':os=' | sort -u  )

# list the availible host with  specific resource
(s_linux_sge ; qhost -F scratch_free -l os=CS6.6,mem_free=51200M,scratch_free=500G,health=1,m_core=16  )
```

### 6. qalter
qalter -  modify a pending or running batch job of Univa Grid Engine.
>      qalter [-a date_time][-A account_string][-c interval][-e path_name]
>                [-h hold_list][-j join_list][-k keep_list][-l resource_list]
>                [-m mail_options][-M mail_list][-N name][-o path_name]
>                [-p priority][-r y|n][-S path_name_list][-u user_list]
>                job_identifier ...

Job Alert job:
qalter: use the same option and argument as the "qsub" to alter the queued job
The qalter utility allows users to change the attributes of a batch job. The qalter utility allows users to change the attributes of a batch job.

```bash
# adjust the job priority:
qalter -P <priority> <job_id_list>

# To test/verify a job requset is available:
qalter -w p 9068517

# adjust the mt setting to make the job submitted rather than 'qw'
qalter -pt mt 1
```

    The '-w' option:
        -w e|w|n|p|v
            Available for qsub, qsh, qrsh, qlogin and qalter. Specifies `a validation level applied to the job` to be submitted (qsub, qlogin, and qsh) or the specified queued job (qalter).  The information displayed indicates whether the job can possibly be scheduled assuming an empty system with no other jobs. Resource requests exceeding the configured maximal thresholds or requesting unavailable resource attributes are possible causes for jobs to fail this validation.
    
    The specifiers e, w, n and v define the following validation modes:
           'e'  error - jobs with invalid requests will be
                rejected.
           'w'  warning - only a warning will be displayed
                for invalid requests.
           'n'  none - switches off validation; the default for
                qsub, qalter, qrsh, qsh
                and qlogin.
           'p'  poke - does not submit the job but prints a
                validation report based on a cluster as is with
                all resource utilizations in place.
           'v'  verify - does not submit the job but prints a validation report based on an empty cluster. Note, that the necessary checks are performance consuming and hence the checking is switched  off  by  default. It  should  also  be  noted  that  load  values are not taken into account with the verification since they are assumed to be too volatile. To cause -w e verification to be passed at submission time, it is possible to specify non-volatile values (non-consumables) or maximum values (consumables) in complex_values.


### 7. qdel - delete batch jobs
>    qdel [ -f ] [ -help ] [ -u wc_user_list ] [ wc_job_range_list ] [ -t task_id_range ]

```bash
qdel -u <user_id>
qdel <job_id>
```

### 8. quser
quser - Show access/resource status for Grid Engine users

    quser [-help] [-l ResourceFlag ] [-u Username] [-ext]
             -help Print this usage message;
             -u    Username;
             -l    ResourceFlag;
             -sf <num> -  slots free
             -pe mt <num> - parallel environment mt usage
             -ext  Show rush queues & extended output-
                   (OS KERNEL CPU MODEL QSC)


### 9. Job suspension:
```bash
    qhold <job_id>
    qrls <job_id>
```

---
## IV. FAQ
[FAQ](https://www.ace-net.ca/wiki/FAQ)

### 1. General errors
## Quota reached
In some cases, the storage system may mistakenly report that you have reached your storage quota. 
Please refer to the following page for details.

### 2. Running Jobs
#### 1. "Error: No suitable queues"
You will get the message "Unable to run job: error: no suitable queues" when you submit the job if Grid Engine finds it could never run. You may have failed to provide a run time (h_rt), requested more memory than can be provided (h_vmem), or mistyped the name of a queue or parallel environment. If you want some hints from Grid Engine about why it can't be scheduled, re-submit it with "-w v":
```bash
qsub -w v ...other options...
```
If you know the job can't be scheduled and want it to go in anyway, you can use "-w w" or "-w n" options to override the default "-w e".

#### 2. No output or truncated output
If your job output is mysteriously truncated or you get no output at all, or you receive the "Killed" message, it might be because:
    - the program exceeded a run-time limit (h_rt). Look at the output you got and try to determine why the program is taking longer than you expected. If you think you know why, resubmit with a larger value for h_rt.
    - the program ran out of memory (h_vmem). See Memory Management for a detailed discussion.
    - the program crashed due to an internal error — check your code for bugs
the disk quota for the storage the program is writing to was reached — See disk quotas for a list of quotas and commands to check disk usage.

If your job has been terminated unexpectedly (for example it has exit_status 137 in the 'qacct' records) and it did not violate the run-time limit (h_rt) then it may have violated a memory limit (h_vmem). Try increasing h_vmem or decreasing the size of some large arrays in your program, and resubmit. Use the qacct command to get Grid Engine accounting data about your job: how much memory it consumed, how long it ran, etc.

#### 3. Eqw: Job waiting in error state
If qstat or showq has "Eqw" in the STATE column for one of your jobs you can use
```bash
qstat -j jobid | grep error
```

to check the reason. If you understand the reason and can get it fixed, you can clear the error state with
```bash
qmod -cj jobid
```

Some common error messages are these:
>can't chdir to directory: No such file or directory
 can't stat() "file" as stdout_path

These indicate that some directory or file (respectively) cannot be found. Verify that the file or directory in question exists, i.e., you haven't forgotten to create it and you can see it from the head node. If it appears to be okay, then the job may have suffered a transient condition such as a failed NFS automount, or an NFS server was temporarily down. Clear the error state as shown above.

#### 4. My job is stuck in the 'dr' state
Sometimes users find their jobs being stuck indefinitely in the dr state. 
The d state indicates that a qdel has been used to initiate job deletion.
The reason a job gets stuck in this state is because Grid Engine loses communication with one of the compute nodes, and thus cannot cleanly remove the job from a queue - hence the dual state: (r)unning and being (d)eleted. 
Usually, this is due to a failed compute node, which was probably the reason why you tried to remove the job in the first place - because it was not making any progress. 
Please let us know about such jobs in the dr state so that we can remove faulty nodes out of production as soon as possible. You can also try to force delete your job like so: *qdel -f job_id*


#### 5. Job won't start
There are a lot of possible reasons why your job does not start right away.
There may not be enough CPU slots free.
There may not be enough slots in the time-limit queue (medium.q, long.q) your job qualifies for.
There might be enough slots but not enough memory because some of the running jobs have reserved a lot of memory.
A higher priority job may be reserving slots for a large parallel run.
An outage may be scheduled to begin before your job would end. (See Cluster Status for planned outages.)
Serial jobs are not scheduled on most 16-core shared memory hosts.
An individual research group cannot occupy more than 80% of the slots on a given cluster.
Some other requestable resource (e.g. Myrinet endpoints, Fluent licenses) may not be available.
You can query the Grid Engine for hints about why your job hasn't yet run this way:
```bash
qalter -w v job_id 
```

#### 6. Rr: Job re-started
A capital R in the job status in qstat or showq signifies "rescheduled" or "rescheduling". If a host goes down while running a job, Grid Engine will put the job back in the waiting list to be run again. "Rr" means it has restarted and is running again; "Rq" means it is waiting to be restarted. We strongly recommend you verify that a restarted job is progressing as you would expect by checking the output file. Not all applications recover gracefully on a restart like this.
If you want your jobs not to be rescheduled when a host fails in the middle, set the "rerun" option to "no" in your job script like this:
```bash
#$ -r no
```

If you like the restart feature but your application doesn't handle it automatically and gracefully, you can also write your script to detect when it has been restarted by checking if the environment variable $RESTARTED == 1.

#### 7. Why doesn't my job start right away?
This could be for a variety of reasons. When you submit a job to the N1 Grid Engine you are making a request for resources.
There may be times when the cluster is busy and you will be required to wait for resources. 
If you use the qstat command, you may see qw next to your job. This indicates that it is in the queue and waiting to be scheduled. If you see an r next to your job then your job is running.
That said, it is often not clear what resources are missing that are preventing your job from being scheduled. 
Most often it is memory that is in short supply, h_vmem. 
You may be able to increase your job's likelihood of being scheduled if it requires only few resources by reducing the job's memory requirements. For example:
```bash
qalter -l h_vmem=500M,h_rt=hh:mm:ss job_id
```

will reduce the virtual memory reserved for the job to 500 megabytes. 
You must re-supply the h_rt and any other arguments to -l when you use qalter. The default values are listed here.
Note that for parallel jobs, this h_vmem request is per process.
The scheduler will only start your job if it can find a host (or hosts) with enough memory unassigned to other jobs. 
You can determine the vmem available on various hosts with:
```bash
qhost -F h_vmem
```

or you can see how many hosts have at least, say, 8 gigabytes free with
```bash
qhost -l h_vmem=8G
```

You can also try defining a short time limit for the job:
```bash
qalter -l h_rt=0:1:0,other args job_id
```

imposes a hard run-time limit of 0 hours, 1 minute, 0 seconds (0:1:0). 
In certain circumstances the scheduler will be able to schedule a job that it knows will finish quickly, where it cannot schedule a longer job.
qalter gotcha at Placentia: Following the simple example above can land your job in the subordinate queue where it is subject to being suspended. 
Now, if you want your job to start sooner this might be A Good Thing, but if you'd rather wait for a regular queue slot then here's how you avoid that:
An additional -l resource request, suspendable=true, is added to your job quietly by default. qalter replaces the entire list of -l arguments, so if you just want to change h_rt you should first extract the resource list like this, and incorporate the modified but complete list into the qalter command. For example:
```bash
qstat -j 1098765 | grep resource_list
hard resource_list:         test=false,suspendable=false,h_stack=10M,h_vmem=1G,h_rt=169200
qalter -l test=false,suspendable=false,h_stack=10M,h_vmem=800M,h_rt=12:0:0 1098765
```

As you can see, suspendable is not the only resource request that gets quietly added to your job by default!
I need to change the order of my waiting jobs
You can **shuffle** the order of your own jobs with the "job share" option to qalter or qsub. For example,
```bash
qalter -js 100 job_id
```

will boost the priority of the given job relative to the other jobs belonging to you. 
The change in priority may take 15 seconds or so to be reflected in qstat.

#### 8. How to merge output files
Usually there are four output files generated by Grid Engine for a parallel job: .o, .e, .pe and .po. 
The .\*e files represent stderr, and the .\*o files represent stdout, while the .p\* files get generated when there is a parallel environment specified in a submission script.
Users may want to reduce that number of files to just one. Here is how. The stderr and stdout streams can be merged with the following option in your submission script:
```bash
#$ -j y

# This will yield two files .o and .po instead of four. You can merge these two further if you explicitly specify a name for the output file like so:
#$ -o output.log

# The problem here is that if you submit several such jobs from the same directory, they will be writing to the same file, which is usually undesirable, so the advice would be to use a Grid Engine environment variable to set a unique file name like so:
#$ -o $JOB_ID.log

So, the recipe to get four files into one with a unique name is:
#$ -j y
```


#### 9. Warning: No xauth data; using fake authentication data for X11 forwarding
Your ~/.Xauthority file got corrupted. Please delete it manually, and next time you login with X11 forwarding enabled, it will get re-created.

#### 10. I need to extend the run-time limit for a running job
You cannot alter parameters of a running job. If you are sure that your jobs will not be able to finish on time, then it might be better to terminate and then re-submit it again with a different run-time limit.

---
## V. Others
### 1. man sge_conf
### 2. man sge_flags 
to know which resource flags are available:
vg, longidle, os_version, os_minor, kernel_version, os_distribution, model, os_bit, cputype, cpu_code, cpu_cache, vm, ht, regress/build, qsc, project, pool, mem_free, mem_inst, ncps, scratch_free, DEFAULT, arch, num_proc, swap_free, virtual_free, mem_used, swap_used, virtual_used, mem_total, swap_total, virtual_total,...

