artnewgo.com
=
A searchable index of artworks on view in New York City (and, eventually, beyond)
-
Artnewgo is a Python web application, utilizing the Django framework, that employs Scrapy spiders to retrieve relevant data and the viewing status of artworks in major museums and collections. This data is relayed to a PostgreSQL database comprising of 11 relational tables. This data is made available to web traffic via dynamic dropdown menus and an Elasticsearch search index.

Database
-
The database relations are established in the following manner:

### Displays
Displays are comprised of:
* "start_date" (When the artwork was first displayed)
* "end_date" (When the artwork is known to be removed from display)
* "collection" (Collection in which the artwork is diplayed)
* "artwork"

### Artworks
Artworks are comprised of:
* "artist"
* "title"
* "date" (The date the artwork was created)
* "medium"
* "description" (A brief description of the artwork, if it exists)
* "dimensions"
* "pageurl" (The url for the artworks page on the collections website)
* "accession_number" (A unique number ascribed to individual artworks. Initials relating to the collection name are amended to the beginning of the accession number to insure uniqueness)
* "imageurl"
* "timestamp" (When the artwork was initially scraped)

### Artist
Artists are comprised of:
* "artist_sans_accents" (The artists name with all diacritics removed)
* "movements"
* "nationality" (Deprecated. see "new_nationality")
* "sex" ("gender" would have been a better word)
* "born"
* "died" (Again, "deceased" probably would have been better)
* "descriptors" (Deprecated. Initially established to contain metadata, this field is rarely used)
* "new_nationality" (Many to many. Artists can have multiple nationalitys)
* "ethnicity"
* "movement" (Artistic movements in which the artist was involved)
* "description" (A brief summary taken from, and attributed to, wikipedia.)

### Movements
Contains the title of the movement and a brief description.

### Name Variants
Contains known variations of the artists name in order to normalize incoming data.

### Last Crawls
Logs the last run date for each spider. In turn, the spiders are run twice daily. The first run is the main scrape. The second run is a fail safe in which the spider checks the log to see if an initial run took place and, if not, execute a scrape. This is to overcome Heroku's spotty scheduler.

### Ethnicity and Nationality are fairly self descriptive

To do list:
-
#### Establish a users app in which users can:
* Favorite artists in order to recieve updates about newly displayed artworks
* Check-off artworks that they have already viewed
* Favorite artworks that they intend to view
* Comment on artworks
* Share all of this with friends

#### Speed up the HTTP response time.

#### Make an "Exhibitions" model that represents current and upcoming exhibitions, along with the artists included.
