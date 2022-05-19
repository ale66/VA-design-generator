
### Running Notebooks on a remote server

This quick guide is taken from a [blog entry](https://ljvmiranda921.github.io/notebook/2018/01/31/running-a-jupyter-notebook/) that describe the process in detail.

#### Setting up

For simplicity we are going to assume that both the server process and the client/remote viewing will be setup on port 8888 which is tipycally used for connecting to a Jupyter notebook running on the localhost.

0. On the local computer

Start a terminal (Terminal for MacOs, PowerShell for Windows, or Cmder) then type.

```bash
remoteuser@remotehost:>ssh -l remoteuser remotehost
```

So for me it looks like this:

```bash
ale@ale-xps15:>ssh -l ale vasari.bbk.ac.uk
```
Now we are connected to the remotehost

2. On the remote host

The needed notebook must be loaded there. Various methods exist, probably the easiest is to clone the respecitve Github repository on the remote host.
So,

```bash
remoteuser@remotehost:>jupyter notebook --no-browser --port=8888
```

So for me it looks like this:

```bash
ale@vasari:>jupyter mynotebook --no-browser --port=8888
```

The output is going to show a URL which has a long token string at its end, e.g.

```bash
http://localhost:8888/?token=867c531d9bb6a188bf2214b44e316be8e9c5734b9144b270
```

we will need the toke part for authentication later.


2. on your local computer open a terminal and say

```bash
>ssh -N -f -L localhost:888:localhost:8888 remoteuser@remotehost
```

where ``remoteuser@remotehost`` is something like ``ale@vasari.bbk.ac.uk``

Now, open a browser and point it to this URL:

```bash
http://localhost:8888
```

3. start the remote process

Back to the terminal wehere the ``ssh`` command was given, we start the process on the remote server:

```bash
remoteuser@remotehost:>jupyter notebook --no-browser --port=8888
```

4. Stop the remote execution

back to the terminal where whe original ``ssh`` connection is still open, give ``Control+C`` twice.

To control for possible hung-up of the server say

```bash
localuser@localhost:> sudo netstat -lpn |grep :8888
```

this will print the process number, PID, in parantheses, say ``(500)``.
Then:

```bash
localuser@localhost:>kill 500

localuser@localhost:>exit
```

