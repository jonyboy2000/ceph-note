```                                                                                                                                                                                                                                                                                                            |
                                                                                                                                                           
                                                   socat TCP4-LISTEN:30000,reuseaddr,fork TCP4:10.139.11.90:30000                                          
                                                                                                                                                           
                                 +-----------+              +-----------+          +-------------+                                                         
                                 |  jump1    +--------------+ jump2     +----------+ jump3       |                                                         
                           +----->     11.90 |              |    12.23  |          |             |                                                         
                           |     +-----------+              +-----------+          +-------------+                                                         
                           |     socat TCP-LISTEN:30000,fork TCP:127.0.0.1:1080                                                                            
                           |                                                         socat TCP4-LISTEN:30000,reuseaddr,fork TCP4:10.139.12.23:30000        
                           |                                                                                                                               
                           |反向代理                                                                                                                           |
                           |                                                                                                                               
                           |                                                                                                                               
                     +--------+                                                                                                                            
                     |  ss    |                                                                                                                            
                     |        |                                                                                                                            
                     | xshell |                                                                                                                            
                     +--------+                                                                                                                            

```


```
vps

socat TCP-LISTEN:993,fork TCP:imap.gmail.com:993
socat TCP-LISTEN:465,fork TCP:smtp.gmail.com:465
socat TCP-LISTEN:578,fork TCP:smtp.gmail.com:578
```
