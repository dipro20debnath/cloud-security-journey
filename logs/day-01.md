# Day 01 · Setup

**Date:** 2026-10-25 · **Time spent:** ~3 h · **Quiz:** 5/5

## What I did
- Set up my lab: Kali Linux (kernel 6.19, x86_64) running in VMware.
- Created this repository and its progress dashboard.
- Watched the first ~50 minutes of *Linux For DevOps In One Shot* (TrainWithShubham) and ran the basic commands myself.

## What I learned

| Command | What it does |
| --- | --- |
| `whoami` | Shows which user account I am logged in as. |
| `pwd` | Prints the folder (directory) I am currently in. |
| `ls -la` | Lists every file and folder in the current directory, including hidden ones, with size and permissions. |
| `uname -a` | Shows details of the system: OS, kernel version and hardware architecture. |
| `echo "..."` | Prints the given text to the screen. |

## Commands I ran (output trimmed)

Username and hostname are masked, and the `ls -la` output is cut short because it listed private project files.

```console
$ whoami
<user>
$ pwd
/home/<user>
$ ls -la
drwx------ 34 <user> <user> 4096 Oct 25 17:01 .
drwxr-xr-x  4 root   root   4096 Jul  2 03:11 ..
-rw-r--r--  1 <user> <user>  220 Apr 25  2026 .bash_logout
-rw-r--r--  1 <user> <user> 5605 Apr 25  2026 .bashrc
lrwxrwxrwx  1 <user> <user>    8 May 11 22:10 log -> /var/log
-rw-r--r--  1 <user> <user>  807 Apr 25  2026 .profile
...
$ uname -a
Linux <host> 6.19.11+kali-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.19.11-1kali1 (2026-04-09) x86_64 GNU/Linux
$ echo "Hello Cloud Security"
Hello Cloud Security
```

## Tomorrow
- Day 2 · Git fundamentals: init, add, commit, push.
