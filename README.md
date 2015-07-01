Compose Monkey
===============

Resiliency testing tool for docker-compose
------------------------------------------

[![asciicast](https://asciinema.org/a/22706.png)](https://asciinema.org/a/22706)

##Quick Install

Go to your existing application containing `fig.yml` config. And then:

```bash
$ pip install compose-monkey
$ docker-compose --monkey up
```

**Note** : `-m` / `--monkey` is the flag to activate `ComposeMonkey` and without that flag, `docker-compose` will run as usual.

If everything goes fine, a UI server gets started at the port 2020 (configurable) exposed on the host machine.

##What is Compose Monkey
Compose Monkey is a resiliency testing tool for applications running through `docker-compose`. It is a fork of [compose](https://github.com/docker/compose) which adds an opt-in feature to test the scenarios where the downstream services become flaky/down/slow.

It also provides a UI port to control the behavior of all the downstream services in real time. On start, all the downstream services behave as normal i.e. the proxy exhibits dummy behvaior.

Compose Monkey :

* Smartly suggests port and TCP protocol for the destination link
* Option to skip proxy creation for any link
* UI controller to change the behvaior of the link in real time.

##How it works
Internally, it uses a package [Vaurien](http://vaurien.readthedocs.org/) which provides TCP proxy and behavior simulation. For every link, ComposeMonkey injects a Vaurien container between the source and the destination service. To start a Vaurien container, it needs the TCP [protocol](http://vaurien.readthedocs.org/en/1.8/protocols.html) and the port needed to talk to the destination. ComposeMonkey makes a best effort strategy to find those and shows them to the user as defaults.

Destination Port is found by searching for `exposed port` of the destination, if any. Protocol is suggested naively by checking the downstream service name. User has the option to provide port/protocol of their choice if not satisfied with the defaults.

```
      +------------+           +-------------+            
      |            |           |             |            
      |    WEB     +----------->    REDIS    |            
      |            |           |             |            
      +------------+           +-------------+            
                                                          
                     Without --monkey                     
                                                          
                                                           

|                                                               |
|---------------------------------------------------------------|
|                                                               |

                                                          
+------------+        +------------+        +------------+
|            |        |            |        |            |
|    WEB     +--------> COMPOSMNKY +-------->    REDIS   |
|            |        |            |        |            |
+------------+        +-----^------+        +------------+
                            |                             
                            |                             
                            |                             
                      +-----+------+                      
                      |            |                      
                      |     UI     |                      
                      |            |                      
                      +------------+                      
                                                          
                                                          
                       With --monkey                      
```

##Future Work

ComposeMonkey can also be built and packaged outside of docker-compose. This can be implemented by creating a temporary `fig.yml` from the original config yaml file which has a vaurien container entry for each downstream link and single UI container which links all the proxy containers. This work is still in development.
