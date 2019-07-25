# Spotif... I Forgot
CLI-based album finder utilizing the Spotify API - enter songs from that album you kinda-sorta-but-don't-really remember, and see if the results jog your memory!

## Setup
From the repo's home directory:
```
./setup.sh
```
The `setup.sh` script does a few things:
* Create a new virtualenv named "env"
* Activate the virtualenv
* Install requirements

Once you've done that you should be good to go.

## Run the App
```
[user@Some-MBP: spotififorgot]$ source env/bin/activate
(env) [user@Some-MBP: spotififorgot]$ python run_app.py 
 .oooooo..o                          .    o8o   .o88o.                ooooo 
d8P'    `Y8                        .o8    `"'   888 `"                `888' 
Y88bo.      oo.ooooo.   .ooooo.  .o888oo oooo  o888oo                  888  
 `"Y8888o.   888' `88b d88' `88b   888   `888   888                    888  
     `"Y88b  888   888 888   888   888    888   888                    888  
oo     .d8P  888   888 888   888   888 .  888   888    .o. .o. .o.     888  
8""88888P'   888bod8P' `Y8bod8P'   "888" o888o o888o   Y8P Y8P Y8P    o888o 
             888                                                            
            o888o                                                           
                                                                            
oooooooooooo                                             .       
`888'     `8                                           .o8       
 888          .ooooo.  oooo d8b  .oooooooo  .ooooo.  .o888oo     
 888oooo8    d88' `88b `888""8P 888' `88b  d88' `88b   888       
 888    "    888   888  888     888   888  888   888   888       
 888         888   888  888     `88bod8P'  888   888   888 . .o. 
o888o        `Y8bod8P' d888b    `8oooooo.  `Y8bod8P'   "888" Y8P 
                                d"     YD                        
                                "Y88888P'                        
                                                                 

Album Finder

Enter songs from that album you kinda-sorta-but-don't-really remember, and see if the results jog your memory!

Enter a track name (\q to quit): Riders on the Storm

Most Likely Albums
1. 'L.A. Woman' by The Doors, released 1971-04-19 (Matched 1 Queries, Max Similarity of 1.0, Max Popularity of 70)
2. 'Shallow and Profound' by Yonderboi, released 2000-02-21 (Matched 1 Queries, Max Similarity of 1.0, Max Popularity of 42)
3. 'With Arms Wide Open: A Retrospective' by Creed, released 2015-01-01 (Matched 1 Queries, Max Similarity of 1.0, Max Popularity of 40)
4. 'Guitar Heaven: The Greatest Guitar Classics Of All Time (Deluxe Version)' by Santana,Chester Bennington,Ray Manzarek, released 2010-09-17 (Matched 1 Queries, Max Similarity of 1.0, Max Popularity of 36)
5. 'Forever Changing: The Golden Age Of Elektra Records 1963-1973' by The Doors, released 2007-01-23 (Matched 1 Queries, Max Similarity of 1.0, Max Popularity of 31)
6. 'Canyon Songs' by Lisa Bassenge, released 2015-09-25 (Matched 1 Queries, Max Similarity of 1.0, Max Popularity of 29)
7. 'The Doors (Original Soundtrack Recording)' by The Doors, released 1991-01-01 (Matched 1 Queries, Max Similarity of 1.0, Max Popularity of 24)
8. 'The Complete Studio Albums' by The Doors, released 2012-10-22 (Matched 1 Queries, Max Similarity of 1.0, Max Popularity of 23)
9. 'Lullaby Renditions of the Doors' by Rockabye Baby!, released 2017-04-28 (Matched 1 Queries, Max Similarity of 1.0, Max Popularity of 22)
10. 'Vol. 2' by Hippie Sabotage, released 2014-03-11 (Matched 1 Queries, Max Similarity of 1.0, Max Popularity of 18)


Enter a track name (\q to quit): 
```

## Possible improvements
* Some generic queries can take a while to run - a progress bar would be a good addition for the user's sanity
* Could possibly speed up execution time if I stop pinging the API once I get at least N good-enough looking matches
