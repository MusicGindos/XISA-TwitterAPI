# XISA-TwitterAPI v1.0

## Main api site:
[API site](https://xisaapi.herokuapp.com/) - https://xisaapi.herokuapp.com


## GET calls

### Celebs
* URL : https://xisaapi.herokuapp.com/getCelebs
* Example : https://xisaapi.herokuapp.com/getCelebs
* Params : None
* Callback : Array of celebs

### Celeb
* URL = https://xisaapi.herokuapp.com/celeb/xxx
* Example = https://xisaapi.herokuapp.com/celeb/trump
* Params : xxx = "trump"
* Callback : Celeb with tweets

### Users
* URL = https://xisaapi.herokuapp.com/getCelebs
* Example = https://xisaapi.herokuapp.com/getCelebs
* Params = none
* Callback : array of celebs

### User
* URL = https://xisaapi.herokuapp.com/user/xxx
* Example = https://xisaapi.herokuapp.com/user/realDonaldTrump
* Params = xxx = twitter screen_name without @
* Callback : array of celebs
* In case no such a user, will return null



