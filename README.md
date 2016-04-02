# BUtils

## Introduction

This is a repository that holds a bunch of separated python scripts whose origin arises from a bunch of several independent ideas that are not big enough to have a dedicated repository and dedicated attention. Some of the utilities will be described in this *README* file and others maybe not. The idea is to keep this little ideas living in the realm of consciousness and to organize this birth living thoughts, that may end in nothing, but were important for me somewhere in this journey I call life.

## Networking

Here we have a folder dedicated to networking based experiences. It could be in the other repository called [pysniff](http://git.balhau.net/pysniff.git/) that is dedicated to low level networking protocols. But since this was a separated line of thought that impeled me to start the work this ended up as a miscellaneous script in this jungle of code. The most interesting thing here is the *upnp.py* script that uses the [Simple Service Discovery Protocol](https://en.wikipedia.org/wiki/Simple_Service_Discovery_Protocol) to ask the router for information. The next step here, if it will ever be one (muhahaha) would be to clean the code and give a more organized python API to query the router and give them instructions, namely for port forward rules based on this [UPNp](https://en.wikipedia.org/wiki/Universal_Plug_and_Play) philosophy.

## MEO

Don't worry I will not sell you ISP solutions. I'm a portuguese folk and in my country (Portugal, for those who don't know what portuguese mean) there is a [ISP](https://en.wikipedia.org/wiki/Internet_service_provider) called [MEO](https://www.meo.pt/) that used to setup [Thompson Routers](https://forum.meo.pt/t5/Servi%C3%A7o-Telefone/Tutorial-Como-Configurar-Router-MEO-THOMPSON-para-MEO-VOIP/td-p/2077) for their clients. It turns out that they were poorly configured and they were vulnerable to this [attack](http://lixei.me/algoritmo-chaves-wireless-thomson-meo/) so this is basically the python implemented described there. As a disclaimer I must add that no other routers were attacked, just my own for educational and proof of concept, purposes.

## Base

This was an initial idea of scrapping public services to automate analysis and in someway generates the project called [WebPtData](https://github.com/Balhau/WebPtData). This will scrap the
[Base.gov.pt](http://www.base.gov.pt/Base/pt/Homepage) site and inject the data in a local [MySQL](https://www.mysql.com/) database for further analysis.

## Ereader

I have an Ereader. Yes I'm capable of reading stuff, who would say!? So it turns out that my ereader is a [Cybook Ocean](https://www.bookeen.com/en/cybook-ocean) a very nice 8 inch ereader that sucks in terms of software and integration with other platforms. I'm a tech guy who also happens to use [Goodreads](https://www.goodreads.com/) to keep track of my reading status. It also happens that the integration between these two worlds is practically non existent so I decide to give it a help and try to mitigate this serious failure. The initial idea would be to use some goodreads API and do only the SQLite extraction of data and inject it in goodreads with one of the *given APIs*. It turns out that I didn't like any of them, [more on this subject here](https://codecorner.balhau.net/2016/02/28/goodreads-api/), and by this reason I decided also to implement my own goodreads API which is under the file goodreads.py.

## Installation

To install this package in your system you just need to run

    sudo pip install butils --extra-index-url http://pip.balhau.net/simple

This command line will fetch the last version from my local pip repository.
