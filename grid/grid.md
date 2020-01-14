# uge&sge #
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



## 2. Job priorities
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
> The -P (`priority`) option allows users to designate the relative priority of a batch job for selection from a queue.
-A  account_string
    Define the account to which the resource consumption of the batch job should be charged.
-b y[es]|n[o]
    Gives the user the possibility to indicate explicitly whether command should be treated as binary or script. If the value of -b is 'y', then command  may be a binary or script.
> -e  path_name
    Define the path to be used for the standard error stream of the batch job.
-j y|n
    Specifies whether or not the standard error stream of the job is merged into the standard output stream. If both the -j y and the -e options are present, Univa Grid Engine sets but ignores the error-path attribute.
-shell y[es]|n[o]
    -shell n causes qsub to execute the command line directly, as if by exec(2).  No command shell will be executed for the job.  This option only applies when -b y is also used.  Without -b y, -shell n has no effect.
    This option can be used to speed up execution as some overhead, like the shell startup and sourcing the shell resource files is avoided.
-v  variable_list
    Add to the list of variables that are *exported* to the session leader of the batch job.
-V  Specify that all of the environment variables of the process are exported to the context of the batch job.
-N option allows users to associate a name with the batch job.
The -o option allows users to redirect the standard output stream.

Multithreaded job submission use `-pe mt <n>` option
Distributed job submission use `-pe dp <n>` option

 Batch Jobs (examples)
  Submit to bnormal project, and choose a Linux machine
> qsub -P bnormal -l arch=glinux $PATH/script.sh

  Submit to bnormal project and stay in the current working directory, and choose a AMD 64 type CPU
> qsub -P bnormal -cwd -l cputype=amd64 script.sh
  Submit to bhigh project, and choose a Solaris 64 bit machine which has at least 10GB of virtual memory free
> qsub -P bhigh -l arch=solari64,mem_free=10g script.sh

  Submit to bhigh and choose a Linux machine which has the BibMem kernel installed (capable of accessing upto 3.6GB memory)
> qsub -P bhigh -l model=PC2800 script.sh

  specify the job option in the job script with "\#\$" like:
> \#\$ -cwd
> \#\$ -N jobName


### 4. qstat
qstat - show the status of Univa Grid Engine jobs and queues

> -s {p|r|s|z|hu|ho|hs|hd|hj|ha|h|a}[+]
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

>
 -j   Prints all jobs `running` on the  queues  hosted  by  the shown hosts. This switch calls _-q_ implicitly. _-q_ Show information about the queues  instances hosted by the displayed hosts.
 -h display only selected hosts
 -l [resource request]
      Defines the resources to be granted by the hosts which should be included in the host list output.
 **-F** [ resource_name,... ]
    qhost will present a detailed listing of the current **resource availability** per host *with respect to* all resources (if the option argument is omitted) or with respect to those resources contained in the resource_name list. Please refer to the description of the Full Format in section OUTPUT FORMATS below  for  further detail.

```bash
# list running jobs on the queues hosts
   qhost -j
   job-ID     prior   name       user         state submit/start at     queue      master ja-task-ID
   -------------------------------------------------------------------------------------------------
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
                [-h hold_list][-j join_list][-k keep_list][-l resource_list]
                [-m mail_options][-M mail_list][-N name][-o path_name]
                [-p priority][-r y|n][-S path_name_list][-u user_list]
                job_identifier ...

Job Alert job:
qalter: use the same option and argument as the "qsub" to alter the queued job
The qalter utility allows users to change the attributes of a batch job. The qalter utility allows users to change the attributes of a batch job.

```bash
# adjust the job priority:
qalter -P <priority> <job_id_list>

# To test/verify a job requset is available:
qalter -w p 9068517

# adjust the mt setting to make the job submitted rather than 'qw'
> qalter -pt mt 1
```

The '-w' option:
>  -w e|w|n|p|v
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



### 7. qdel
> qdel - delete batch jobs
    qdel [ -f ] [ -help ] [ -u wc_user_list ] [ wc_job_range_list ] [ -t task_id_range ]


```bash
qdel -u <user_id>
qdel <job_id>
```

### 8. quser
quser - Show access/resource status for Grid Engine users

> quser [-help] [-l ResourceFlag ] [-u Username] [-ext]
         -help Print this usage message;
         -u    Username;
         -l    ResourceFlag;
         -sf <num> -  slots free
         -pe mt <num> - parallel environment mt usage
         -ext  Show rush queues & extended output-
               (OS KERNEL CPU MODEL QSC)


### 9. Job suspension:
  qhold &lt;job id&gt;
  qrls &lt;job id&gt;

## IV. FAQ

## V. Others
man sge_conf
man sge_flags to know which resource flags are available:
vg, longidle, os_version, os_minor, kernel_version, os_distribution, model, os_bit, cputype, cpu_code, cpu_cache, vm, ht, regress/build, qsc, project, pool, mem_free, mem_inst, ncps, scratch_free, DEFAULT, arch, num_proc, swap_free, virtual_free, mem_used, swap_used, virtual_used, mem_total, swap_total, virtual_total,...

