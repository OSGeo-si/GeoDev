# GeoDev Meetups Slovenia 🌍

This GeoDev Meetup is an open, friendly, technical gathering for GIS users, GIS developers, and anyone else interested in spatial data and in technologies used to process, analyze, and visualize it. From enthusiastic noobs to experts - everyone is welcome to join and share their geo-related ideas, experiences, questions, pains, or joys.

This GitHub repository is place to store all Meetup Materials, presentations and useful links.

## Next Meetups 🚀

__Datum__: Sreda, 23.09.2026 ob 18:00
__Lokacija__: [Urbanistični inštitut Republike Slovenije](https://www.uirs.si/sl-si/), Trnovski pristan 2, 1000 Ljubljana
[Vhod iz pasaže](https://www.openstreetmap.org/node/12504450770), predavalnica se nahaja v 2. nadstropju.


More details can be found here [GeoDev Meetup #16](2026-16-meetup/README.md).

Draft roadmap for the next meetups:

* __20.11.2024__: GeoDev Meetup #11       ✅
* __29.01.2025__: GeoDev Meetup #12       ✅
* __10.04.2025__: GeoDev Meetup #13       ✅
* __11.11.2025__: GeoDev Meetup #14       ✅
* __26.05.2026__: GeoDev Meetup #15       ✅
* __23.09.2026__: GeoDev Meetup #16       🎯

## Future Topics (Wish List) 🧞‍♂️

You can add your own suggestions to the list of future topics, or you can volunteer to present on one of the topics 
Just open an issue in this repository.

* Open data: where to find it, how to use it, how to contribute to it.
* How to create, update and host a Web Map for free. 
* How to configure a geoserver?
* Can we serve vector tiles from PostGIS (we do not have time to setup a Geoserver)?
* Overview of web-based mapping libraries like Openlayers, Leaflet.
* More about PostGis
* GIT
* [Kart](https://t.co/FSZ3V6t1NM)
* Docker
* Public speaking
* GeoPackage
* Račke 
* Koordinatni sistemi
* COG
* LAS/LAZ-COPC
* Conda / Mamba


## Supporters 💸

Become a supporter of GeoDev Meetup Slovenia. If you are interested in supporting GeoDev Meetup Slovenia, please contact
us by opening an issue in this repository.


## Publishing a New Event 📣

Step-by-step guide for adding a new GeoDev event across this repo, the [landing-page](https://github.com/OSGeo-si/landing-page) and the social channels. This is the workflow established with #15.

**1. Plan**
* Pick the next sequential number `N` and confirm date, time, venue, speakers.

**2. Add the event to this repo** (`OSGeoSi/GeoDev/`)
* Create folder `YYYY-N-meetup/` (year = event year, `N` = sequential meetup number).
* Copy `2026-15-meetup/README.md` as template; update title, date, location, the three program blocks (title, time-range, abstract, speaker) and the registration link in "Ostalo".
* Copy the three banner HTMLs from the previous event folder (`banner-story.html`, `banner-landscape.html`, `banner-square.html`); edit content. See [CLAUDE.md](CLAUDE.md) for naming/template conventions.
* Update top-level `README.md`: change the "Next Meetups" headline date and link, mark the previous event ✅ and add a new row 🎯 to the roadmap.

**3. Add the event to the [landing-page](https://github.com/OSGeo-si/landing-page) repo**
* Create `content/events/geodev/geodev-N.md` with frontmatter (`title`, `slug`, `date`, `time`, `location`, `lat`, `lng`, `eventUrl`, `tags: [geodev]`).
* Body: short intro + the program. Keep abstracts to roughly one paragraph each — long abstracts make the event page hard to skim.
* After the meetup, drop photos into `content/events/geodev/geodev-N/`.

**4. Create the Luma event** (https://lu.ma)
* Title `GeoDev Slovenija #N`, set date/time/location, capacity (50 default), free, theme "Minimalna".
* Use `banner-square.html` rendered PNG as the cover image.
* Copy the rendered Luma description from `najava.md` § 3 into the "Dodaj opis" field.
* Grab the short URL (e.g. `https://luma.com/<code>`) and paste it into:
   * This event's `README.md` ("Ostalo" → registration link)
   * The landing-page frontmatter (`eventUrl`)
   * `najava.md` (replace `{{LUMA_URL}}` placeholders everywhere)

**5. Render the banners to PNG**
```sh
cd scripts && npm install && npx playwright install chromium   # one-time
node banner-to-png.js ../YYYY-N-meetup/banner-*.html
```
Outputs `banner-*.png` next to each source HTML at 2× device pixel ratio.

**6. Compose promo copy**
* Copy `2026-15-meetup/najava.md` as template; rewrite for the new event.
* It already contains LinkedIn, newsletter, Luma description, Discord/Facebook, Twitter/X, and a short OSGeo-website blurb.

**7. Publish across channels** (in this order)
* [ ] Luma event live
* [ ] Landing-page deployed with the new event entry
* [ ] MailChimp newsletter sent
* [ ] LinkedIn post
* [ ] Discord announcement
* [ ] Facebook post
* [ ] Optional: Twitter/X, Meetup.com group

**8. After the event**
* Add speaker slides to `YYYY-N-meetup/0X-<slug>/` (one subfolder per talk).
* Drop photos into `YYYY-N-meetup/photos/` and into the landing-page event folder.
* Mark the event ✅ on the roadmap.


## Checklist for Organizers 🔖

* [ ] Use Checklist for organizing the event.
* [ ] Reserve the location, date and time.
* [ ] Find speakers (2).
* [ ] Find a sponsor for rent, pizzas and drinks.
* [ ] Update the GitHub repository with the new event details.
* [ ] Announce the event on Mailing list (MailChimp).
* [ ] Announce the event on OS Geo WebPAge.
* [ ] Announce the event on Facebook.
* [ ] Announce the event on Discord.
* [ ] Come to venue 30 minutes before the event starts.
* [ ] Prepare the projector and the screen.
* [ ] Update the GitHub repository with the new event details.
* [ ] Repeat. :) 

## Useful links 📖

_Groups_

* [Discord Group OSGeo Slovenia](https://discord.gg/aJtB6VxG) This is most active group.
* [MeetUp Group GeoDev Slovenia](https://www.meetup.com/GeoDev-Meetup-Slovenia/)
* [Facebook Group GeoDev Slovenia](https://www.facebook.com/geodevslovenia/)
* [Slack Group Qgis Slovenia](https://qgisslovenia.slack.com/)
* 

_Data_

* [Slovenski Inspire metapodatkovni portal](http://prostor4.gov.si/imps/srv/slv/catalog.search#/home)
* [Odprti podatki Slovenije](https://podatki.gov.si/)


![alt text](./resources/geodev-raccoon.svg "GeoRaccoon")
