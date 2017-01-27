# XISA-TwitterAPI v1.0

## Main api site:
[API site](https://xisaapi.herokuapp.com/) - https://xisaapi.herokuapp.com


## GET calls

### Celebs with no category
* URL : https://xisaapi.herokuapp.com/getCelebs
* Example : https://xisaapi.herokuapp.com/getCelebs
* Params : None
* Callback : Array of celebs

### Celebs with category
* URL : https://xisaapi.herokuapp.com/getCelebs/<category>
* Example : https://xisaapi.herokuapp.com/getCelebs/crazy-ill
* Params : category must be one of this:
    * characteristics
    * body-parts
    * misogynist
    * gay-sexuality
    * crazy-ill
    * belief-agenda
* Callback : Array of celebs

### Celeb with no category
* URL = https://xisaapi.herokuapp.com/celeb/<last_name>
* Example = https://xisaapi.herokuapp.com/celeb/trump
* Params : last_name = the last name of the celeb
* Callback : Celeb with tweets

### Celeb with category
* URL = https://xisaapi.herokuapp.com/celeb/<last_name>/<category>
* Example = https://xisaapi.herokuapp.com/celeb/trump/crazy-ill
* Params : last_name = "trump", category must be one of this:
    * characteristics
    * body-parts
    * misogynist
    * gay-sexuality
    * crazy-ill
    * belief-agenda
* Callback : Celeb with tweets

### Users
* URL = https://xisaapi.herokuapp.com/getUsers
* Example = https://xisaapi.herokuapp.com/getUsers
* Params = none
* Callback : array of celebs

### User
* URL = https://xisaapi.herokuapp.com/user/xxx
* Example = https://xisaapi.herokuapp.com/user/realDonaldTrump
* Params = xxx = twitter screen_name without @
* Callback : array of celebs
* In case no such a user, will return null



